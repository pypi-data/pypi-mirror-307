import dataclasses
import hashlib
import logging
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional, Union

import pandas as pd

from databricks.rag_eval import context, env_vars, session
from databricks.rag_eval.datasets import entities as datasets_entities
from databricks.rag_eval.evaluation import entities as eval_entities
from databricks.rag_eval.utils import error_utils, progress_bar_utils, rate_limit

_logger = logging.getLogger(__name__)


_ANSWER_TYPES = [datasets_entities.SyntheticAnswerType.MINIMAL_FACTS]


@context.eval_context
def generate_evals_df(
    docs: Union[pd.DataFrame, "pyspark.sql.DataFrame"],  # noqa: F821
    *,
    num_evals: int,
    guidelines: Optional[str] = None,
) -> pd.DataFrame:
    """
    Generate an evaluation dataset with questions and expected answers.
    Generated evaluation set can be used with Databricks Agent Evaluation
    (https://docs.databricks.com/en/generative-ai/agent-evaluation/evaluate-agent.html).

    :param docs: A pandas/Spark DataFrame with a text column `content` and a `doc_uri` column.
    :param num_evals: The number of questions (and corresponding answers) to generate in total.
    :param guidelines: Optional guidelines to help guide the synthetic generation. This is a free-form string that will
        be used to prompt the generation. The string can be formatted in markdown and may include sections like:
        - Task Description: Overview of the agent's purpose and scope
        - User Personas: Types of users the agent should support
        - Example Questions: Sample questions to guide generation
        - Additional Guidelines: Extra rules or requirements
    """
    # Configs
    max_num_example_question = (
        env_vars.AGENT_EVAL_GENERATE_EVALS_MAX_NUM_EXAMPLE_QUESTIONS.get()
    )
    question_generation_rate_limit_config = rate_limit.RateLimitConfig(
        quota=env_vars.AGENT_EVAL_GENERATE_EVALS_QUESTION_GENERATION_RATE_LIMIT_QUOTA.get(),
        time_window_in_seconds=env_vars.AGENT_EVAL_GENERATE_EVALS_QUESTION_GENERATION_RATE_LIMIT_TIME_WINDOW_IN_SECONDS.get(),
    )
    answer_generation_rate_limit_config = rate_limit.RateLimitConfig(
        quota=env_vars.AGENT_EVAL_GENERATE_EVALS_ANSWER_GENERATION_RATE_LIMIT_QUOTA.get(),
        time_window_in_seconds=env_vars.AGENT_EVAL_GENERATE_EVALS_ANSWER_GENERATION_RATE_LIMIT_TIME_WINDOW_IN_SECONDS.get(),
    )
    max_workers = env_vars.RAG_EVAL_MAX_WORKERS.get()

    # Input validation
    if not isinstance(num_evals, int):
        raise error_utils.ValidationError("`num_evals` must be a positive integer.")
    if num_evals < 1:
        raise error_utils.ValidationError("`num_evals` must be at least 1.")
    example_questions = _read_example_questions(None)
    if example_questions and len(example_questions) > max_num_example_question:
        example_questions = example_questions[:max_num_example_question]
        _logger.warning(
            f"example_questions has been truncated to {max_num_example_question} items."
        )
    if guidelines is not None and not isinstance(guidelines, str):
        raise error_utils.ValidationError(
            f"Unsupported type for `guidelines`: {type(guidelines)}. "
            "`guidelines` must be a string."
        )

    # Rate limiters
    question_generation_rate_limiter = rate_limit.RateLimiter.build_from_config(
        question_generation_rate_limit_config
    )
    answer_generation_rate_limiter = rate_limit.RateLimiter.build_from_config(
        answer_generation_rate_limit_config
    )

    generate_evals: List[eval_entities.EvalItem] = []
    docs: List[datasets_entities.Document] = _read_docs(docs)
    session.current_session().set_synthetic_generation_num_docs(len(docs))
    session.current_session().set_synthetic_generation_num_evals(num_evals)

    # Plan the generation tasks
    generation_tasks = _plan_generation_tasks(docs, num_evals)

    # Use a progress manager to show the progress of the generation
    with progress_bar_utils.ThreadSafeProgressManager(
        total=num_evals,
        disable=False,
        desc="Generating evaluations",
        smoothing=0,  # 0 means using average speed for remaining time estimates
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} evals generated [Elapsed: {elapsed}, Remaining: {remaining}]",
    ) as progress_manager:
        with ThreadPoolExecutor(max_workers) as executor:
            futures = [
                executor.submit(
                    _generate_evals_for_doc,
                    task=task,
                    example_questions=example_questions,
                    guidelines=guidelines,
                    question_generation_rate_limiter=question_generation_rate_limiter,
                    answer_generation_rate_limiter=answer_generation_rate_limiter,
                    progress_manager=progress_manager,
                )
                for task in generation_tasks
            ]
            try:
                for future in as_completed(futures):
                    result = future.result()
                    generate_evals.extend(result)
            except KeyboardInterrupt:
                for future in futures:
                    future.cancel()
                _logger.info("Generation interrupted.")
                raise

    return pd.DataFrame(
        [
            pd.Series(generate_eval.as_dict(use_chat_completion_request_format=True))
            for generate_eval in generate_evals
        ]
    )


