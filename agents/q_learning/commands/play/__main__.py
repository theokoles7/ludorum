"""# ludorum.agents.q_learning.commands.play.main

Q-Learning game-play arbitration.
"""

from json                       import dumps
from math                       import inf
from time                       import sleep
from typing                     import Any, Dict, Optional

from dashing                    import HSplit, Log, Text, VSplit

from agents.q_learning.__base__ import QLearning
from environments               import Environment, load_environment

class Game():
    """# Game (Process).
    
    Process execution for Q-Learning agent game-play.
    """
    
    def __init__(self,
        environment:    str,
        episodes:       Optional[int] = 100,
        max_steps:      Optional[int] = 100,
        animate:        bool =          False,
        animation_rate: float =         0.1,
        **kwargs
    ) -> Dict[str, Any]:
        """# Initialize Game.

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
        # Instantiate environment.
        self._environment_:     Environment =   load_environment(name = environment, **kwargs)
        
        # Instantiate agent.
        self._agent_:           QLearning =     QLearning(
                                                    action_space =      self._environment_.action_space,
                                                    observation_space = self._environment_.observation_space,
                                                    **kwargs
                                                )
        
        # Define game parameters.
        self._episodes_:        int =           episodes
        self._max_steps_:       int =           max_steps
        
        # Define animation parameters.
        self._animate_:         bool =          animate
        self._animation_rate_:  float =         animation_rate
        
        # Intialize panel layout if animation is enabled.
        if animate: self._init_layout_()
        
    # METHODS ======================================================================================
    
    def execute(self) -> Dict[str, Any]:
        """# Execute Game.

        ## Returns:
            * Dict[str, Any]:   Game data.
        """
        # Initialize game statistics.
        game_statistics:    Dict[str, Any] =    {
                                                    "episodes": {},
                                                    "best":     {
                                                                    "reward":   -inf,
                                                                    "episode":  0
                                                                }
                                                }
        
        # For each prescribed episode...
        for episode in range(1, self._episodes_ + 1):
                
            # If animation is enabled...
            if self._animate_:
                
                # Update UI renderings.
                self._update_game_stats_(game_statistics = game_statistics)
            
            # Set current episode.
            self._current_episode_: int =   episode
            
            # Execute episode.
            game_statistics["episodes"].update({episode: self._execute_episode_(episode = episode)})
            
            # If new reward record was achieved...
            if game_statistics["episodes"][episode]["reward"] > game_statistics["best"]["reward"]:
                
                # Update record.
                game_statistics["best"]["reward"] =     game_statistics["episodes"][episode]["reward"]
                game_statistics["best"]["episode"] =    episode
                
        # Return game statistics.
        return game_statistics
        
    # HELPERS ======================================================================================
    
    def _append_event_(self,
        event:  str
    ) -> None:
        """# Append Event.
        
        Append event to log panel.

        ## Args:
            * event (str):  Event being appended.
        """
        self._log_panel_.append(event)
    
    def _execute_episode_(self,
        episode:    int
    ) -> Dict[str, Any]:
        """# Execute Episode.
        
        ## Args:
            * episode   (int):  Current episode.

        ## Returns:
            * Dict[str, Any]:   Episode data.
        """
        # Set environment to initial state.
        state:              Any =               self._environment_.reset()
        
        # Initialize episode statistics.
        episode_statistics: Dict[str, Any] =    {
                                                    "steps":        {},
                                                    "reward":       0.0,
                                                    "steps_taken":  0,
                                                    "completed":    False
                                                }
        
        # For each allowed step...
        for step in range(1, self._max_steps_ + 1):
            
            # Select action based on state.
            action: int =                       self._agent_.act(state = state)
            
            # Interact with environment.
            reward, new_state, done, data =     self._environment_.step(action = action)
            
            # Execute step.
            episode_statistics["steps"].update({step:   {
                                                            "old_state":    state,
                                                            "new_state":    new_state,
                                                            "reward":       reward,
                                                            "done":         done,
                                                            "data":         data
                                                        }})
            
            # Update running statistics.
            episode_statistics["steps_taken"]   +=  1
            episode_statistics["reward"]        +=  episode_statistics["steps"][step]["reward"]
            episode_statistics["completed"]      =  episode_statistics["steps"][step]["done"]
            
            # If animation is enabled...
            if self._animate_:
                
                # Update UI renderings.
                self._render_environment_()
                self._append_event_(event = f"Took action {action} and {episode_statistics["steps"][step]["data"]["event"]}")
                self._update_episode_stats_(episode_statistics = episode_statistics)
                self._ui_.display()
                
                # Simulate refresh rate.
                sleep(self._animation_rate_)
            
            # If agent reached terminal state, then episode concludes.
            if episode_statistics["steps"][step]["done"]: break
            
            # Update current state.
            state:  Any =                       new_state
            
        # Return episode statistics.
        return episode_statistics
        
    def _init_layout_(self) -> None:
        """# Initialize Panel Layout."""
        # Define layout.
        self._ui_:  VSplit =    VSplit(
                                    HSplit(
                                        Text("", title = "Environment", border_color = 7, color = 7),
                                        VSplit(
                                            Text("", title = "Game",    border_color = 7, color = 7),
                                            Text("", title = "Episode", border_color = 7, color = 7),
                                            title = "Statistics", border_color = 7, color = 7
                                        ),
                                        Log(title = "Events",      border_color = 7, color = 7),
                                        title = f"Q-Learning playing {self._environment_.name}", border_color = 7, color = 7
                                    )
                                )
        
        # Extract components.
        self._env_panel_:           Text =  self._ui_.items[0].items[0]
        self._game_stats_panel_:    Text =  self._ui_.items[0].items[1].items[0]
        self._episode_stats_panel_: Text =  self._ui_.items[0].items[1].items[1]
        self._log_panel_:           Log =   self._ui_.items[0].items[2]
        
    def _render_environment_(self) -> None:
        """# Render Environment.

        Update environment rendering.
        """
        if self._animate_: self._env_panel_.text = str(self._environment_)
        
    def _update_episode_stats_(self,
        episode_statistics: Dict[str, Any]
    ) -> None:
        """# Update Episode Statistics Panel.

        ## Args:
            * episode_statistics    (Dict[str, Any]):   Current episode statistics.
        """
        self._episode_stats_panel_.title =  f"Episode {self._current_episode_}/{self._episodes_}"
        self._episode_stats_panel_.text =   dumps(
                                                {k:v for k, v in episode_statistics.items() if k != "steps"},
                                                indent =    2,
                                                default =   str
                                            )
        
    def _update_game_stats_(self,
        game_statistics:    Dict[str, Any]
    ) -> None:
        """# Update Game Stiatistics Panel.

        ## Args:
            * game_statistics   (Dict[str, Any]):   Current game statistics.
        """
        self._game_stats_panel_.text =  dumps(
                                            {k:v for k, v in game_statistics.items() if k != "episodes"},
                                            indent =    2,
                                            default =   str
                                        )
        
# Define main process driver.
def main(**kwargs) -> Dict[str, Any]:
    """# Execute Game.

    ## Returns:
        * Dict[str, Any]:   Game statistics.
    """
    # Execute game.
    return Game(**kwargs).execute()