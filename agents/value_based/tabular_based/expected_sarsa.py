"""Implementation of Expected SARSA agent as proposed in the 2009 paper "A Theoretical and Empirical 
Analysis of Expected SARSA" by Seijen et al."""

__all__ = ["ExpectedSARSAAgent"]

from typing                                     import override

from agents.value_based.tabular_based.__base__  import TabularBasedAgent

class ExpectedSARSAAgent(TabularBasedAgent):
    """Expected SARSA Agent class based on 2009 paper, by Seijen et al.
    
    This agent is an on-policy temporal-difference control method.
    
    Link to paper: https://www.ai.rug.nl/~mwiering/GROUP/ARTICLES/expected_sarsa.pdf


    Expected SARSA update rule:
        
        Q(s, a) ← Q(s, a) + α [R + γ ∑_a' π(s', a') Q(s', a') - Q(s, a)]


        Vars:
            Q(s, a): Current Q-value
            Q(s', a'): Next state-action pair
            α: learning rate
            R: reward after taking action s
            γ: discount rate
            ∑_a' π(s', a'): expected value of next state s' under policy π
                π: policy
                π(s', a'): Probability of taking action a' in state s' under policy π
            [R + γ ∑_a' π(s', a') Q(s', a') - Q(s, a)]: temporal difference error for Expected SARSA


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


        # Calculate expected Q-value
        if done:
            expected_q = 0 # No actions left to take (terminal)
        else:
            expected_q = 0 # Initialize expected_q for updating later

            # Find highest (max) Q-value in Q-table
            greedy_action = argmax(self._q_table_[next_state]).item() 

            for next_action in range(self.action_size_):
                if next_action == greedy_action:
                    # Greedy (highest Q-value): (1-ε) + ε/|A|
                    prob = (1 - self.exploration_rate_) + 
                           (self.exploration_rate_ / self.action_size_)
                else:
                    # If greedy action is not taken: ε/|A|
                    prob = self.exploration_rate_ / self.action_size_

                # Sum up Q-value probabilities
                expected_q += prob * self._q_table_[next_state][next_action]

        # Update Q-table
        self._q_table_[state][action] += 
            self._learning_rate_ * 
            (reward + self.discount_rate_ * expected_q - self._q_table_[state][action])
