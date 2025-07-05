"""# ludorum.agents.q_learning.commands.play

Q-Learning game-play arbitration.
"""

from time                       import sleep
from typing                     import Any, Dict, Optional

from dashing                    import HSplit, Log, Text, VSplit

from agents.q_learning.__base__ import QLearning
from environments               import Environment, load_environment

def main(
    environment:    str,
    episodes:       Optional[int] = 100,
    max_steps:      Optional[int] = 100,
    animate:        bool =          False,
    animation_rate: float =         0.1,
    **kwargs
) -> Dict[str, Any]:
    """# (Q-Learning) Play.
    
    Execute episodic game-play process with Q-Learning agent on specified environment.

    ## Args:
        * environment       (str):      Game being played.
        * episodes          (int):      Number of episodes for which agent will interact with 
                                        environment. Defaults to 100.
        * max_steps         (int):      Maximum number of steps that agent is allowed to take during 
                                        any given episode. Defaults to 100.
        * animate           (bool):     Animate agent interaction with the environment.
        * animation_rate    (float):    Rate at which animation will be refreshed in seconds. 
                                        Defaults to 0.1 seconds.

    ## Returns:
        * Dict[str, Any]:   Game-play results/statistics.
    """
    # Load environment.
    environment:        Environment =       load_environment(name = environment, **kwargs)
    
    # Instantiate agent.
    agent:              QLearning =         QLearning(
                                                action_space =      environment.action_space,
                                                observation_space = environment.observation_space,
                                                **kwargs
                                            )
    
    # Initialize game statistics.
    game_statistics:    Dict[str, Any] =    {
                                                "episodes": {},
                                                "best":     {
                                                                "reward":   0.0,
                                                                "episode":  0
                                                            }
                                            }
    
    # For each prescribed episode...
    for episode in range(1, episodes + 1):
        
        # Execute episode.
        episode_statistics: Dict[str, Any] =    _execute_episode_(
                                                    agent =             agent,
                                                    environment =       environment,
                                                    max_steps =         max_steps,
                                                    animate =           animate,
                                                    animation_rate =    animation_rate
                                                )
            
        # Record episode statistics.
        game_statistics["episodes"].update({episode: episode_statistics})
        
        # If episode reward record is achieved...
        if episode_statistics["reward"] > game_statistics["best"]["reward"]:
            
            # Update record.
            game_statistics["best"]["reward"] =     episode_statistics["reward"]
            game_statistics["best"]["episode"] =    episode
        
    from json import dump
    dump(game_statistics, open("game_statistics.json", "w"), indent = 2, default = str)
        
    # Return results.
    return game_statistics

# HELPERS ==========================================================================================

def _execute_episode_(
    agent:          QLearning,
    environment:    Environment,
    max_steps:      int,
    animate:        bool =          False,
    animation_rate: float =         0.1,
) -> Dict[str, Any]:
    """# Execute Episode.

    ## Args:
        * agent             (QLearning):    Agent interacting with environment.
        * environment       (Environment):  Environment with which agent is interacting.
        * max_steps         (int):          Maximum number of steps that agent is allowed to take 
                                            during episode.
        * animate           (bool):         Animate agent interaction with the environment.
        * animation_rate    (float):        Rate at which animation will be refreshed in seconds. 
                                            Defaults to 0.1 seconds.

    ## Returns:
        * Dict[str, Any]:
            * reward:       Total reward accumulated during episode.
            * steps_taken:  Total number of steps taken during episode.
            * completed:    True if agent was able to reach a terminal state. False if maximum step 
                            count was reached.
            * steps:        Dictionary of individual step data.
    """
    # Initialize animation layout if specified.
    panel_layout:       VSplit =            _init_animation_layout_(environment = environment.name)
    env_panel, stats_panel, log_panel =     panel_layout.items[0].items
    
    # Initialize episode statistics.
    episode_statistics: Dict[str, Any] =    {
                                                "reward":       0.0,
                                                "steps_taken":  0,
                                                "completed":    False,
                                                "steps":        {}
                                            }
    
    # Set environment to initial state.
    state:          Any =   environment.reset()
            
    # For each possible step...
    for step in range(1, max_steps + 1):
        
        # Select action based on state.
        action:     Any =   agent.act(state = state)
        
        # Interact with environment.
        reward, new_state, done, data = environment.step(action = action)
        
        # Observe new state.
        agent.observe(
            state =         state,
            action =        action,
            reward =        reward,
            next_state =    new_state,
            done =          done
        )
        
        # Update episodic progress.
        episode_statistics["reward"]        += reward
        episode_statistics["steps_taken"]   += 1
        episode_statistics["completed"]     =  done
        
        # Record step statistics.
        episode_statistics["steps"].update({step: {
                                                    "old_state":    state,
                                                    "new_state":    new_state,
                                                    "reward":       reward,
                                                    "done":         done,
                                                    "data":         data
                                            }})
        
        # If animation is specified...
        if animate:
            
            # Update environment rendering.
            env_panel.text =    str(environment)
            
            # Update statistics panel.
            stats_panel.text =  f"Step:\t{step}\nReward:\t{reward}\nTotal Reward:\t{episode_statistics["reward"]}"
            
            # Update logging panel.
            log_panel.append(data["event"])
            
            # Update display.
            panel_layout.display()
            
            # Simulate refresh rate.
            sleep(animation_rate)
        
        # If terminal state is reached, episode concludes.
        if done: return episode_statistics
        
        # Updated state.
        state = new_state
        
    # Provide episode statistics.
    return episode_statistics

def _init_animation_layout_(
    environment:    str
) -> VSplit:
    """# Initialize Panel Layout.
    
    ## Args:
        * environment   (str):  Name of environment that agent is interacting with.

    ## Returns:
        * VSplit:   Panel layout.
    """
    return  VSplit(
                HSplit(
                    Text("", title = "Environment", border_color = 1, color = 7),
                    Text("", title = "Statistics",  border_color = 2, color = 7),
                    Log( "", title = "Events",      border_color = 4, color = 7),
                    title =         f"Q-Learning Agent Playing {environment.capitalize()}",
                    border_color =  7
                )
            )