from dataclasses import dataclass
from typing import Iterable, List, Tuple


class PreparedDataset:
    def __init__(self) -> None:
        pass


@dataclass
class HoldoutDataset(PreparedDataset):
    X_train: Iterable
    X_test: Iterable
    y_train: Iterable
    y_test: Iterable
