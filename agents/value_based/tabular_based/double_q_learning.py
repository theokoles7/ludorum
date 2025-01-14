"""Implementatio nof Double Q-Learning agent as proposed in the 2010 paper "Double Q-Learning" by 
Hado van Hasselt."""

__all__ = ["DoubleQLearningAgent"]

from typing                                     import override

from agents.value_based.tabular_based.__base__  import TabularBasedAgent

class DoubleQLearningAgent(TabularBasedAgent):
    """Double Q-Learning agent class based on the original 2010 paper, by Hado van Hasselt.
    
    This agent is an off-policy TD control agent.
    
    Link to paper: https://proceedings.neurips.cc/paper_files/paper/2010/file/091d584fced301b442654dd8c23b3fc9-Paper.pdf
    """

    @override
    def _update_(self) -> None:
        
        raise NotImplementedError(f"Double Q-Learning agent has not been implemented.")