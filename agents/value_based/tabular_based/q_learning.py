"""Implementation of Q-Learning agent as proposed in the 1992 paper "Q-Learning" by Watkins & 
Dayan."""

__all__ = ["QLearningAgent"]

from typing                                     import override

from torch                                      import max

from agents.value_based.tabular_based.__base__  import TabularBasedAgent

class QLearningAgent(TabularBasedAgent):
    """Q-Learning Agent class based on the 1992 paper, by Watkins & Dayan.
    
    This agent is an off-policy temporal-difference control method.
    
    Link to paper: https://link.springer.com/content/pdf/10.1007/BF00992698.pdf
    """
    
    @override
    def _update_(self,
        state:      tuple[int],
        action:     int,
        reward:     float,
        next_state: tuple[int],
        done:       bool
    ) -> None:
        """# Update Q-table based on following rule:
        
        Q(s, a) ← Q(s, a) + α [R + γ max_a Q(s', a) - Q(s, a)]

        ## Args:
            * state         (tuple[int]):   State of the agent before action being taken.
            * action        (int):          Action chosen by agent.
            * reward        (float):        Reward yielded by action taken.
            * next_state    (tuple[int]):   State of the agent after action is taken. 
            * done          (bool):         Indicates if agent has reached end state.
        """
        # Log for debugging
        self.__logger__.debug(f"Updating Q-table[state: {state}, action {action}]")
        
        # Define new action-state value in Q-table
        self._q_table_[state][action] += self._learning_rate_ * (
            reward + (
                self._discount_rate_ * 0 if done else max(self._q_table_[next_state].item())
            ) - self._q_table_[state][action]
        )