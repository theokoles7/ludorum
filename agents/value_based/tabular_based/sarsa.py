"""Implementation of SARSA agent as proposed in the 1994 paper "Online Q-Learning Using 
Connectionist Systems" by Rommery & Niranjan."""

__all__ = ["SARSAAgent"]

from typing                                     import override

from agents.value_based.tabular_based.__base__  import TabularBasedAgent

class SARSAAgent(TabularBasedAgent):
    """SARSA Agent class based on the 1994 paper, by Rommery & Niranjan.
    
    This agent is an on-policy temporal-difference control method.
    
    Link to paper: https://www.researchgate.net/profile/Mahesan-Niranjan/publication/2500611_On-Line_Q-Learning_Using_Connectionist_Systems/links/5438d5db0cf204cab1d6db0f/On-Line-Q-Learning-Using-Connectionist-Systems.pdf?_sg%5B0%5D=HYd0h230b7WOR6m4hj5yx01K97aS61Z0DufUURMQr9ZqMqcEVZ0dNpG84h6uCfRl_M40FNkXgRX-GnpnxH31Ww.jBF3fgrlhaJYs3bDEaHQU22nRpKP0zKeF_oOsqh7WddL8pfxAomPSbeANzdmLP9YPB26HbLeSaEJqhFgzIxvWQ&_sg%5B1%5D=CZtZhHTEMgSwBZrpZU_7BACd8RH04JUKiITdXRQJ6MQ9SFS27jreZmcsuNcqYYWRoxcwBE-xBMbrfl1QobmEZ65bmkmpzonq5JoLRIIUKXne.jBF3fgrlhaJYs3bDEaHQU22nRpKP0zKeF_oOsqh7WddL8pfxAomPSbeANzdmLP9YPB26HbLeSaEJqhFgzIxvWQ&_iepl=
    """

    @override
    def _update_(self) -> None:

        raise NotImplementedError(f"SARSA agent has not been implemented.")