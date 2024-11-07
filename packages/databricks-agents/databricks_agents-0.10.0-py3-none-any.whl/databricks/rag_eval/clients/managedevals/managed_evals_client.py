from typing import Collection, Dict, List, Optional

import requests
from urllib3.util import retry

from databricks import version
from databricks.rag_eval import env_vars, session
from databricks.rag_eval.clients import databricks_api_client
from databricks.rag_eval.datasets import entities

SESSION_ID_HEADER = "managed-evals-session-id"
CLIENT_VERSION_HEADER = "managed-evals-client-version"
SYNTHETIC_GENERATION_NUM_DOCS_HEADER = "managed-evals-synthetic-generation-num-docs"
SYNTHETIC_GENERATION_NUM_EVALS_HEADER = "managed-evals-synthetic-generation-num-evals"


def _get_synthetic_retry_config():
    return retry.Retry(
        total=env_vars.AGENT_EVAL_GENERATE_EVALS_MAX_RETRIES.get(),
        backoff_factor=env_vars.AGENT_EVAL_GENERATE_EVALS_BACKOFF_FACTOR.get(),
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_jitter=env_vars.AGENT_EVAL_GENERATE_EVALS_BACKOFF_JITTER.get(),
        allowed_methods=frozenset(
            ["GET", "POST"]
        ),  # by default, it doesn't retry on POST
    )


def _raise_for_status(resp: requests.Response) -> None:
    """
    Raise an Exception if the response is an error.
    Custom error message is extracted from the response JSON.
    """
    if resp.status_code == requests.codes.ok:
        return
    http_error_msg = ""
    if 400 <= resp.status_code < 500:
        http_error_msg = (
            f"{resp.status_code} Client Error: {resp.reason}\n{resp.text}. "
        )
    elif 500 <= resp.status_code < 600:
        http_error_msg = (
            f"{resp.status_code} Server Error: {resp.reason}\n{resp.text}. "
        )
    raise requests.HTTPError(http_error_msg, response=resp)


