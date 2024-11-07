import dataclasses
import functools
import inspect
import logging
from typing import Any, Callable, Dict, List, Optional

import mlflow.metrics

from databricks.rag_eval import schemas
from databricks.rag_eval.evaluation import entities, metrics
from databricks.rag_eval.utils import error_utils

_logger = logging.getLogger(__name__)


def _get_full_args_for_custom_metric(eval_item: entities.EvalItem) -> Dict[str, Any]:
    """Get the all available arguments for the custom metrics."""
    return {
        schemas.REQUEST_ID_COL: eval_item.question_id,
        schemas.REQUEST_COL: eval_item.raw_request,
        schemas.RESPONSE_COL: eval_item.raw_response or eval_item.answer,
        schemas.RETRIEVED_CONTEXT_COL: (
            eval_item.retrieval_context.to_output_dict()
            if eval_item.retrieval_context
            else None
        ),
        schemas.EXPECTED_RESPONSE_COL: eval_item.ground_truth_answer,
        schemas.EXPECTED_FACTS_COL: eval_item.expected_facts,
        schemas.EXPECTED_RETRIEVED_CONTEXT_COL: (
            eval_item.ground_truth_retrieval_context.to_output_dict()
            if eval_item.ground_truth_retrieval_context
            else None
        ),
        schemas.TRACE_COL: eval_item.trace,
    }


@dataclasses.dataclass
class CustomMetric(metrics.Metric):
    """
    A custom metric that runs a user-defined evaluation function.

    :param name: The name of the metric.
    :param eval_fn: A user-defined function that computes the metric value.
    """

    name: str
    eval_fn: Callable[..., Any]

    def run(
        self,
        *,
        eval_item: Optional[entities.EvalItem] = None,
        assessment_results: Optional[List[entities.AssessmentResult]] = None,
    ) -> List[entities.MetricResult]:
        if eval_item is None:
            return []

        kwargs = self._get_kwargs(eval_item)
        try:
            # noinspection PyCallingNonCallable
            metric_value = self.eval_fn(**kwargs)
            if metric_value is not None and not isinstance(
                metric_value, (int, float, bool)
            ):
                raise error_utils.ValidationError(
                    f"Metric '{self.name}' should return a number or a boolean. "
                    f"Got {type(metric_value)}.",
                )
        except Exception as e:
            _logger.error(
                "Error running custom metric %s: %s",
                self.name,
                str(e),
            )
            return []
        # Add prefix to ensure the name does not conflict with built-in metrics
        metric_name = schemas.CUSTOM_METRICS_PREFIX + self.name
        return [
            entities.MetricResult(
                metric_name=metric_name,
                metric_value=metric_value,
            )
        ]

    def __call__(self, *args, **kwargs):
        return self.eval_fn(*args, **kwargs)

    def _get_kwargs(self, eval_item: entities.EvalItem) -> Dict[str, Any]:
        # noinspection PyTypeChecker
        arg_spec = inspect.getfullargspec(self.eval_fn)

        full_args = _get_full_args_for_custom_metric(eval_item)
        # If the metric accepts **kwargs, pass all available arguments
        if arg_spec.varkw:
            return full_args
        kwonlydefaults = arg_spec.kwonlydefaults or {}
        required_args = arg_spec.args + [
            arg for arg in arg_spec.kwonlyargs if arg not in kwonlydefaults
        ]
        optional_args = list(kwonlydefaults.keys())
        accepted_args = required_args + optional_args
        # Validate that the dataframe can cover all the required arguments
        missing_args = set(required_args) - full_args.keys()
        if missing_args:
            raise TypeError(
                f"Dataframe is missing arguments {missing_args} to metric {self.name}"
            )
        # Filter the dataframe down to arguments that the metric accepts
        return {k: v for k, v in full_args.items() if k in accepted_args}


def agent_metric(eval_fn=None, *, name: Optional[str] = None):
    # noinspection PySingleQuotedDocstring
    '''
    Create a custom agent metric from a user-defined eval function.

    Can be used as a decorator on the eval_fn.

    The eval_fn should have the following signature:
        .. code-block:: python

            def eval_fn(
                *,
                request_id: str,
                request: Union[ChatCompletionRequest, str],
                response: Optional[Any],
                retrieved_context: Optional[List[Dict[str, str]]]
                expected_response: Optional[Any],
                expected_facts: Optional[List[str]],
                expected_retrieved_context: Optional[List[Dict[str, str]]],
                trace: Optional[mlflow.entities.Trace],
                **kwargs,
            ) -> Optional[Union[int, float, bool]]:
                """
                Args:
                    request_id: The ID of the request.
                    request: The agent's input from your input eval dataset.
                    response: The agent's raw output. Whatever we get from the agent, we will pass it here as is.
                    retrieved_context: Retrieved context, can be from your input eval dataset or from the trace,
                                       we will try to extract retrieval context from the trace;
                                       if you have custom extraction logic, use the `trace` field.
                    expected_response: The expected response from your input eval dataset.
                    expected_facts: The expected facts from your input eval dataset.
                    expected_retrieved_context: The expected retrieved context from your input eval dataset.
                    trace: The trace object. You can use this to extract additional information from the trace.
                """
    eval_fn will always be called with named arguments. You only need to declare the arguments you need.
    If kwargs is declared, all available arguments will be passed.

    The return value of the function should be either a number or a boolean. It will be used as the metric value.
    Return None if the metric cannot be computed.

    :param eval_fn: The user-defined eval function.
    :param name: The name of the metric. If not provided, the function name will be used.
    '''

    def decorator(fn, *, _name=name):
        # Use mlflow.metrics.make_metric to validate the metric name
        mlflow.metrics.make_metric(eval_fn=fn, greater_is_better=True, name=_name)
        metric_name = _name or fn.__name__

        # Validate signature of the fn
        arg_spec = inspect.getfullargspec(fn)
        if arg_spec.varargs:
            raise error_utils.ValidationError(
                "The eval_fn should not accept *args.",
            )
        return functools.wraps(fn)(CustomMetric(name=metric_name, eval_fn=fn))

    if eval_fn is not None:
        return decorator(eval_fn)

    return decorator
