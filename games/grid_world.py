"""Gird World game implementation."""

__all__ = ["GridWorld"]

from logging    import Logger

from termcolor  import colored

from utils      import LOGGER

class GridWorld():
    """Grid World game environment."""
    
    def __init__(self,
        rows:       int =               3,
        columns:    int =               4,
        goal:       tuple[int] =        (2, 3),
        start:      tuple[int] =        (0, 0),
        loss:       tuple[int] =        None,
        walls:      list[tuple[int]] =  []
    ):
        """# Initialize Grid-World game environment.
        
        NOTE: Column indeces are in order from left to right, but row indeces are in reverse order, 
        from the bottom to the top.

        ## Args:
            * rows      (int, optional):                Number of rows with which grid will be initialized. Defaults to 3.
            * columns   (int, optional):                Number of columns with which grid will be initialized. Defaults to 4.
            * goal      (tuple[int], optional):         Row, column coordinate at which goal square will be located. Defaults to (3, 4).
            * start     (tuple[int], optional):         Coordinate at which agent should begin the game.
            * loss      (tuple[int], optional):         Row, column coordinate at which loss square will be located.
            * walls     (list[tuple[int]], optional):   List of row, column coordinates at which wall squares will be located.
        """
        # Initialize logger
        self.__logger__:        Logger =            LOGGER.getChild("grid-world")
        
        # Define attributes
        self._rows_:            int =               rows
        self._columns_:         int =               columns
        self._goal_:            tuple[int] =        goal
        self._loss_:            tuple[int] =        loss
        self._start_:           tuple[int] =        start
        self._walls_:           list[tuple[int]] =  walls
        
        # Define actions
        self._actions_:         dict =              {
                                                        0:  {
                                                                "name":     "DOWN",
                                                                "action":   (-1, 0)
                                                            },
                                                        1:  {
                                                                "name":     "UP",
                                                                "action":   (1, 0)
                                                            },
                                                        2:  {
                                                                "name":     "LEFT",
                                                                "action":   (0, -1)
                                                            },
                                                        3:  {
                                                                "name":     "RIGHT",
                                                                "action":   (0, 1)
                                                            }
                                                    }
        
        # Set agent position to starting point
        self._agent_position_:  list[int] =         list(self._start_)
        
        # Log for debugging
        self.__logger__.debug(f"Initialize Grid-World puzzle ({locals()})")
        
    def __str__(self) -> str:
        """# Provide string format of Grid-World puzzle.

        ## Returns:
            * str: String format of Grid-World puzzle.
        """
        # Initialize with top border
        grid_str:   str =   "   ┌" + ("───┬" * (self._columns_ - 1)) + "───┐"
        
        # For each row that needs to be printed...
        for row in reversed(range(self._rows_)):
            
            # Append left border with row index
            grid_str += f"\n {row} │"
            
            # For each column that needs to be printed...
            for column in range(self._columns_):
                
                # Format as wall square
                if (row, column) in self._walls_:                   grid_str += " ╳ │"
                
                # Format as agent position
                elif (row, column) == tuple(self._agent_position_): grid_str += f" {colored(text = 'A', color = "yellow")} │"
                
                # Format as goal square
                elif (row, column) == self._goal_:                  grid_str += f" {colored(text = '█', color = "green")} │"
                
                # Format as loss square
                elif (row, column) == self._loss_:                  grid_str += f" {colored(text = '█', color = "red")} │"
                
                # Otherise, it's a normal, navigable square
                else: grid_str += "   │"
                
            # Append right border and dividing line, if not at end of grid
            if row != 0: grid_str += "\n   ├" + ("───┼" * (self._columns_ - 1)) + "───┤"
            
        # Initialize column index
        col_idx:    str =   "\n   "
            
        # Populate column index
        for col in range(self._columns_): col_idx += f"  {col} "
        
        # Return final string with bottom border
        return grid_str + "\n   └" + ("───┴" * (self._columns_ - 1)) + "───┘" + col_idx
    
    def reset(self) -> list[int]:
        """# Reset puzzle; Move agent to bottom left corner (0, 0).
        
        ## Returns:
        * tuple[int]:   Current agent position.
        """
        # Set agent position to row 1, column 1
        self._agent_position_:  list[int] = list(self._start_)

        # Log for debugging
        self.__logger__.debug(f"Agent reset to starting position: {self._start_}")
        
        # Return current state
        return self.state()
    
    def state(self) -> tuple[int]:
        """# Provide the agent's current position in the puzzle.

        ## Returns:
            * tuple[int]:   Agent's current position in the puzzle.
        """
        return tuple(self._agent_position_)
    
    def step(self,
        action: str
    ) -> tuple[tuple[int], int, bool]:
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
        """
        # Log action for debugging
        self.__logger__.debug(f"Action submitted: {self._actions_[action]["name"]}")

        # Calculate new position
        new_position:   list[int] = [
            self._agent_position_[0] + self._actions_[action]["action"][0], # New row
            self._agent_position_[1] + self._actions_[action]["action"][1]  # New column
        ]
        
        # If new position is out of bounds...
        if (
            new_position[0] < 0                     or
            new_position[0] > self._rows_ - 1       or
            new_position[1] < 0                     or
            new_position[1] > self._columns_ - 1
        ):
            # Log for debugging
            self.__logger__.debug(f"Action leads to out of bounds")
            
            # Return original position with punishment
            return (
                self.state(),   # State before action
                -0.1,           # Punishment
                False           # End state not reached
            )

        # If new position is a wall...
        if tuple(new_position) in self._walls_:

            # Log for debugging
            self.__logger__.debug(f"Action leads to wall square at {new_position}")

            # Return original position with punishment
            return (
                self.state(),   # State before action
                -0.1,           # Punishment
                False           # End state not reached
            )

        # If new position is loss square...
        if tuple(new_position) == self._loss_:

            # Log for debugging
            self.__logger__.debug(f"New position is loss sqaure. Agent loses.")

            # Return original position with punishment
            return (
                self.state(),   # State before action
                -1,             # Punishment
                True            # End state not reached
            )
        
        # Otherwise, update agent position
        self._agent_position_ = new_position

        # Log for debugging
        self.__logger__.debug(f"Step taken (new agent position: {self.state()}, reward: {1 if self.state() == self._goal_ else -0.1}, done: {self.state() == self._goal_})")
        self.__logger__.debug(f"Current state of environment:\n{self.__str__()}")
        
        # Provide agent's position, reward/punishment, & completion status
        return (
            self.state(),                                   # Agent's position
            (1 if self.state() == self._goal_ else -0.1),   # Reward/punishment
            self.state() == self._goal_                     # Completion status
        )