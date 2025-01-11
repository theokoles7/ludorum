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
        goal:       tuple[int] =        (3, 4),
        loss:       tuple[int] =        None,
        walls:      list[tuple[int]] =  []
    ):
        """# Initialize Grid-World game environment.
        
        NOTE: Column indeces are in order from left to right, but row indeces are in reverse order, 
        from the bottom to the top.

        ## Args:
            * rows      (int, optional):            Number of rows with which grid will be 
                                                    initialized. Defaults to 3.
            * columns   (int, optional):            Number of columns with which grid will be 
                                                    initialized. Defaults to 4.
            * goal  (tuple[int], optional):         Row, column coordinate at which goal square will 
                                                    be located. Defaults to (3, 4).
            * loss  (tuple[int], optional):         Row, column coordinate at which loss square will 
                                                    be located.
            * wall  (list[tuple[int]], optional):   List of row, column coordinates at which wall 
                                                    squares will be located.
        """
        # Initialize logger
        self._logger:   Logger =    LOGGER.getChild("grid-world")
        
        # Define attributes
        self.rows:              int =               rows
        self.columns:           int =               columns
        self.goal:              tuple[int] =        goal
        self.loss:              tuple[int] =        loss
        self.walls:             list[tuple[int]] =  walls
        
        # Define actions
        self.actions:           dict =              {
                                                        "up":       (-1,  0),
                                                        "down":     ( 1,  0),
                                                        "left":     ( 0, -1),
                                                        "right":    ( 0,  1)
                                                    }
        
        # Log for debugging
        self._logger.debug(f"Initialize Grid-World puzzle ({locals()})")
        
        # Set agent position to (1, 1)
        self.agent_position:    tuple[int] =        (1, 1)
        
    def __str__(self) -> str:
        """# Provide string format of Grid-World puzzle.

        ## Returns:
            * str: String format of Grid-World puzzle.
        """
        # Initialize with top border
        grid_str:   str =   "   ┌" + ("───┬" * (self.columns - 1)) + "───┐"
        
        # For each row that needs to be printed...
        for row in reversed(range(1, self.rows + 1)):
            
            # Append left border with row index
            grid_str += f"\n {row} │"
            
            # For each column that needs to be printed...
            for column in range(1, self.columns + 1):
                
                # Format as wall square
                if (row, column) in self.walls: grid_str += " ╳ │"
                
                # Format as goal square
                elif (row, column) == self.goal:  grid_str += f" {colored(text = '█', color = "green")} │"
                
                # Format as loss square
                elif (row, column) == self.loss:  grid_str += f" {colored(text = '█', color = "red")} │"
                
                # Otherise, it's a normal, navigable square
                else: grid_str += "   │"
                
            # Append right border and dividing line, if not at end of grid
            if row != 1: grid_str += "\n   ├" + ("───┼" * (self.columns - 1)) + "───┤"
            
        # Initialize column index
        col_idx:    str =   "\n   "
            
        # Populate column index
        for col in range(1, self.columns + 1): col_idx += f"  {col} "
        
        # Return final string with bottom border
        return grid_str + "\n   └" + ("───┴" * (self.columns - 1)) + "───┘" + col_idx
    
    def reset(self) -> tuple[int]:
        """# Reset puzzle; Move agent to bottom left corner (1, 1).
        
        ## Returns:
        * tuple[int]:   Current agent position.
        """
        # Set agent position to row 1, column 1
        self.agent_position:    tuple[int] =    (1, 1)
        
        # Return current state
        return self.state()
    
    def state(self) -> tuple[int]:
        """# Provide the agent's current position in the puzzle.

        ## Returns:
            * tuple[int]:   Agent's current position in the puzzle.
        """
        return self.agent_position
    
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
        # Update agent's row coordinate
        self.agent_position[0] = max(0, min(self.rows - 1, self.agent_position[0] + self.actions[action][0]))
        
        # Update agent's column coordinate
        self.agent_position[1] = max(0, min(self.columns - 1, self.agent_position[1] + self.actions[action][1]))
        
        # Provide agent's position, reward/punishment, & completion status
        return (
            self.state(),                                   # Agent's position
            (1 if self.state() == self.goal() else -0.1),   # Reward/punishment
            self.state() == self.goal()                     # Completion status
        )