"""Implementation of Expected SARSA agent as proposed in the 2009 paper "A Theoretical and Empirical 
Analysis of Expected SARSA" by Seijen et al."""

__all__ = ["ExpectedSARSAAgent"]

from typing                                     import override

from agents.value_based.tabular_based.__base__  import TabularBasedAgent

class ExpectedSARSAAgent(TabularBasedAgent):
    """Expected SARSA Agent class based on 2009 paper, by Seijen et al.
    
    This agent is an on-policy temporal-difference control method.
    
    Link to paper: https://www.ai.rug.nl/~mwiering/GROUP/ARTICLES/expected_sarsa.pdf
    """

    @override
    def _update_(self) -> None:

        raise NotImplementedError(f"Expected SARSA agent has not been implemented.")