"""Agents package."""

__all__ =   [
                # Model-based
                    # Learned Models
                    # Planning-based
                # Neurosymbolic
                    # NeuroSymbolic Inference Network
                # Policy-based
                    # Actor-Critic
                    # Gradient
                    # Modern Policy Optimization
                # Value-based
                    # Function Approximation
                    # Multi-Step Temporal Difference
                    # Tabular-based
                    "QLearningAgent",
                    "DoubleQLearningAgent",
                    "SARSAAgent",
                    "ExpectedSARSAAgent"
            ]

from agents.value_based   import *