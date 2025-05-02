"""Implementation of SARSA agent as proposed in the 1994 paper "Online Q-Learning Using 
Connectionist Systems" by Rommery & Niranjan."""

__all__ = ["SARSAAgent"]

from typing                                     import override

from agents.value_based.tabular_based.__base__  import TabularBasedAgent

class SARSAAgent(TabularBasedAgent):
    """SARSA Agent class based on the 1994 paper, by Rommery & Niranjan.
    
    This agent is an on-policy temporal-difference control method.
    
    Link to paper: https://www.researchgate.net/profile/Mahesan-Niranjan/publication/2500611_On-Line_Q-Learning_Using_Connectionist_Systems/links/5438d5db0cf204cab1d6db0f/On-Line-Q-Learning-Using-Connectionist-Systems.pdf?_sg%5B0%5D=HYd0h230b7WOR6m4hj5yx01K97aS61Z0DufUURMQr9ZqMqcEVZ0dNpG84h6uCfRl_M40FNkXgRX-GnpnxH31Ww.jBF3fgrlhaJYs3bDEaHQU22nRpKP0zKeF_oOsqh7WddL8pfxAomPSbeANzdmLP9YPB26HbLeSaEJqhFgzIxvWQ&_sg%5B1%5D=CZtZhHTEMgSwBZrpZU_7BACd8RH04JUKiITdXRQJ6MQ9SFS27jreZmcsuNcqYYWRoxcwBE-xBMbrfl1QobmEZ65bmkmpzonq5JoLRIIUKXne.jBF3fgrlhaJYs3bDEaHQU22nRpKP0zKeF_oOsqh7WddL8pfxAomPSbeANzdmLP9YPB26HbLeSaEJqhFgzIxvWQ&_iepl=
    
    SARSA (Modified Connectionist Q-Learning) Update Rule: 

        select next action rather than the next 'best' action

        Q(s, a) ← Q(s, a) + α [R + γ Q(s', a') - Q(s, a)]

    Vars:
        Q(s,a): Current Q-value for state-action pair (s,a)
        Q(s',a'): Next state-action pair Q-value
        α: learning rate
        R: reward
        γ: discount factor
        [R + γ Q(s', a') - Q(s, a)]: temporal difference error

    Args:
        state (list[int]): State of the agent before action being taken.
        action (int): Action chosen by agent.
        reward (float): Reward yielded by action taken.
        next_state (list[int]): State of the agent after action is taken.
        done (bool): Indicates if agent has reached end state.
    
    """

    @override
    def _update_(self,
        state:      tuple[int],
        action:     int,
        reward:     float,
        next_state: tuple[int],
        done:       bool
    ) -> None:

        # Log for debugging
        self.__logger__.debug(f"Updating Q-table[state: {state}, action: {action}]")

        # Choose next action (SARSA requirement) and define new action-state for Q-table
        # next_action will be of type int, like action param

        next_action = self._choose_action_(next_state) if not done else 0

        next_q_value = 0 if done else self._q_table_[next_state][next_action]

        # Update table based on SARSA rule
        self._q_table_[state + (action,)] += 
        self._learning_rate_ * (
            reward + self._discount_rate_ *
            next_q_value - self._q_table_[state][action]
        )