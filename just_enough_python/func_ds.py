from math import fabs
from typing import Callable, List

y_true = [1, 2, 3, 4, 5, 6, 7, 8, 0]
y_pred = [1, 2, 4, 5, 6, 9, 8, 3, 0]


def mae(y_true: List[int], y_pred: List[int]) -> float:
    return sum([fabs(t - p) for t, p in zip(y_true, y_pred)]) / len(y_true)


def mse(y_true: List[int], y_pred: List[int]) -> float:
    return sum([(t - p) ** 2 for t, p in zip(y_true, y_pred)]) / len(y_true)


def iou(y_true: List[int], y_pred: List[int]) -> float:
    return len(set(y_true) & set(y_pred)) / len(set(y_true) | set(y_pred))


def super_metric(
    fns: List[Callable[[List[int], List[int]], float]],
    weights: List[float],
    y_true: List[int],
    y_pred: List[int],
) -> float:
    total = sum(weights)

    return sum([fn(y_true, y_pred) * w for fn, w in zip(fns, weights)]) / total


scoring = {"mae": mae, "mean_absolute_error": mae, "mse": mse, "iou": iou}


def score(metric: str, y_true: List[int], y_pred: List[int]) -> float:
    fn = scoring.get(metric, mae)

    return fn(y_true, y_pred)


print(score("mse", y_pred, y_true))
print(score("mean_absolute_error", y_pred, y_true))
print(score("mahmut's favorite scoring machine", y_pred, y_true))
print(score("ahmet özal", y_pred, y_true))
print(score("iou", y_pred, y_true))

print(super_metric([mse, mae, iou], [1 / 3, 1 / 3, 1 / 3], y_pred, y_true))
