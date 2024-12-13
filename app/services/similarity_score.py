
import numpy as np
from typing import Dict, List

from .schemas import ActualValueDtype, MetricReturnModel, EvaluationType
from .metric_names import METRICNAMES
from .utils import return_labels_binary
import logging

class SimilarityScore:
    """A base class for metrics."""
    @staticmethod
    def compression_score(
        ground_truths: List[str], predictions: List[str]
    ) -> List[float]:
        """Calculate the compression score for the given predictions and ground truth."""

        def _compression(t1, t2):
            return len(t1) / len(t2)

        return {
            "avg": np.round(
                np.mean(
                    [
                        _compression(pr, ref)
                        for ref, pr in zip(ground_truths, predictions)
                    ]
                ),
                3,
            )
        }