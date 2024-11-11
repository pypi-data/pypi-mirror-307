from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Union
from relari.core.utils import check_type, type_hint_to_str
from typing_extensions import TypedDict

class Args(TypedDict):
    name: str
    typehint: Any


@dataclass(frozen=True)
class MetricArgs:
    base: Args
    ground_truth: Args

    def validate(self, data: List[Dict[str, Any]], with_optional: bool = False):
        for d, t in self.base.items():
            if d not in data:
                raise ValueError(f"Missing field: {d}")
            if not check_type(data[d], t):
                raise ValueError(
                    f"Invalid type for field {d}: expected {type_hint_to_str(t)} but found {type_hint_to_str(type(data[d]))}"
                )
        if with_optional:
            for d, t in self.ground_truth.items():
                if d not in data:
                    raise ValueError(f"Missing field: {d}")
                if not check_type(data[d], t):
                    raise ValueError(
                        f"Invalid type for field {d}: expected {type_hint_to_str(t)} but found {type_hint_to_str(type(data[d]))}"
                    )


@dataclass(frozen=True)
class MetricDef:
    name: str
    help: str
    args: MetricArgs

    @property
    def value(self):
        return self.name

    def validate(self, data: List[Dict[str, Any]], with_optional: bool = False):
        self.args.validate(data, with_optional)


class ToolCall(TypedDict):
    name: str
    kwargs: Dict[str, Any]


class Metric(Enum):
    SingleLabelClassification = (
        "SingleLabelClassification",
        MetricArgs(
            base={"predicted_class": Union[str, int, List[float]]},
            ground_truth={"ground_truth_class": Union[str, int]},
        ),
    )
    SQLASTSimilarity = (
        "SQLASTSimilarity",
        MetricArgs(
            base={"answer": str},
            ground_truth={"ground_truth_answers": Union[List[str], str]},
        ),
    )
    SQLSyntaxMatch = (
        "SQLSyntaxMatch",
        MetricArgs(
            base={"answer": str},
            ground_truth={"ground_truth_answers": Union[List[str], str]},
        ),
    )
    SQLCorrectness = (
        "SQLCorrectness",
        MetricArgs(
            base={"answer": str},
            ground_truth={"ground_truth_answers": Union[List[str], str]},
        ),
    )
    CodeStringMatch = (
        "CodeStringMatch",
        MetricArgs(
            base={"answer": str}, ground_truth={"ground_truth_answers": List[str]}
        ),
    )
    PythonASTSimilarity = (
        "PythonASTSimilarity",
        MetricArgs(
            base={"answer": str},
            ground_truth={"ground_truth_answers": Union[List[str], str]},
        ),
    )
    DeterministicFaithfulness = (
        "DeterministicFaithfulness",
        MetricArgs(
            base={"answer": str},
            ground_truth={"retrieved_context": Union[List[str], str]},
        ),
    )
    DeterministicAnswerCorrectness = (
        "DeterministicAnswerCorrectness",
        MetricArgs(
            base={"answer": str},
            ground_truth={"ground_truth_answers": Union[List[str], str]},
        ),
    )
    FleschKincaidReadability = (
        "FleschKincaidReadability",
        MetricArgs(base={"answer": str}, ground_truth=dict()),
    )
    PrecisionRecallF1 = (
        "PrecisionRecallF1",
        MetricArgs(
            base={"retrieved_context": List[str]},
            ground_truth={"ground_truth_context": List[str]},
        ),
    )
    PrecisionRecallF1Ext = (
        "PrecisionRecallF1Ext",
        MetricArgs(
            base={"retrieved_context": List[str]},
            ground_truth={"ground_truth_context": List[str]},
        ),
    )
    ChunkPrecisionRecallF1 = (
        "ChunkPrecisionRecallF1",
        MetricArgs(
            base={"retrieved_context": List[str]},
            ground_truth={"ground_truth_context": List[str]},
        ),
    )
    SentencePrecisionRecallF1 = (
        "SentencePrecisionRecallF1",
        MetricArgs(
            base={"retrieved_context": List[str]},
            ground_truth={"ground_truth_context": List[str]},
        ),
    )
    RankedRetrievalMetrics = (
        "RankedRetrievalMetrics",
        MetricArgs(
            base={"retrieved_context": List[str]},
            ground_truth={"ground_truth_context": List[str]},
        ),
    )
    TokenCount = (
        "TokenCount",
        MetricArgs(base={"retrieved_context": List[str]}, ground_truth=dict()),
    )
    TokenCount_o200k = (
        "TokenCount_o200k",
        MetricArgs(base={"retrieved_context": List[str]}, ground_truth=dict()),
    )
    ToolSelectionAccuracy = (
        "ToolSelectionAccuracy",
        MetricArgs(
            base={"tools": List[ToolCall]},
            ground_truth={"ground_truths": List[ToolCall]},
        ),
    )
    LLMBasedFaithfulness = (
        "LLMBasedFaithfulness",
        MetricArgs(base={"answer": str}, ground_truth={"question": str}),
    )
    LLMBasedAnswerCorrectness = (
        "LLMBasedAnswerCorrectness",
        MetricArgs(
            base={"answer": str},
            ground_truth={
                "question": str,
                "ground_truth_answers": Union[List[str], str],
            },
        ),
    )
    LLMBasedAnswerRelevance = (
        "LLMBasedAnswerRelevance",
        MetricArgs(base={"answer": str}, ground_truth={"question": str}),
    )
    LLMBasedStyleConsistency = (
        "LLMBasedStyleConsistency",
        MetricArgs(
            base={"answer": str},
            ground_truth={"ground_truth_answers": Union[List[str], str]},
        ),
    )
    LLMBasedContextPrecision = (
        "LLMBasedContextPrecision",
        MetricArgs(
            base={"retrieved_context": List[str]},
            ground_truth={
                "question": str,
            },
        ),
    )
    LLMBasedContextCoverage = (
        "LLMBasedContextCoverage",
        MetricArgs(
            base={"retrieved_context": List[str]},
            ground_truth={
                "question": str,
                "ground_truth_answers": Union[List[str], str],
            },
        ),
    )
    ProbabilisticCorrectness = (
        "ProbabilisticCorrectness",
        MetricArgs(
            base={"answer": str},
            ground_truth={
                "question": str,
                "ground_truth_answers": Union[List[str], str],
            },
        ),
    )
    Tone = (
        "Tone",
        MetricArgs(
            base={"answer": str},
            ground_truth={
                "question": str,
                "ground_truth_answers": Union[List[str], str],
            },
        ),
    )

    @staticmethod
    def PrecisionRecallF1AtK(k: int):
        metric = object.__new__(Metric)
        metric._value_ = f"PrecisionRecallF1AtK@{k}"
        metric.args = MetricArgs(
            base={"retrieved_context": List[str]},
            ground_truth={"ground_truth_context": List[str]},
        )
        return metric

    @staticmethod
    def PrecisionRecallF1AtK(k: int):
        metric = object.__new__(Metric)
        metric._value_ = f"PrecisionRecallF1AtK@{k}"
        metric.args = MetricArgs(
            base={"retrieved_context": List[str]},
            ground_truth={"ground_truth_context": List[str]},
        )
        return metric

    def __init__(self, value, args):
        self._value_ = value
        self.args = args

    @property
    def name(self):
        return self._value_


class SingleLabelClassification:
    def __init__(self, name, description):
        self.name = name
        self.description = description
