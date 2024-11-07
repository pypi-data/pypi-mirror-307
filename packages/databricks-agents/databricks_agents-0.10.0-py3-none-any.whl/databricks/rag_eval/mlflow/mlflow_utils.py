"""Helper functions to convert RagEval entities to MLflow entities."""

import time
from typing import List, Optional, Union

from mlflow import evaluation as mlflow_eval
from mlflow.entities import metric as mlflow_metric

from databricks.rag_eval import schemas
from databricks.rag_eval.evaluation import entities
from databricks.rag_eval.utils import enum_utils

_CHUNK_INDEX_KEY = "chunk_index"
_IS_OVERALL_ASSESSMENT_KEY = "is_overall_assessment"


class EvaluationErrorCode(enum_utils.StrEnum):
    MODEL_ERROR = "MODEL_ERROR"


def eval_result_to_mlflow_evaluation(
    eval_result: entities.EvalResult,
) -> mlflow_eval.Evaluation:
    """
    Convert an EvalResult object to an MLflow Evaluation object.

    :param eval_result: EvalResult object
    :return: MLflow Evaluation object
    """
    eval_item = eval_result.eval_item
    # Inputs
    inputs = {
        schemas.REQUEST_COL: eval_item.question,
    }
    # Outputs
    outputs = {}
    if eval_item.retrieval_context:
        outputs[schemas.RETRIEVED_CONTEXT_COL] = (
            eval_item.retrieval_context.to_output_dict()
        )
    if eval_item.answer:
        outputs[schemas.RESPONSE_COL] = eval_item.answer
    # Targets
    targets = {}
    if eval_item.ground_truth_answer:
        targets[schemas.EXPECTED_RESPONSE_COL] = eval_item.ground_truth_answer
    if eval_item.ground_truth_retrieval_context:
        targets[schemas.EXPECTED_RETRIEVED_CONTEXT_COL] = (
            eval_item.ground_truth_retrieval_context.to_output_dict()
        )
    if eval_item.grading_notes:
        targets[schemas.GRADING_NOTES_COL] = eval_item.grading_notes
    if eval_item.expected_facts:
        targets[schemas.EXPECTED_FACTS_COL] = eval_item.expected_facts
    # Assessments
    assessments = []
    for assessment_result in eval_result.assessment_results:
        assessments.extend(assessment_result_to_mlflow_assessments(assessment_result))
    # Overall assessment
    overall_assessment = _get_overall_assessment(eval_result)
    if overall_assessment:
        assessments.append(overall_assessment)
    # Metrics
    metrics = eval_result_to_mlflow_metrics(eval_result)

    # Tags
    tags = {}
    if eval_item.managed_evals_eval_id:
        tags[schemas.MANAGED_EVALS_EVAL_ID_COL] = eval_item.managed_evals_eval_id
    if eval_item.managed_evals_dataset_id:
        tags[schemas.MANAGED_EVALS_DATASET_ID_COL] = eval_item.managed_evals_dataset_id
    if eval_item.source_doc_uri:
        tags[schemas.SOURCE_DOC_URI_COL] = eval_item.source_doc_uri

    error_message = None
    error_code = None
    if eval_item.model_error_message:
        error_code = EvaluationErrorCode.MODEL_ERROR
        error_message = eval_item.model_error_message

    evaluation = mlflow_eval.Evaluation(
        inputs=inputs,
        outputs=outputs,
        inputs_id=eval_item.question_id,
        request_id=eval_item.trace.info.request_id if eval_item.trace else None,
        targets=targets,
        error_code=error_code,
        error_message=error_message,
        assessments=assessments,
        metrics=metrics,
        tags=tags,
    )

    return evaluation


def eval_result_to_mlflow_metrics(
    eval_result: entities.EvalResult,
) -> List[mlflow_metric.Metric]:
    """Get a list of MLflow Metric objects from an EvalResult object."""
    return [
        _construct_mlflow_metrics(
            key=k,
            value=v,
        )
        for k, v in eval_result.get_metrics_dict().items()
        # Do not log metrics with non-numeric-or-boolean values
        if isinstance(v, (int, float, bool))
    ]


def _construct_mlflow_metrics(
    key: str, value: Union[int, float, bool]
) -> mlflow_metric.Metric:
    """
    Construct an MLflow Metric object from key and value.
    Timestamp is the current time and step is 0.
    """
    return mlflow_metric.Metric(
        key=key,
        value=value,
        timestamp=int(time.time() * 1000),
        step=0,
    )


def assessment_result_to_mlflow_assessments(
    assessment_result: entities.AssessmentResult,
) -> List[mlflow_eval.Assessment]:
    """
    Convert an AssessmentResult object to a list of MLflow Assessment object.

    A single PerChunkAssessmentResult object can be converted to multiple MLflow Assessment objects.

    :param assessment_result: AssessmentResult object
    :return: MLflow Assessment object
    """
    if isinstance(assessment_result, entities.PerRequestAssessmentResult):
        return [
            mlflow_eval.Assessment(
                name=assessment_result.assessment_name,
                source=_convert_to_ai_judge_assessment_source(
                    assessment_result.assessment_source
                ),
                value=assessment_result.rating.categorical_value,
                rationale=assessment_result.rating.rationale,
                error_message=assessment_result.rating.error_message,
                error_code=assessment_result.rating.error_code,
            )
        ]
    elif isinstance(assessment_result, entities.PerChunkAssessmentResult):
        return [
            mlflow_eval.Assessment(
                name=assessment_result.assessment_name,
                source=_convert_to_ai_judge_assessment_source(
                    assessment_result.assessment_source
                ),
                value=rating.categorical_value,
                rationale=rating.rationale,
                error_message=rating.error_message,
                error_code=rating.error_code,
                metadata={_CHUNK_INDEX_KEY: index},
            )
            for index, rating in assessment_result.positional_rating.items()
        ]
    else:
        raise ValueError(
            f"Unsupported assessment result type: {type(assessment_result)}"
        )


def _convert_to_ai_judge_assessment_source(
    assessment_source: entities.AssessmentSource,
) -> mlflow_eval.AssessmentSource:
    """
    Convert an AssessmentSource object to a MLflow AssessmentSource object.
    Source type is always AI_JUDGE.
    """
    return mlflow_eval.AssessmentSource(
        source_type=mlflow_eval.AssessmentSourceType.AI_JUDGE,
        source_id=assessment_source.source_id,
    )


def _get_overall_assessment(
    eval_result: entities.EvalResult,
) -> Optional[mlflow_eval.Assessment]:
    """
    Get optional overall assessment from a EvalResult object.

    :param eval_result: A EvalResult object
    :return: Optional overall assessment
    """
    return (
        mlflow_eval.Assessment(
            name=schemas.OVERALL_ASSESSMENT,
            source=_convert_to_ai_judge_assessment_source(
                entities.AssessmentSource.builtin()
            ),
            value=eval_result.overall_assessment.categorical_value,
            rationale=eval_result.overall_assessment.rationale,
            metadata={_IS_OVERALL_ASSESSMENT_KEY: True},
        )
        if eval_result.overall_assessment
        else None
    )
