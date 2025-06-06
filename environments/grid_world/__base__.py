"""Gird World game implementation."""

__all__ = ["GridWorld"]

from logging                import Logger
from os                     import name, system
from time                   import sleep

from termcolor              import colored

from environments.__base__  import Environment
from utilities.logger       import get_child

class GridWorld(Environment):
    """# Grid World.
    
    Discrete, deterministic grid environment.
    
    ## Space Definitions:
        * State Space:  Discrete(rows * columns)
        * Action Space: Discrete(4) = {0=DOWN, 1=UP, 2=LEFT, 3=RIGHT}
    """
    
    def __init__(self,
        # Dimensions
        rows:           int =                           4,
        columns:        int =                           4,
        # Grid Features
        goal:           tuple[int] =                    None,
        start:          tuple[int] =                    (0, 0),
        loss:           list[tuple[int]] =              [],
        walls:          list[tuple[int]] =              [],
        coins:          list[tuple[int]] =              [],
        portals:        list[dict[str, tuple[int]]] =   [],
        wrap_map:       bool =                          False,
        # Reward/Penalty
        goal_reward:    float =                         1.0,
        step_penalty:   float =                         -0.01,
        wall_penalty:   float =                         -0.1,
        loss_penalty:   float =                         -0.5,
        coin_reward:    float =                         0.5,
        **kwargs
    ):
        """# Initialize Grid-World game environment.
        
        NOTE: Column indeces are in order from left to right, but row indeces are in reverse order, 
        from bottom to top.

        ## Dimension Args:
            * rows          (int, optional):                            Number of rows with which 
                                                                        grid will be initialized 
                                                                        (max = 10). Defaults to 4.
            * columns       (int, optional):                            Number of columns with which 
                                                                        grid will be initialized 
                                                                        (max = 10). Defaults to 4.
            
        ## Grid Features:
            * start         (tuple[int], optional):                     Coordinate at which agent 
                                                                        should begin the game. 
                                                                        Defaults to (0, 0).
            * goal          (tuple[int], optional):                     Row, column coordinate at 
                                                                        which goal square will be 
                                                                        located. Defaults to 
                                                                        top-right corner of grid.
            * loss          (list[tuple[int]], optional):               Row, column coordinate at 
                                                                        which loss square will be 
                                                                        located.
            * walls         (list[tuple[int]], optional):               List of row, column 
                                                                        coordinates at which wall 
                                                                        squares will be located.
            * coins         (list[tuple[int]], optional):               List of row,columns 
                                                                        coordinates at which coins 
                                                                        squares will be located.
            * portals       (list[dict[str, tuple[int]]], optional):    List of dictionaries 
                                                                        defining entry and exit row, 
                                                                        column coordinates at which 
                                                                        entry and exit portal 
                                                                        squares will be located.
            * wrap_map      (bool, optional):                           If True, agent will not 
                                                                        collide with grid 
                                                                        boundaries, but will 
                                                                        instead be transported to 
                                                                        the opposite side of the 
                                                                        grid corresponding to the 
                                                                        location that they exited 
                                                                        the grid. Defaults to False.
            
        ## Reward/Punishment:
            * goal_reward   (float, optional):                          Reward recieved if agent 
                                                                        lands on winning terminal 
                                                                        state. Defaults to 1.0.
            * step_penalty  (float, optional):                          Cost for each action that 
                                                                        the agent takes. Defaults 
                                                                        to -0.01.
            * wall_penalty  (float, optional):                          Penalty received if agent 
                                                                        collides with a wall square. 
                                                                        Defaults to -0.1.
            * loss_penalty  (float, optional):                          Penalty recieved if agent 
                                                                        lands on losing terminal 
                                                                        state. Defaults to -0.5.
            * coin_reward   (float, optional):                          Reward received if agents 
                                                                        lands on coin square. 
                                                                        Defaults to 0.5.
        """
        # Initialize Environment object.
        super(GridWorld, self).__init__()
        
        # Initialize logger.
        self.__logger__:        Logger =                        get_child(
                                                                    logger_name =   "grid-world",
                                                                    
                                                                )
        
        # Ensure state dimensions are greater than zero.
        assert 0 < rows <=10,                   f"Row dimension must be integer value 1-10, got {rows}"
        assert 0 < columns <= 10,               f"Column dimension must be integer value 1-10, got {columns}"
        
        # If no goal coordinate was provided, default to top-right corner.
        if goal is None: goal: tuple[int] = (rows - 1, columns - 1)
        
        # Assert that goal square exists within state dimensions.
        assert (
            0 <= goal[0] < rows                 and
            0 <= goal[1] < columns
        ),                                      f"Goal coordinate {goal} is out of bounds for environment shape ({rows}, {columns})"
        
        # Ensure that the goal is not the same as the start.
        assert goal != start,                   f"Goal coordinate {goal} cannot be the same as start coordinate {start}"
        
        # Assert that start square exists within state dimensions.
        assert (
            0 <= start[0] < rows                and
            0 <= start[1] < columns
        ),                                      f"Start coordinate {start} is out of bounds for environment shape ({rows}, {columns})"
        
        # If a loss square was specified...
        for c, coordinate in enumerate(loss):
            
            # Assert that loss square exists within state dimensions.
            assert (
                0 <= coordinate[0] < rows       and
                0 <= coordinate[1] < columns
            ),                                  f"Loss[{c}] coordinate {coordinate} is out of bounds for environment shape ({rows}, {columns})"
            
            # Assert that loss square is not being placed on goal square.
            assert coordinate != goal,          f"Loss[{c}] coordinate {coordinate} cannot be the same as goal square {goal}"
        
        # For each wall coordinate provided...
        for c, coordinate in enumerate(walls):
            
            # Assert that wall square exists within state dimensions.
            assert (
                0 <= coordinate[0] < rows       and
                0 <= coordinate[1] < columns
            ),                                  f"Wall[{c}] coordinate {coordinate} is out of bounds for environment shape ({rows}, {columns})"
            
            # Assert that wall square is not being placed on goal square.
            assert coordinate != goal,          f"Wall[{c}] coordinate {coordinate} cannot be the same as goal square {goal}"
            assert coordinate not in loss,      f"Wall[{c}] coordinate overlaps with loss coordinate(s): {loss}"
            assert coordinate not in coins,     f"Wall[{c}] coordinate overlaps with coin coordinate(s): {coins}"
            assert coordinate not in portals,   f"Wall[{c}] coordinate overlaps with portal coordinate(s): {portals}"
        
        # For each coin coordinate provided...
        for c, coordinate in enumerate(coins):
            
            # Assert that wall square exists within state dimensions.
            assert (
                0 <= coordinate[0] < rows       and
                0 <= coordinate[1] < columns
            ),                                  f"Coin[{c}] coordinate {coordinate} is out of bounds for environment shape ({rows}, {columns})"
            
            # Assert that wall square is not being placed on goal square.
            assert coordinate != goal,          f"Coin[{c}] coordinate {coordinate} cannot be the same as goal square {goal}"
            
        # Define dimensions.
        self._rows_:            int =                           rows
        self._columns_:         int =                           columns
        self._shape_:           tuple[int] =                    (rows, columns)
        self._state_size_:      int =                           rows * columns
        
        # Define grid features.
        self._goal_:            tuple[int] =                    goal
        self._start_:           tuple[int] =                    start
        self._loss_:            list[tuple[int]] =              loss
        self._walls_:           list[tuple[int]] =              walls
        self._coins_:           list[tuple[int]] =              coins
        self._portals_:         list[dict[str, tuple[int]]] =   portals
        self._wrap_map_:        bool =                          wrap_map
        
        # Define rewards & penalties.
        self._goal_reward_:     float =                         goal_reward
        self._step_penalty_:    float =                         step_penalty
        self._wall_penalty_:    float =                         wall_penalty
        self._loss_penalty_:    float =                         loss_penalty
        self._coin_reward_:     float =                         coin_reward
        
        # Define actions.
        self._action_size_:     int =                           4
        self._actions_:         dict =                          {
                                                                    0:  {
                                                                            "name":     "DOWN",
                                                                            "delta":    (-1, 0),
                                                                            "symbol":   "↓"
                                                                        },
                                                                    1:  {
                                                                            "name":     "UP",
                                                                            "delta":    (1, 0),
                                                                            "symbol":   "↑"
                                                                        },
                                                                    2:  {
                                                                            "name":     "LEFT",
                                                                            "delta":    (0, -1),
                                                                            "symbol":   "←"
                                                                        },
                                                                    3:  {
                                                                            "name":     "RIGHT",
                                                                            "delta":    (0, 1),
                                                                            "symbol":   "→"
                                                                        }
                                                                }
        
        # Initialize interaction metrics.
        self.reset()

        # Log for debugging.
        self.__logger__.debug(f"Initialized Grid World {locals()}")
        
    def __str__(self) -> str:
        """# Provide string format of Grid-World puzzle.

        ## Returns:
            * str: String format of Grid-World puzzle.
        """
        # Initialize with top border.
        grid_str:   str =   "   ┌" + ("───┬" * (self._columns_ - 1)) + "───┐"
        
        # For each row that needs to be printed...
        for row in reversed(range(self._rows_)):
            
            # Append left border with row index.
            grid_str += f"\n {row} │"
            
            # For each column that needs to be printed...
            for column in range(self._columns_):
                
                # Format as agent position.
                if (row, column) == tuple(self._agent_position_):           grid_str += f" {colored(text = "A", color = "blue")} │"
                
                # Format as wall square.
                elif (row, column) in self._walls_:                         grid_str += " █ │"
                
                # Format as coin square.
                elif (row, column) in self._coins_remaining_:               grid_str += f" {colored(text = "$", color = "yellow")} │"
                
                # Format as loss square.
                elif (row, column) in self._loss_:                          grid_str += f" {colored(text = "◯", color = "red")} │"
                
                # Format as goal square.
                elif (row, column) == self._goal_:                          grid_str += f" {colored(text = "◯", color = "green")} │"
                
                # Format as portal entry.
                elif (row, column) in [p["entry"] for p in self._portals_]: grid_str += f" ☖ │"
                
                # Format as portal exit.
                elif (row, column) in [p["exit"] for p in self._portals_]:  grid_str += f" ☗ │"
                
                # Otherise, it's a normal, navigable square.
                else: grid_str += "   │"
                
            # Append right border and dividing line, if not at end of grid.
            if row != 0: grid_str += "\n   ├" + ("───┼" * (self._columns_ - 1)) + "───┤"
            
        # Initialize column index.
        col_idx:    str =   "\n   "
            
        # Populate column index.
        for col in range(self._columns_): col_idx += f"  {col} "
        
        # Return final string with bottom border.
        return grid_str + "\n   └" + ("───┴" * (self._columns_ - 1)) + "───┘" + col_idx
    
    def metadata(self) -> dict:
        """# Get Metadata
        
        Provide a dictionary outlining running metrics pertaining to the agent's interaction with 
        the environment.

        ## Returns:
            * dict: Metadata dictionary.
        """
        # Provide marshalled metrics.
        return  {
                    "game_status":              self._game_status_,
                    "squares_visited":          len(self._squares_visited_),
                    "squares_visited_ratio":    len(self._squares_visited_) / self._state_size_,
                    "coins_remaining":          len(self._coins_remaining_),
                    "coins_collected":          self._coins_collected_,
                    "coins_ratio":              self._coins_collected_ / (
                                                    len(self._coins_remaining_)
                                                    if len(self._coins_remaining_) > 0 
                                                    else 1
                                                ),
                    "coins_rewards":            self._coins_collected_ * self._coin_reward_,
                    "portal_activations":       self._portals_entered_,
                    "wall_collisions":          self._wall_collisions_,
                    "boundary_collisions":      self._boundary_collisions_,
                    "collision_penalties":      (self._wall_collisions_ + self._boundary_collisions_) * self._wall_penalty_
                }
    
    def portal_exit(self,
        portal_entry:   tuple[int]
    ) -> tuple[int]:
        """# Provide Portal Exit.
        
        Given a portal entry coordinate, provide the respective portal exit coordinate.

        ## Args:
            * port_entry    (tuple[int]):   Coordinate of portal entry.

        ## Returns:
            * tuple[int]:   Coordinate of portal exit.
        """
        # For each portal defined...
        for portal in self._portals_:
            
            # If entry coordinate matches the one given...
            if portal["entry"] == portal_entry:
                
                # Provide the exit coordinate.
                return portal["exit"]
            
    def render(self) -> None:
        """# Render Environment
        
        Render environment in console such that it appears animated.
        """
        # Clear console to simulate "new frame".
        system("clear" if name != "nt" else "cls")
        
        # Display grid.
        print(self.__str__())
        
        # Display current metrics.
        print(f"Steps:  {self._steps_taken_}\nReward: {self._cumulative_reward_}\nStatus: {self._game_status_}")
        
        # Wait for a small amount of time.
        sleep(0.1)
    
    def reset(self) -> list[int]:
        """# Reset puzzle; Move agent to bottom left corner (0, 0).
        
        ## Returns:
        * tuple[int]:   Current agent position.
        """
        # Set agent position to starting point.
        self._agent_position_:      list[int] =     list(self._start_)
        self._game_status_:         str =           "INCOMPLETE"
        self._cumulative_reward_:   float =         0.0
        
        # Initialize step sequence.
        self._step_sequence_:       list[tuple] =   []
        self._steps_taken_:         int =           0
        
        # Initialize interaction metrics & counters.
        self._coins_remaining_:     list[tuple] =   self._coins_.copy()
        self._coins_collected_:     int =           0
        self._portals_entered_:     int =           0
        self._wall_collisions_:     int =           0
        self._boundary_collisions_: int =           0
        self._squares_visited_:     set =           set()

        # Log for debugging.
        self.__logger__.debug(f"Agent reset to starting position: {self._start_}")
        
        # Return current state.
        return self.state()
    
    def save_config(self,
        path:   str
    ) -> None:
        """# Save Environment Configuration.

        ## Args:
            * path  (str):  Path at which environment configuration file will be saved.
        """
        from json   import dump
        from os     import makedirs
        
        # Ensure that path exists.
        makedirs(name = path, exist_ok = True)
        
        # Save configuratino to JSON file.
        dump(
            obj =       {
                            "rows":         self._rows_,
                            "columns":      self._columns_,
                            "start":        self._start_,
                            "loss":         self._loss_,
                            "walls":        self._walls_,
                            "coins":        self._coins_,
                            "portals":      self._portals_,
                            "wrap_map":     self._wrap_map_,
                            "goal_reward":  self._goal_reward_,
                            "step_penalty": self._step_penalty_,
                            "wall_penalty": self._wall_penalty_,
                            "loss_penalty": self._loss_penalty_,
                            "coin_reward":  self._coin_reward_
                        },
            fp =        open(f"{path}/grid_world_config.json", "w"),
            indent =    2,
            default =   str
        )
        
        # Log save location.
        self.__logger__.info(f"Grid World configuration saved to {path}/grid_world_config.json")
    
    def state(self) -> int:
        """# Provide the agent's current position in the puzzle.

        ## Returns:
            * int:  Agent's current position in the puzzle.
        """
        return (self._agent_position_[0] * self._columns_) + self._agent_position_[1]
    
    def step(self,
        action: str
    ) -> tuple[tuple[int], int, bool, dict]:
        """# Execute action on environment.

        ## Args:
            * action    (str):  Choice of "up", "down", "left", or "right".        

        ## Returns:
            * tuple[tuple[int], int]:
                * tuple[int]:   Agent's position after action.
                * int:          Agent's reward/punishment after action.
                    * 1:        Agent has reached goal square.
                    * -0.1:     Agent has not reached goal square.
                * bool:
                    * True:     Agent has reached goal square.
                    * False:    Agent has not reached goal square.
                * dict:         Metadata, outlining status & metrics of current game.
        """
        # Log action for debugging.
        self.__logger__.debug(f"Action submitted: {self._actions_[action]["name"]}")

        # Calculate new position.
        new_position:   list[int] = [
            self._agent_position_[0] + self._actions_[action]["delta"][0], # New row
            self._agent_position_[1] + self._actions_[action]["delta"][1]  # New column
        ]
        
        # Increment step count.
        self._steps_taken_ += 1
        
        # If new position is out of bounds...
        if (
            (0 > new_position[0] or new_position[0] >= self._rows_)      or
            (0 > new_position[1] or new_position[1] >= self._columns_) 
        ):
            
            # If map is not wrapped...
            if not self._wrap_map_:
                
                # Increment boundary collision count.
                self._boundary_collisions_ +=   1
                
                # Update cumulative reward.
                self._cumulative_reward_ +=     self._wall_penalty_
                
                # Log for debugging
                self.__logger__.debug(f"Action leads out of bounds (boundary collisions: {self._boundary_collisions_})")
                
                # Return original position with punishment.
                return (
                    self.state(),               # State before action
                    self._wall_penalty_,        # Collision penalty
                    False,                      # End state not reached,
                    self.metadata()             # Current game metrics
                )
                
            # Otherwise...
            else:
                
                # Log for debugging
                self.__logger__.debug(f"Action leads out of bounds, but map is wrapped")
                
                # New position will be modulated from last position.
                new_position[0] =   new_position[0] % self._rows_
                new_position[1] =   new_position[1] % self._columns_
                
        # Add new position to squares visited set.
        self._squares_visited_.add(tuple(new_position))

        # If new position is a wall...
        if tuple(new_position) in self._walls_:
            
            # Increment wall collision count.
            self._wall_collisions_ +=   1
                
            # Update cumulative reward.
            self._cumulative_reward_ += self._wall_penalty_

            # Log for debugging
            self.__logger__.debug(f"Action leads to wall square at {new_position} (wall collisions: {self._wall_collisions_})")

            # Return original position with punishment.
            return  (
                        self.state(),           # State before action
                        self._wall_penalty_,    # Punishment
                        False,                  # End state not reached
                        self.metadata()         # Current game metrics
                    )

        # If new position is loss square...
        if tuple(new_position) in self._loss_:
            
            # Set game status.
            self._game_status_ =    "LOSE"
                
            # Update cumulative reward.
            self._cumulative_reward_ += self._loss_penalty_

            # Log for debugging
            self.__logger__.debug(f"New position is a loss sqaure. Agent loses.")

            # Return original position with punishment.
            return  (
                        self.state(),           # Loss square position
                        self._loss_penalty_,    # Loss penalty
                        True,                   # End state reached
                        self.metadata()         # Current game metrics
                    )
            
        # If new position is a portal entry square...
        if tuple(new_position) in [p["entry"] for p in self._portals_]:
            
            # Increment portal activation count.
            self._portals_entered_ += 1
            
            # Log for debugging.
            self.__logger__.debug(f"Actions leads to portal from {tuple(new_position)} to {self.portal_exit(portal_entry = tuple(new_position))} (portals activated: {self._portals_entered_})")
            
            # Define new position at portal exit.
            new_position:   tuple[int] =    self.portal_exit(portal_entry = tuple(new_position))
                
            # Update cumulative reward.
            self._cumulative_reward_ +=     self._step_penalty_
            
            # Return new position at exit portal with penalty.
            return  (
                        self.state(),           # Portal exit
                        self._step_penalty_,    # Step penalty
                        False,                  # End state not reached
                        self.metadata()         # Current game metrics
                    )
            
        # If new position earns a coin...
        if tuple(new_position) in self._coins_remaining_:
            
            # Increment coin collection count.
            self._coins_collected_ += 1
            
            # Eliminate coin from grid.
            self._coins_remaining_.remove(tuple(new_position))

            # Log for debugging
            self.__logger__.debug(f"Action leads to coin sqaure (coins collected: {self._coins_collected_}).")
                
            # Update cumulative reward.
            self._cumulative_reward_ += self._coin_reward_

            # Return original position with punishment.
            return  (
                        self.state(),           # Loss square position
                        self._coin_reward_,     # Coin reward
                        False,                  # End state reached
                        self.metadata()         # Current game metrics
                    )
        
        # Otherwise, update agent position.
        self._agent_position_ = new_position
            
        # Update game status.
        self._game_status_ =    "WIN" if tuple(self._agent_position_) == self._goal_ else "INCOMPLETE"

        # Log for debugging
        self.__logger__.debug(f"Step taken (new agent position: {self._agent_position_}, reward: {1 if self.state() == self._goal_ else -0.1}, done: {tuple(self._agent_position_) == self._goal_})")
                
        # Update cumulative reward.
        self._cumulative_reward_ += self._goal_reward_ if self.state() == self._goal_ else self._step_penalty_
        
        # Provide agent's position, reward/punishment, & completion status.
        return (
            self.state(),                                                               # Agent's new position
            self._goal_reward_ if self.state() == self._goal_ else self._step_penalty_, # Reward/punishment
            tuple(self._agent_position_) == self._goal_,                                # Completion status
            self.metadata()                                                             # Current game metrics
        )