# ========================== Generation task planning ==========================
@dataclasses.dataclass
class _GenerationTask:
    doc: datasets_entities.Document
    """ The document to generate evaluations from. """
    num_evals_to_generate: int
    """ The number of evaluations to generate from this document. """


def _plan_generation_tasks(
    docs: List[datasets_entities.Document], num_evals: int
) -> List[_GenerationTask]:
    """
    Create an execution plan to distribute the number of evals to generate for each document based on the number of
    tokens in the document. The number of tokens in the document is used as a proxy for the amount of information
    in the document. Here is the high-level plan:
    - Sum up the tokens from all the docs and determine `tokens_per_eval = ceil(sum_all_tokens / num_evals)`
    - Walk each doc and generate `num_evals_for_doc = ceil(doc_tokens / tokens_per_eval)`
    - Stop early when we’ve generated `num_evals` in total

    :param docs: the list of documents to generate evaluations from
    :param num_evals: the number of evaluations to generate in total
    """
    sum_all_tokens_in_docs = sum(doc.num_tokens for doc in docs if doc.num_tokens)
    tokens_per_eval = math.ceil(sum_all_tokens_in_docs / num_evals)

    generation_tasks: List[_GenerationTask] = []
    num_evals_planned = 0
    for doc in docs:
        if not doc.num_tokens:
            continue
        num_evals_for_doc = (
            math.ceil(doc.num_tokens / tokens_per_eval) if tokens_per_eval > 0 else 1
        )
        num_evals_for_doc = min(
            num_evals_for_doc, num_evals - num_evals_planned
        )  # Cap the number of evals
        generation_tasks.append(
            _GenerationTask(doc=doc, num_evals_to_generate=num_evals_for_doc)
        )
        num_evals_planned += num_evals_for_doc
        # Stop early if we've generated enough evals
        if num_evals_planned >= num_evals:
            break
    return generation_tasks


# ========================== Generation task execution ==========================
def _generate_evals_for_doc(
    task: _GenerationTask,
    example_questions: Optional[List[str]],
    guidelines: Optional[str],
    question_generation_rate_limiter: rate_limit.RateLimiter,
    answer_generation_rate_limiter: rate_limit.RateLimiter,
    progress_manager: progress_bar_utils.ThreadSafeProgressManager,
) -> List[eval_entities.EvalItem]:
    """
    Generate evaluations for a single document.

    :param task: a generation task
    :param example_questions: optional list of example questions to guide the synthetic generation
    :param guidelines: optional guidelines to guide the question generation
    :param question_generation_rate_limiter: rate limiter for question generation
    :param answer_generation_rate_limiter: rate limiter for answer generation
    """
    doc = task.doc
    num_evals_to_generate = task.num_evals_to_generate

    if not doc.content or not doc.content.strip():
        _logger.warning(f"Skip {doc.doc_uri} because it has empty content.")
        return []

    client = _get_managed_evals_client()
    with question_generation_rate_limiter:
        try:
            generated_questions = client.generate_questions(
                doc=doc,
                num_questions=num_evals_to_generate,
                example_questions=example_questions,
                guidelines=guidelines,
            )
        except Exception as e:
            _logger.warning(f"Failed to generate questions for doc {doc.doc_uri}: {e}")
            return []

    if not generated_questions:
        return []

    generated_answers: List[datasets_entities.SyntheticAnswer] = []
    # Use a thread pool to run answer generation in parallel
    # Use the number of questions as the number of workers
    with ThreadPoolExecutor(max_workers=len(generated_questions)) as executor:
        futures = [
            executor.submit(
                _generate_answer_for_question,
                question=question,
                answer_generation_rate_limiter=answer_generation_rate_limiter,
            )
            for question in generated_questions
        ]

        try:
            for future in as_completed(futures):
                result = future.result()
                generated_answers.append(result)
                progress_manager.update()
        except KeyboardInterrupt:
            for future in futures:
                future.cancel()
            _logger.info("Generation interrupted.")
            raise
    return [
        eval_entities.EvalItem(
            question_id=hashlib.sha256(
                generated_answer.question.question.encode()
            ).hexdigest(),
            question=generated_answer.question.question,
            ground_truth_answer=generated_answer.synthetic_ground_truth,
            ground_truth_retrieval_context=eval_entities.RetrievalContext(
                chunks=[
                    eval_entities.Chunk(
                        doc_uri=generated_answer.question.source_doc_uri,
                        content=generated_answer.question.source_context,
                    )
                ]
            ),
            grading_notes=generated_answer.synthetic_grading_notes,
            expected_facts=generated_answer.synthetic_minimal_facts,
            source_doc_uri=generated_answer.question.source_doc_uri,
        )
        for generated_answer in generated_answers
        if generated_answer is not None
    ]


