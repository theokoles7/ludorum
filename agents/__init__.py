"""Ludorum agents package."""

__all__ =   [
                "Agent",
                "QLearning"
            ]

from agents.__base__    import Agent

from agents.q_learning  import QLearning