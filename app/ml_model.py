import math
from typing import Dict


class SimpleLogisticModel:
    def __init__(self) -> None:
        self.bias = -0.3
        self.weights = {
            "feature_1": 0.8,
            "feature_2": -0.4,
        }

    def predict_proba(self, features: Dict[str, float]) -> float:
        z = self.bias
        for name, w in self.weights.items():
            z += w * features.get(name, 0)
        return 1 / (1 + math.exp(-z))

    def predict_class(self, features: Dict[str, float]) -> int:
        return int(self.predict_proba(features) >= 0.5)