def _generate_answer_for_question(
    question: datasets_entities.SyntheticQuestion,
    answer_generation_rate_limiter: rate_limit.RateLimiter,
) -> Optional[datasets_entities.SyntheticAnswer]:
    """
    Generate an answer for a single question.

    :param question: the question to generate an answer for
    :param answer_generation_rate_limiter: rate limiter for answer generation
    """
    if not question.question or not question.question.strip():
        # Skip empty questions
        return None

    client = _get_managed_evals_client()
    with answer_generation_rate_limiter:
        try:
            return client.generate_answer(question=question, answer_types=_ANSWER_TYPES)
        except Exception as e:
            _logger.warning(
                f"Failed to generate answer for question '{question.question}': {e}"
            )
            return None


# ========================== I/O helpers ==========================
def _read_example_questions(
    example_questions: Optional[Union[List[str], pd.DataFrame, pd.Series]],
) -> Optional[List[str]]:
    """
    Read example questions from the input.
    """
    if example_questions is None:
        return None

    if isinstance(example_questions, pd.DataFrame):
        if not len(example_questions.columns) == 1:
            raise error_utils.ValidationError(
                "`example_questions` DataFrame must have a single string column"
            )
        return example_questions.iloc[:, 0].to_list()

    if isinstance(example_questions, pd.Series):
        return example_questions.to_list()

    if isinstance(example_questions, List):
        return list(example_questions)

    raise error_utils.ValidationError(
        f"Unsupported type for `example_questions`: {type(example_questions)}. "
        "`example_questions` can be a list of strings, a pandas Series of strings, or a pandas DataFrame with a single string column."
    )


def _read_docs(
    docs: Union[pd.DataFrame, "pyspark.sql.DataFrame"],  # noqa: F821
) -> List[datasets_entities.Document]:
    """
    Read documents from the input pandas/Spark DateFrame.
    """
    if docs is None:
        raise error_utils.ValidationError("Input docs must not be None.")

    if isinstance(docs, pd.DataFrame):
        # read from pandas DataFrame
        return _read_docs_from_pandas_df(docs)

    # Import pyspark here to avoid hard dependency on pyspark
    import pyspark.sql.connect.dataframe

    if isinstance(
        docs, (pyspark.sql.DataFrame, pyspark.sql.connect.dataframe.DataFrame)
    ):
        # read from Spark DataFrame
        return _read_docs_from_spark_df(docs)

    raise ValueError(
        f"Unsupported type for `docs`: {type(docs)}. "
        f"`docs` can be a pandas/Spark DataFrame with a text column `content` and a `doc_uri` column."
    )


def _read_docs_from_pandas_df(pd_df: pd.DataFrame) -> List[datasets_entities.Document]:
    """
    Read documents from a pandas DataFrame.
    """
    # check if the input DataFrame has the required columns
    if "doc_uri" not in pd_df.columns or "content" not in pd_df.columns:
        raise error_utils.ValidationError(
            "`docs` DataFrame must have 'doc_uri' and 'content' columns."
        )
    return [
        datasets_entities.Document(
            doc_uri=row["doc_uri"],
            content=row["content"],
        )
        for _, row in pd_df.iterrows()
    ]


def _read_docs_from_spark_df(
    spark_df: "pyspark.sql.DataFrame",  # noqa: F821
) -> List[datasets_entities.Document]:
    """
    Read documents from a Spark DataFrame.
    """
    # check if the input DataFrame has the required columns
    if "doc_uri" not in spark_df.columns or "content" not in spark_df.columns:
        raise error_utils.ValidationError(
            "`docs` DataFrame must have 'doc_uri' and 'content' columns"
        )
    return [
        datasets_entities.Document(
            doc_uri=row.asDict()["doc_uri"],
            content=row.asDict()["content"],
        )
        for row in spark_df.collect()
    ]


# ================================ Misc. helpers ================================
def _get_managed_evals_client():
    """
    Get a managed evals client.
    """
    return context.get_context().build_managed_evals_client()
