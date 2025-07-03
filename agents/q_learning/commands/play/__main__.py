"""# ludorum.agents.q_learning.commands.play

Q-Learning game-play arbitration.
"""

from typing                     import Any, Dict, Optional

from agents.q_learning.__base__ import QLearning
from environments               import Environment, load_environment

def main(
    environment:    str,
    episodes:       Optional[int] = 100,
    max_steps:      Optional[int] = 100,
    **kwargs
) -> Dict[str, Any]:
    """# (Q-Learning) Play.
    
    Execute episodic game-play process with Q-Learning agent on specified environment.

    ## Args:
        * environment   (str):  Game being played.
        * episodes      (int):  Number of episodes for which agent will interact with environment. 
                                Defaults to 100.
        * max_steps     (int):  Maximum number of steps that agent is allowed to take during any 
                                given episode. Defaults to 100.

    ## Returns:
        * Dict[str, Any]:   Game-play results/statistics.
    """
    # Load environment.
    environment:    Environment =   load_environment(name = environment, **kwargs)
    
    # Instantiate agent.
    agent:          QLearning =     QLearning(
                                        action_space =      environment.action_space,
                                        observation_space = environment.observation_space,
                                        **kwargs
                                    )
    
    # For each prescribed episode...
    for episode in range(1, episodes + 1):
        
        # Set environment to initial state.
        state:          Any =   environment.reset()
        
        # Initialize episodic progress.
        done:           bool =  False
        episode_reward: float = 0.0
        step_count:     int =   0
        
        # Until environment reaches a terminal state...
        while not done and step_count < max_steps:
            
            # Select action based on state.
            action:     Any =   agent.act(state = state)
            
            # Interact with environment.
            new_state, reward, done, data = environment.step(action = action)
            
            # Observe new state.
            agent.observe(
                state =         state,
                action =        action,
                reward =        reward,
                next_state =    new_state,
                done =          done
            )
            
            # Update episodic progress.
            episode_reward  += reward
            step_count      += 1
            state           =  new_state
            
            # Display environment.
            print(environment)