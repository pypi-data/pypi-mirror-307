from typing import Any, Dict, List, Optional


def accuracy_score(y_true: List[int], y_pred: List[int]) -> float:
    """Calculate the accuracy score."""
    if len(y_true) != len(y_pred):
        raise ValueError("Length of y_true and y_pred must be the same")
    correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    return correct / len(y_true)


def precision_score(
    y_true: List[int],
    y_pred: List[int],
    average: str = "micro",
    zero_division: float = 1.0,
) -> float:
    """Calculate the precision score."""
    if average not in ["micro", "macro"]:
        raise ValueError("Average must be either 'micro' or 'macro'")

    classes = sorted(set(y_true + y_pred))
    precisions = []

    for cls in classes:
        true_positives = sum(1 for t, p in zip(y_true, y_pred) if t == cls and p == cls)
        predicted_positives = sum(1 for p in y_pred if p == cls)

        if predicted_positives == 0:
            precisions.append(zero_division)
        else:
            precisions.append(true_positives / predicted_positives)

    if average == "micro":
        return sum(precisions) / len(precisions)
    else:  # macro
        return sum(precisions) / len(classes)


def recall_score(
    y_true: List[int],
    y_pred: List[int],
    average: str = "micro",
    zero_division: float = 1.0,
) -> float:
    """Calculate the recall score."""
    if average not in ["micro", "macro"]:
        raise ValueError("Average must be either 'micro' or 'macro'")

    classes = sorted(set(y_true + y_pred))
    recalls = []

    for cls in classes:
        true_positives = sum(1 for t, p in zip(y_true, y_pred) if t == cls and p == cls)
        actual_positives = sum(1 for t in y_true if t == cls)

        if actual_positives == 0:
            recalls.append(zero_division)
        else:
            recalls.append(true_positives / actual_positives)

    if average == "micro":
        return sum(recalls) / len(recalls)
    else:  # macro
        return sum(recalls) / len(classes)


def f1_score(
    y_true: List[int],
    y_pred: List[int],
    average: str = "micro",
    zero_division: float = 1.0,
) -> float:
    """Calculate the F1 score."""
    precision = precision_score(y_true, y_pred, average, zero_division)
    recall = recall_score(y_true, y_pred, average, zero_division)

    if precision + recall == 0:
        return zero_division
    else:
        return 2 * (precision * recall) / (precision + recall)


def aggregate_classification_results(
    results: List[Dict[str, Any]],
    classes: Optional[List[str]] = None,
    average: str = "micro",
) -> Dict[str, Any]:
    """
    Aggregate classification results from multiple workers.
    """
    if classes is None:
        classes = set(r["classification_prediction"] for r in results)
        classes.update(set(r["classification_ground_truth"] for r in results))
        classes = sorted(classes)
    else:
        classes = classes
    class_to_index = {c: i for i, c in enumerate(classes)}
    pred = [class_to_index[r["classification_prediction"]] for r in results]
    gt = [class_to_index[r["classification_ground_truth"]] for r in results]
    return {
        "accuracy": accuracy_score(gt, pred),
        "precision": precision_score(gt, pred, average=average, zero_division=1.0),  # type: ignore
        "recall": recall_score(gt, pred, average=average, zero_division=1.0),  # type: ignore
        "f1": f1_score(gt, pred, average=average, zero_division=1.0),  # type: ignore
    }
