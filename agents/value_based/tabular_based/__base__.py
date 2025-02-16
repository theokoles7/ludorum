"""Base implementation of tabluar, value-based agent."""

__all__ = ["TabularBasedAgent"]

from logging        import Logger

from numpy.random   import rand, randint
from torch          import argmax, float32, Tensor, zeros
from tqdm           import tqdm

from utils          import LOGGER

class TabularBasedAgent():
    """# Base class for tabular, value-based reinforcement learning agents.
    
    This class provides common functionality and attributes shared acros tabular agents such as 
    Q-Learning, SARSA, Monte Carlo Control, etc.
    
    ## Attributes:
        * _state_size_          (tuple[int]):   Dimensions of state space.
        * _action_size_         (int):          Number of possible actions.
        * _learning_rate_       (float):        Agent's learning rate for value updates.
        * _discount_rate_       (float):        Discount factor for future rewards.
        * _exploration_rate_    (float):        Exploration rate for epsilon-greedy policy.
        * _q_table_             (Tensor):       Q-table for storing state-action policies (action 
                                                qualities).
    """
    
    def __init__(self,
        state_size:         tuple[int],
        action_size:        int,
        learning_rate:      float           = 0.1,
        discount_rate:      float           = 0.99,
        exploration_rate:   float           = 1.0,
        **kwargs
    ):
        """# Initialize Tabular-Based agent.

        ## Args:
            * state_size        (tuple[int]):       Dimensions of state space.
            * action_size       (int):              Number of possible actions.
            * learning_rate     (float, optional):  Agent's learning rate for value updates. 
                                                    Defaults to 0.1.
            * discount_rate     (float, optional):  Discount factor for future rewards. Defaults to 
                                                    0.99.
            * exploration_rate  (float, optional):  Exploration rate for epsilon-greedy policy. 
                                                    Defaults to 1.0.
        """
        # Declare logger
        self.__logger__:            Logger =        LOGGER.getChild(self.__class__.__name__.lower())
        
        # Define agent attributes
        self._state_size_:          tuple[int] =    state_size
        self._action_size_:         int =           action_size
        self._learning_rate_:       float =         learning_rate
        self._discount_rate_:       float =         discount_rate
        self._exploration_rate_:    float =         exploration_rate
        
        # Initialize Q-Table
        self._q_table_:             Tensor =        zeros(
                                                        size = self._state_size_ + (self._action_size_,), 
                                                        dtype = float32
                                                    )
        
        # Log for debugging
        self.__logger__.debug(f"Agent initialized ({locals()})")
        
    def _choose_action_(self,
        state:  tuple[int, ...]
    ) -> int:
        """# Select an action using epsilon-greedy policy.

        ## Args:
            * state (tuple[int, ...]):  Current state of agent.

        ## Returns:
            * int:  Index of action chosen.
        """
        # Explore if exploration rate (epsilon) is higher than randomly chosen value
        if rand() < self._exploration_rate_: return randint(self._action_size_)
        
        # Otherwise, choose max quality from Q-table based on current state
        return argmax(self._q_table_[state]).item()
    
    def _decay_epsilon_(self,
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
        self._exploration_rate_ = max(self._exploration_rate_ * decay_rate, min_epsilon)
        
    def _train_(self,
        environment:    any,
        episodes:       int =   1000,
        max_steps:      int =   100,
        **kwargs
    ) -> dict[str, list]:
        """# Train Tabular-Based Agent on given environment.

        ## Args:
            * environment   (any):              Environment in which to train the agent.
            * episodes      (int, optional):    Prescribed training episodes. Defaults to 1000.
            * max_steps     (int, optional):    Maximum number of steps an agent can make within a 
                                                single episode. Defaults to 100.

        ## Returns:
            * dict:
                * rewards   (list): Rewards accrued during interaction with the environment.
        """
        # Log environment for debugging
        self.__logger__.debug(f"Environment prompt:\n{environment}")
        
        # Initialize rewards list
        results:    list =  {
                                "episodes": {},
                                "max":      {
                                                "max_reward":   -999,
                                                "steps_taken":  0
                                            }
                            }
        
        # Initialize progress bar
        with tqdm(
            total =     episodes,
            desc =      f"{self.__class__.__name__} training on {episodes} episodes",
            leave =     False,
            colour =    "magenta"
        ) as progress_bar:
            
            # For each episode prescribed...
            for episode in range(1, episodes + 1):
                
                # Update progress bar status
                progress_bar.set_postfix(text = f"Episode {episode}/{episodes}")
                
                # Reset environment
                state:          tuple[int, ...] =   environment.reset()
                
                # Reset reward
                total_reward:   int =               0
                
                # For each possible step the agent can make...
                for step in range(max_steps):
                    
                    # Choose an action for current state
                    action: int =   self._choose_action_(state = state)
                    
                    # Execute action
                    next_state, reward, done =   environment.step(action)
                    
                    # Update Q-Table
                    self._update_(
                        state =         state, 
                        action =        action, 
                        reward =        reward, 
                        next_state =    next_state, 
                        done =          done
                    )
                    
                    # Update total reward
                    total_reward += reward
                    
                    # Update current state
                    state = next_state
                    
                    # Break from episode if agent has reached end state
                    if done: break
                    
                # Update running maximum results if new record is achieved
                if total_reward > results["max"]["max_reward"]: results["max"].update({
                    "max_reward":   total_reward,
                    "steps_taken":  step
                })
                    
                # Append episode's reward to list
                results["episodes"].update({
                    episode:    {
                        "steps_taken":  step,
                        "reward":       total_reward
                    }
                })
                
                # Administer exploration rate (epsilon) decay
                self._decay_epsilon_()
                
                # Update progress bar
                progress_bar.update(1)
            
        return results
    
    def _update_(self,
        state:          tuple[int, ...],
        action:         int,
        reward:         float,
        next_state:     tuple[int, ...],
        done:           bool,
        **kwargs
    ) -> None:
        """# Update Q-value for given state-action pair.

        ## Args:
            * current_state (tuple[int, ...]):  State of agent before action is taken.
            * action        (int):              Action being taken.
            * reward        (float):            Reward yielded from action being taken.
            * next_state    (tuple[int, ...]):  State of agent after action is taken.
            * done          (bool):             Indactes if agent has reach end state.
        """
        raise NotImplementedError(f"Subclass must override method.")