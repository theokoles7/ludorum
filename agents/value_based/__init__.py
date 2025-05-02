"""Value-based Agents package."""

__all__ =   [
                # Function Approximation
                # Multi-Step Temporal Difference
                # Tabular-based
                "QLearningAgent"
                "DoubleQLearningAgent"
                "SARSAAgent"
                "ExpectedSARSAAgent"
            ]

from agents.value_based.function_approximation          import *
from agents.value_based.multi_step_temporal_difference  import *
from agents.value_based.tabular_based                   import *