"""# ludorum.agents.q_learning

Implementation based on "Q-Learning" by Watkins & Dayan (1992).
Link to paper: https://link.springer.com/content/pdf/10.1007/BF00992698.pdf
"""

__all__ = ["QLearning"]

from logging                import Logger

from numpy                  import argmax, full, loadtxt, max, ndarray, savetxt, zeros
from numpy.random           import normal, rand, randint, uniform

from agents.__base__        import Agent
from utilities              import get_child

class QLearning(Agent):
    """# Q-Learning Agent.
    
    Q-Learning is an off-policy, tabular-based, value-based algorithm.
    
    Implementation based on "Q-Learning" by Watkins & Dayan (1992). Link to paper: 
    https://link.springer.com/content/pdf/10.1007/BF00992698.pdf
    """
    
    def __init__(self,
        action_space:       int,
        state_space:        tuple[int],
        learning_rate:      float =     0.1,
        discount_rate:      float =     0.99,
        exploration_rate:   float =     1.0,
        exploration_decay:  float =     0.99,
        exploration_min:    float =     0.01,
        bootstrap:          str =       "zeros",
        **kwargs
    ):
        """# Initialize Q-Learning Agent

        ## Args:
            * action_space      (int):              Number of possible actions that the agent can 
                                                    take.
            * state_space       (int):              Dimensions of the environment in which the 
                                                    agent will act.
            * learning_rate     (float, optional):  Controls how much new information overrides old 
                                                    information when updating Q-values. A higher 
                                                    learning rate means the agent learns faster, 
                                                    updating Q-values more significantly with new 
                                                    experiences. Conversely, a lower learning rate 
                                                    leads to more gradual updates, potentially 
                                                    stabilizing training but slowing down 
                                                    convergence. Defaults to 0.1.
            * discount_rate     (float, optional):  Determines the importance of future rewards. A 
                                                    factor of 0 will make the agent "myopic" (or 
                                                    short-sighted) by only considering current 
                                                    rewards, while a factor approaching 1 will make 
                                                    it strive for a long-term high reward. Defaults 
                                                    to 0.99.
            * exploration_rate  (float, optional):  Probability that the agent will choose a random 
                                                    action, rather than selecting the action that is 
                                                    believed to be optimal based on its current 
                                                    knowledge (i.e., the action with the highest 
                                                    Q-value). When set high, the agent is more 
                                                    likely to explore new actions. When low, the 
                                                    agent favors exploiting its current knowledge. 
                                                    Defaults to 1.0.
            * exploration_decay (float, optional):  Controls how quickly the exploration rate 
                                                    decreases over time. The exploration rate 
                                                    determines how often the agent selects random 
                                                    actions (explores) versus exploiting its learned 
                                                    knowledge (selecting the best action based on 
                                                    Q-values). A decay factor less than 1 (e.g., 
                                                    0.995) causes the exploration rate to gradually 
                                                    decrease, leading to more exploitation as the 
                                                    agent learns more about the environment. 
                                                    Defaults to 0.99.
            * exploration_min   (float, optional):  Specifies the minimum exploration rate that the 
                                                    agent will reach after the exploration decay 
                                                    process. This ensures that the agent does not 
                                                    completely stop exploring and retains a small 
                                                    chance to explore randomly, even in later 
                                                    stages of training. By setting a minimum value 
                                                    for exploration, the agent can still 
                                                    occasionally discover new actions, avoiding 
                                                    getting stuck in a local optimum. Defaults to 
                                                    0.01.
            * bootstrap         (str, optional):    Initialize Q-Table with specific values 
                                                    (defaults to "zeros"):
                                                    * zeros:        Common choice when you assume 
                                                                    that the agent has no prior 
                                                                    knowledge of the environment and 
                                                                    should learn everything from 
                                                                    scratch. All states and actions 
                                                                    start with equal value.
                                                    * random:       Useful when you want the agent 
                                                                    to start with some variability 
                                                                    in its Q-values and potentially 
                                                                    avoid any symmetry in the 
                                                                    learning process. It may help in 
                                                                    environments where different 
                                                                    actions in the same state can 
                                                                    have varying levels of 
                                                                    importance or expected rewards.
                                                    * small-random: Similar to random 
                                                                    initialization, but with smaller 
                                                                    values to prevent large, 
                                                                    unrealistic initial biases. 
                                                                    It's a good choice when you want 
                                                                    to start with some exploration 
                                                                    but without the extreme variance 
                                                                    that might come with large 
                                                                    random values.
                                                    * optimistic:   Used to encourage exploration by 
                                                                    making every state-action pair 
                                                                    initially appear to be 
                                                                    rewarding. Over time, the agent 
                                                                    will update these values based 
                                                                    on the actual rewards received.
        """
        # Declare logger.
        self.__logger__:            Logger =        get_child("q-learning")
        
        # Define environment components.
        self._state_space_:         int =           state_space
        self._action_space_:        int =           action_space
        
        # Define learning parameters.
        self._learning_rate_:       float =         learning_rate
        
        # Define discount parameters.
        self._discount_rate_:       float =         discount_rate
        
        # Define exploration parameters.
        self._exploration_rate_:    float =         exploration_rate
        self._exploration_decay_:   float =         exploration_decay
        self._exploration_min_:     float =         exploration_min
        
        # Initialize Q-Table.
        self._q_table_:             ndarray =       self.bootstrap_q_table(
                                                        states =    self._state_space_,
                                                        actions =   self._action_space_,
                                                        method =    bootstrap
                                                    )
        
        # Log for debugging.
        self.__logger__.debug(f"Initialized Q-Learning agent {locals()}")
        
    def bootstrap_q_table(self,
        states:     int,
        actions:    int,
        method:     str =   "zeros"
    ) -> ndarray:
        """# Initialize Q-Table
        
        ## Methods:
        * zeros:        Common choice when you assume that the agent has no prior knowledge of the 
                        environment and should learn everything from scratch. All states and actions 
                        start with equal value.
        * random:       Useful when you want the agent to start with some variability in its 
                        Q-values and potentially avoid any symmetry in the learning process. It may 
                        help in environments where different actions in the same state can have 
                        varying levels of importance or expected rewards.
        * small-random: Similar to random initialization, but with smaller values to prevent large, 
                        unrealistic initial biases. It's a good choice when you want to start with 
                        some exploration but without the extreme variance that might come with 
                        large random values.
        * optimistic:   Used to encourage exploration by making every state-action pair initially 
                        appear to be rewarding. Over time, the agent will update these values based 
                        on the actual rewards received.

        ## Args:
            * states    (int):              Number of states to track in table.
            * action    (int):              Number of actions to track in table.
            * method    (str, optional):    Method by which q-table values will be initialized. One 
                                            of "zeros", "random", "small-random", or "optimistic". 
                                            Defaults to "zeros".

        ## Returns:
            * ndarray:  Array of `states` x `actions` dimensions, initialized using method specified.
        """
        # Log action for debugging.
        self.__logger__.debug(f"Initializing {states}x{actions} Q-Table using {method} method.")
        
        # Match method.
        match method:
            
            # Zeros
            case "zeros":           return zeros(shape = (states, actions))
            
            # Random
            case "random":          return uniform(low = -1, high = 1, size = (states, actions))
            
            # Small Random
            case "small-random":    return normal(loc = 0, scale = 0.1, size = (states, actions))
            
            # Optimistic
            case "optimistic":      return full(shape = (states, actions), fill_value = 10)
            
            # Invalid Method Selection
            case _:                 raise ValueError(f"Invalid Q-Table initialization method provided: {method}")
    
    def decay_epsilon(self) -> None:
        """# Decay Exploration Rate
        
        Update exploration rate to be the maximum between the current rate decayed or the defined 
        minimum exploration rate value.
        """
        # Administer exploration rate decay.
        self._exploration_rate_:    float = max([
                                                # Decayed exploration rate.
                                                self._exploration_rate_ * self._exploration_decay_,
                                                
                                                # Exploration rate minimum.
                                                self._exploration_min_
                                            ])
        
        # Log action for debugging.
        self.__logger__.debug(f"Exploration rate updated to {self._exploration_rate_}")
        
    def load_model(self,
        path:   str
    ) -> None:
        """# Load Model
        
        Load agent's Q-table from file.

        ## Args:
            * path  (str):  Path at which model can be located/loaded.
        """
        # Log action for debugging.
        self.__logging__.debug(f"Loading q-table from {path}")
        
        # Save Q-table to file.
        self._q_table_: ndarray =   loadtxt(fname = path)  
        
    def save_model(self,
        path:   str
    ) -> None:
        """# Save Model
        
        Save agent's Q-table to file.

        ## Args:
            * path  (str):  Path at which model will be saved.
        """
        # Log action for debugging.
        self.__logging__.debug(f"Saving q-table to {path}")
        
        # Save Q-table to file.
        savetxt(fname = path, X = self._q_table_)  
        
    def select_action(self,
        state:  int
    ) -> int:
        """# Select Action
        
        Choose an action using epsilon-greedy policy.

        ## Args:
            * state (int):  Current state of agent.

        ## Returns:
            * int:  Index of action chosen.
        """
        # Explore if exploration rate (epsilon) is higher than randomly chosen value.
        if rand() < self._exploration_rate_: return randint(low = 0, high = self._action_space_)
        
        # Otherwise, choose max-value action from Q-table based on current state.
        return argmax(self._q_table_[state]).item()  
    
    def update(self,
        state:      int,
        action:     int,
        reward:     float,
        next_state: list[int],
        done:       bool
    ) -> None:
        """# Update Q-table
        
        Update agent's Q-Table based on following rule:
        
        Q(s, a) ← Q(s, a) + α [R + γ max_a Q(s', a) - Q(s, a)]
        
        Where:
            * α:                Learning rate (alpha)
            * γ:                Discount rate (gamma)
            * a:                Action submitted
            * s:                State when action was submitted
            * s':               State after action was taken
            * R:                Reward/penalty yielded by action taken
            * Q(s, a):          Current state:action value
            * max_a Q(s', a):   Maximum value for the next state over all possible actions

        ## Args:
            * state         (tuple[int]):   State of the agent before action being taken.
            * action        (int):          Action chosen by agent.
            * reward        (float):        Reward yielded by action taken.
            * next_state    (tuple[int]):   State of the agent after action is taken. 
            * done          (bool):         Indicates if agent has reached end state.
        """
        # Log for debugging.
        self.__logger__.debug(f"Updating Q-table[state: {state}, action: {action}, reward: {reward}]")
        
        # Define new action-state value in Q-table.
        self._q_table_[state, action] +=    (
                                                self._learning_rate_ * (
                                                    reward + (
                                                        (
                                                            self._discount_rate_ * 
                                                            0 if done else max(self._q_table_[next_state])
                                                        )
                                                    ) - self._q_table_[state][action]
                                                )
                                            )