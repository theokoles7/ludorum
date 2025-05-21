"""Q-Learning Agent module.

Implementatino based on "Q-Learning" by Watkins & Dayan (1992).
Link to paper: https://link.springer.com/content/pdf/10.1007/BF00992698.pdf
"""

__all__ = ["QLearning"]

from logging            import Logger

from numpy              import argmax, float32, loadtxt, max, ndarray, savetxt, zeros
from numpy.random       import rand, randint
# from torch              import argmax
from tqdm               import tqdm

from agents.__base__    import Agent
from utilities.logger   import LOGGER

class QLearning(Agent):
    """# Q-Learning Agent.
    
    This agent is an off-policy temporal-difference control method.
    """
    
    def __init__(self,
        action_space:       int,
        state_space:        tuple[int],
        learning_rate:      float =     0.1,
        discount_rate:      float =     0.99,
        exploration_rate:   float =     1.0,
        **kwargs
    ):
        """# Initialize Q-Learning Agent.

        ## Args:
            * action_space      (int):              Number of possible actions that the agent can 
                                                    take.
            * state_space       (int):              Dimensions of the environment in which the 
                                                    agent will act.
            * learning_rate     (float, optional):  Agent's learning rate for value updates. 
                                                    Defaults to 0.1.
            * discount_rate     (float, optional):  Discount factor for future rewards. Defaults to 
                                                    0.99.
            * exploration_rate  (float, optional):  Exploration rate for epsilon-greedy policy. 
                                                    Defaults to 1.0.
        """
        # Declare logger.
        self.__logger__:            Logger =        LOGGER.getChild("q-learning")
        
        # Define agent attributes.
        self._state_space_:         int =           state_space
        self._action_space_:        int =           action_space
        self._learning_rate_:       float =         learning_rate
        self._discount_rate_:       float =         discount_rate
        self._exploration_rate_:    float =         exploration_rate
        
        # Initialize Q-Table.
        self._q_table_:             ndarray =       zeros(
                                                        shape = (self._state_space_, self._action_space_), 
                                                        dtype = float32
                                                    )
        
        # Log for debugging
        self.__logger__.debug(f"Initialized Q-Learning agent {locals()}")
        
    def act(self,
        state:  ndarray
    ) -> int:
        """# Select an action using epsilon-greedy policy.

        ## Args:
            * state (tuple[int, ...]):  Current state of agent.

        ## Returns:
            * int:  Index of action chosen.
        """
        # Explore if exploration rate (epsilon) is higher than randomly chosen value.
        if rand() < self._exploration_rate_: return randint(low = 0, high = self._action_space_)
        
        # Otherwise, choose max quality from Q-table based on current state.
        return argmax(self._q_table_[state]).item()
    
    def decay_epsilon(self,
        decay_rate:     float = 0.99,
        min_epsilon:    float = 0.01
    ) -> None:
        """# Decay exploration rate (epsilon) over time.

        ## Args:
            * decay_rate    (float, optional):  Rate at which exploration rate (epsilon) should 
                                                decay. Defaults to 0.99.
            * min_epsilon   (float, optional):  Minimum value for exploration rate (epsilon). 
                                                Defaults to 0.01.
        """
        self._exploration_rate_ = max([self._exploration_rate_ * decay_rate, min_epsilon])
        
    def load_model(self,
        path:   str
    ) -> None:
        """# Load agent's model from file.

        ## Args:
            * path  (str):  Path at which model can be located/loaded.
        """
        # Save Q-table to file.
        self._q_table_: ndarray =   loadtxt(fname = path)  
        
    def save_model(self,
        path:   str
    ) -> None:
        """# Save agent's model to file.

        ## Args:
            * path  (str):  Path at which model will be saved.
        """
        # Save Q-table to file.
        savetxt(fname = path, X = self._q_table_)        
        
    def _train_(self,
        environment:    any,
        episodes:       int =   100,
        max_steps:      int =   100,
        **kwargs
    ) -> dict[str, list]:
        """# Train agent on given environment.

        ## Args:
            * environment   (any):              Environment in which to train the agent.
            * episodes      (int, optional):    Prescribed training episodes. Defaults to 100.
            * max_steps     (int, optional):    Maximum number of steps an agent can make within a 
                                                single episode. Defaults to 100.

        ## Returns:
            * dict:
                * rewards   (list): Rewards accrued during interaction with the environment.
        """
        # Log environment for debugging.
        self.__logger__.debug(f"Environment prompt:\n{environment}")
        
        # Initialize training report.
        results:    dict =  {
                                "episodes": {},
                                "results":  {
                                                "max_reward":   -999,
                                                "steps_taken":  0,
                                                "episode":      0
                                            }
                            }
        
        # Initialize progress bar.
        with tqdm(
            total =     episodes,
            desc =      f"{self.__class__.__name__} training on {episodes} episodes",
            leave =     False,
            colour =    "magenta"
        ) as progress_bar:
            
            # For each episode prescribed...
            for episode in range(1, episodes + 1):
                
                # Update progress bar status.
                progress_bar.set_postfix(text = f"Episode {episode}/{episodes}")
                
                # Reset environment.
                state:          ndarray =   environment.reset()
                
                # Reset reward.
                total_reward:   int =       0
                
                # For each possible step the agent can make...
                for step in range(max_steps):
                    
                    # Choose an action for current state.
                    action: int =   self.act(state = state)
                    
                    # Execute action.
                    next_state, reward, done =   environment.step(action)
                    
                    # Update Q-Table.
                    self.update(
                        state =         state, 
                        action =        action, 
                        reward =        reward, 
                        next_state =    next_state, 
                        done =          done
                    )
                    
                    # Update total reward.
                    total_reward += reward
                    
                    # Update current state.
                    state =         next_state
                    
                    # Break from episode if agent has reached end state.
                    if done: break
                    
                # Update running maximum results if new record is achieved.
                if total_reward > results["results"]["max_reward"]: results["results"].update({
                                                                    "max_reward":   total_reward,
                                                                    "steps_taken":  step,
                                                                    "episode":      episode
                                                                })
                    
                # Append episode's reward to list.
                results["episodes"].update({
                                        episode:    {
                                            "steps_taken":  step,
                                            "reward":       total_reward
                                        }
                                    })
                
                # Administer exploration rate (epsilon) decay.
                self.decay_epsilon()
                
                # Update progress bar.
                progress_bar.update(1)
            
        # Return results to parent process.
        return results
    
    def update(self,
        state:      int,
        action:     int,
        reward:     float,
        next_state: list[int],
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
        self.__logger__.debug(f"Updating Q-table[state: {state}, action: {action}, reward: {reward}]")
        
        # Define new action-state value in Q-table
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