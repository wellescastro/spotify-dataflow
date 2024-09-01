from dataclasses import dataclass


@dataclass
class OutcomeMetrics:
    accuracy: float
    f1_score: float
    precision: float
    recall: float