class ManagedEvalsClient(databricks_api_client.DatabricksAPIClient):
    """
    Client to interact with the managed-evals service.
    """

    def __init__(
        self,
        api_url: str,
        api_token: str,
    ):
        super().__init__(
            api_url=api_url,
            api_token=api_token,
            version="2.0",
        )

    def _session(
        self,
        retry_config: Optional[retry.Retry] = None,
    ) -> requests.Session:
        default_headers = {
            CLIENT_VERSION_HEADER: version.VERSION,
        }
        session = self.get_request_session(retry_config)
        session.headers.update(default_headers)
        session.auth = self.get_auth()
        return session

    def generate_questions(
        self,
        *,
        doc: entities.Document,
        num_questions: int,
        example_questions: Optional[List[str]],
        guidelines: Optional[str],
    ) -> List[entities.SyntheticQuestion]:
        """
        Generate synthetic questions for the given document.
        """
        request_json = {
            "doc_content": doc.content,
            "num_questions": num_questions,
            "example_questions": example_questions,
            "guidelines": guidelines,
        }
        with self._session(_get_synthetic_retry_config()) as session:
            resp = session.post(
                url=self.get_method_url("/managed-evals/generate-questions"),
                json=request_json,
                headers=self._get_synthesis_headers(),
            )

        _raise_for_status(resp)

        response_json = resp.json()
        if "questions" not in response_json or "error" in response_json:
            raise ValueError(f"Invalid response: {response_json}")
        return [
            entities.SyntheticQuestion(
                question=question,
                source_doc_uri=doc.doc_uri,
                source_context=doc.content,
            )
            for question in response_json["questions"]
        ]

    def generate_answer(
        self,
        *,
        question: entities.SyntheticQuestion,
        answer_types: Collection[entities.SyntheticAnswerType],
    ) -> entities.SyntheticAnswer:
        """
        Generate synthetic answer for the given question.
        """
        request_json = {
            "question": question.question,
            "context": question.source_context,
            "answer_types": [str(answer_type) for answer_type in answer_types],
        }

        with self._session(_get_synthetic_retry_config()) as session:
            resp = session.post(
                url=self.get_method_url("/managed-evals/generate-answer"),
                json=request_json,
                headers=self._get_synthesis_headers(),
            )

        _raise_for_status(resp)

        response_json = resp.json()
        return entities.SyntheticAnswer(
            question=question,
            synthetic_ground_truth=response_json.get("synthetic_ground_truth"),
            synthetic_grading_notes=response_json.get("synthetic_grading_notes"),
            synthetic_minimal_facts=response_json.get("synthetic_minimal_facts"),
        )

    def _get_synthesis_headers(self) -> Dict[str, str]:
        """
        Constructs the request headers for synthetic generation.
        """
        eval_session = session.current_session()
        if eval_session is None:
            return {}
        return {
            SESSION_ID_HEADER: eval_session.session_id,
            SYNTHETIC_GENERATION_NUM_DOCS_HEADER: str(
                eval_session.synthetic_generation_num_docs
            ),
            SYNTHETIC_GENERATION_NUM_EVALS_HEADER: str(
                eval_session.synthetic_generation_num_evals
            ),
        }

    def create_evals_table(
        self,
        evals_table_name: str,
        *,
        eval_mode: Optional[entities.EvalMode] = None,
        agent_name: Optional[str] = None,
        model_serving_endpoint_name: Optional[str] = None,
        docs_table_name: Optional[str] = None,
        primary_key_col_name: Optional[str] = None,
        content_col_name: Optional[str] = None,
        docs_render_mode: Optional[entities.DocsRenderMode] = None,
    ) -> entities.EvalsInstance:
        evals_instance = entities.EvalsInstance(
            eval_mode=eval_mode,
            agent_name=agent_name,
            model_serving_endpoint_name=model_serving_endpoint_name,
            docs_table_name=docs_table_name,
            primary_key_col_name=primary_key_col_name,
            content_col_name=content_col_name,
            docs_render_mode=docs_render_mode,
        )
        request_body = {"instance": evals_instance.to_json()}
        with self._session() as session:
            response = session.post(
                url=self.get_method_url(f"/managed-evals/instances/{evals_table_name}"),
                json=request_body,
            )
        _raise_for_status(response)
        return entities.EvalsInstance.from_json(response.json())

    def delete_evals_table(self, evals_table_name: str) -> None:
        with self._session() as session:
            response = session.delete(
                url=self.get_method_url(f"/managed-evals/instances/{evals_table_name}"),
            )
        _raise_for_status(response)

    def update_evals_table(
        self,
        evals_table_name: str,
        *,
        eval_mode: Optional[entities.EvalMode] = None,
        agent_name: Optional[str] = None,
        model_serving_endpoint_name: Optional[str] = None,
        docs_table_name: Optional[str] = None,
        primary_key_col_name: Optional[str] = None,
        content_col_name: Optional[str] = None,
        docs_render_mode: Optional[entities.DocsRenderMode] = None,
    ) -> entities.EvalsInstance:
        evals_instance = entities.EvalsInstance(
            eval_mode=eval_mode,
            agent_name=agent_name,
            model_serving_endpoint_name=model_serving_endpoint_name,
            docs_table_name=docs_table_name,
            primary_key_col_name=primary_key_col_name,
            content_col_name=content_col_name,
            docs_render_mode=docs_render_mode,
        )
        request_body = {
            "instance": evals_instance.to_json(),
            "update_mask": evals_instance.get_fieldmask(),
        }

        with self._session() as session:
            response = session.patch(
                url=self.get_method_url(f"/managed-evals/instances/{evals_table_name}"),
                json=request_body,
            )
        _raise_for_status(response)
        return entities.EvalsInstance.from_json(response.json())

    def get_evals_table(self, evals_table_name: str) -> entities.EvalsInstance:
        with self._session() as session:
            response = session.get(
                url=self.get_method_url(f"/managed-evals/instances/{evals_table_name}"),
            )
        _raise_for_status(response)
        return entities.EvalsInstance.from_json(response.json())
