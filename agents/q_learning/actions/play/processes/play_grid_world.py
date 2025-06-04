"""# ludorum.agents.q_learning.actions.processes.play_grid_world

Define the process by which the Q-Learning agent will interact with the Grid World environment.
"""

__all__ = ["main"]

from argparse                           import Namespace
from logging                            import Logger
from os                                 import name, system
from time                               import sleep

from numpy                              import ndarray
from tqdm                               import tqdm

from agents.q_learning.__base__         import QLearning
from environments.grid_world.__base__   import GridWorld
from utilities                          import get_child
        
def main(
    episodes:   int =   100,
    max_steps:  int =   100,
    animate:    bool =  False,
    **kwargs
) -> dict[str, list]:
    """# Execute Q-Learning Game Play.

    ## Args:
        * episodes  (int, optional):    Number of episodes for which game play will repeat. Defaults 
                                        to 100.
        * max_steps (int, optional):    Maximum number of interations that the agent is allowed to
                                        make with te environment during each episode. Defaults to 
                                        100.
        * animate   (bool, optional):   Render animation of agent interacting with environment.
    """
    # Initialize logger.
    __logger__:     Logger =    get_child("q-learning.play-grid-world")
    
    # Initialize Grid World environment.
    _environment_:  GridWorld = GridWorld(**kwargs)
    
    # Log environment for debugging.
    __logger__.debug(f"Environment prompt:\n{_environment_}")
    
    # Initialize Q-Learning agent.
    _agent_:        QLearning = QLearning(
                                    action_space =  _environment_.action_space(),
                                    state_space =   _environment_.state_space(),
                                    **kwargs
                                )
    
    # Initialize holistic game report.
    game_results:   dict =      {
                                    "episodes": {},
                                    "results":  {
                                                    "max_reward":   -999,
                                                    "steps_taken":  0,
                                                    "episode":      0
                                                }
                                }
    
    # Reference process parameters.
    episodes:   int =   episodes
    max_steps:  int =   max_steps
    
    # Initialize progress bar.
    with tqdm(
        total =     episodes,
        desc =      f"Q-Learning training on {episodes} episodes",
        leave =     False,
        colour =    "magenta"
    ) as progress_bar:
        
        # For each episode prescribed...
        for episode in range(1, episodes + 1):
    
            # Initialize episodic report.
            episode_results:   dict =  {
                                    "steps":        {},
                                    "steps_taken":  0,
                                    "score":        0,
                                    "metrics":      {}
                                }
            
            # Update progress bar status.
            progress_bar.set_postfix(text = f"Episode {episode}/{episodes}")
            
            # Reset environment.
            state:          ndarray =   _environment_.reset()
            
            # Reset reward.
            total_reward:   float =     0.0
            
            # For each possible step the agent can make...
            for step in range(1, max_steps + 1):
                
                # Choose an action for current state.
                action: int =   _agent_.select_action(state = state)
                
                # Execute action.
                next_state, reward, done, meta =   _environment_.step(action)
                
                # Update Q-Table.
                _agent_.update(
                    state =         state, 
                    action =        action, 
                    reward =        reward, 
                    next_state =    next_state, 
                    done =          done
                )
                
                __logger__.debug(f"Current environment state:\n{_environment_}")
                
                # Update total reward.
                total_reward += reward
    
                # Append step data.
                episode_results["steps"].update({step: {
                                                "action":           action,
                                                "reward":           reward,
                                                "done":             done,
                                                "previous_state":   state,
                                                "current_state":    next_state,
                                                "metrics":          meta
                                            }})
                
                # Update current state.
                state =         next_state
                
                # Update episode's step counter.
                episode_results["steps_taken"] += 1
                
                # If animation if enabled...
                if animate:
                    
                    # Clear terminal.
                    system("clear" if name != "nt" else "cls")
                    
                    # Display environment.
                    print(_environment_)
                    
                    # Display index.
                    print(f"""\nGAME\n----\n{"Episode:":22} {episode}/{episodes}\n{"Step:":22} {step}/{max_steps}\n{"Reward:":22} {_environment_._cumulative_reward_}""")
                    
                    # Print agent attributes.
                    print("\nAGENT\n-----")
                    print(f"""{"Epsilon:":22} {_agent_._exploration_rate_}\n{"Alpha:":22} {_agent_._learning_rate_}\n{"Gamma:":22} {_agent_._discount_rate_}""")
                    
                    # Display statistics.
                    print("\nMETADATA\n--------")
                    for k, v in _environment_.metadata().items(): print(f"""{f"{k}:":22} {v}""")
                    
                    # Pause for a split second to simulate real time animation.
                    sleep(0.1)
                
                # Break from episode if agent has reached end state.
                if done: break
            
                # Administer exploration rate (epsilon) decay.
                _agent_.decay_epsilon()
                
            # Update running maximum results if new record is achieved.
            if total_reward > game_results["results"]["max_reward"]:    game_results["results"].update({
                                                                            "max_reward":   total_reward,
                                                                            "steps_taken":  step,
                                                                            "episode":      episode
                                                                        })
            
            # Update episodic results.
            episode_results["score"] =      total_reward
            episode_results["metrics"] =    meta
                
            # Append episode's reward to list.
            game_results["episodes"].update({episode: episode_results})
            
            # Update progress bar.
            progress_bar.update(1)
        
    # Return results to parent process.
    return game_results