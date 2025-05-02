"""Implementation of Double Q-Learning agent as proposed in the 2010 paper "Double Q-Learning" by 
Hado van Hasselt."""

__all__ = ["DoubleQLearningAgent"]

from typing                                     import override

from agents.value_based.tabular_based.__base__  import TabularBasedAgent

class DoubleQLearningAgent(TabularBasedAgent):
    """Double Q-Learning agent class based on the original 2010 paper, by Hado van Hasselt.
    
    This agent is an off-policy TD control agent.
    
    Link to paper: https://proceedings.neurips.cc/paper_files/paper/2010/file/091d584fced301b442654dd8c23b3fc9-Paper.pdf
    """

    # Override the _init_ function to create a second Q-table for Double Q-learning
    @override
    def __init__(self,
        state_size:       tuple[int],
        action_size:      int,
        learning_rate:    float       = 0.1,
        discount_rate:    float       = 0.99,
        exploration_rate: float       = 1.0,
        **kwargs     
    ):
    
        # Inherit Q-table attributes from parent _init_ attributes
        super().__init__(
            state_size = state_size,
            action_size = action_size,
            learning_rate = learning_rate,
            discount_rate = discount_rate,
            exploration_rate = exploration_rate,
            **kwargs
        )

        # initialize q-values for tables A and B (Double Q-learning)

        # Q-table A (use existing Q-table)
        self._q_table_A = self._q_table_

        # Q-table B (define new Q-table)
        self._q_table_B = zeros(
            size = self._state_size_ + (self._action_size_,),
            dtype = float32
        )

    @override
    def _update_(self,
        state:      list[int],
        action:     int,
        reward:     float,
        next_state: list[int],
        done:       bool
    ) -> None:

        '''
        Update state based on the following rules for QA and QB:
        - QA(s, a) ← QA(s, a) + α [R + γ QB(s', argmax_a' QA(s', a')) - QA(s, a)]
        - QB(s, a) ← QB(s, a) + α [R + γ QA(s', argmax_a' QB(s', a')) - QB(s, a)]

        50% chance to update either table 

        Args:
            state (list[int]): State of the agent before action being taken.
            action (int): Action chosen by agent.
            reward (float): Reward yielded by action taken.
            next_state (list[int]): State of the agent after action is taken.
            done (bool): Indicates if agent has reached end state.
        
        '''

        # Log for debugging
        self.__logger__.debug(f"Updating Q-tables[state: {state}, action: {action}]")

        # Randomly choose to update QA or QB. QA < 0.5, QB >= 0.5
        if random.random() < 0.5:   # Updating Q-table A
            if done:
                next_q_value = 0
            else:
                # Find a* (Max Q-value in table A)
                a_star = argmax(self._q_table_A[next_state]).item()

                # Select next value from other Q-table (Table B) based on best action (a_star)
                next_q_value = self._q_table_B[next_state][a_star].item()


            # Update Q-table with Q-value for next state
            self._q_table_A[state][action] += self._learning_rate_ * (
                reward + self._discount_rate_ * next_q_value - self._q_table_A[state][action]
            )
        else:   # Updating Q-table B
            if done:
                next_q_value = 0
            else:
                # Find b* (Max Q-value in table B)
                b_star = argmax(self._q_table_B[next_state]).item()
                
                # Select next value from other Q-table (Table A) based on best action (b_star)
                next_q_value = self._q_table_A[next_state][b_star].item()


            # Update Q-table with Q-value for next state
            self._q_table_B[state][action] += self._learning_rate_ * (
                reward + self._discount_rate_ * next_q_value - self._q_table_B[state][action]
            )