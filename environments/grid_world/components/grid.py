"""# ludorum.environments.gridf_world.components.grid

Defines the basic greid component of Grid World.
"""

from typing                                     import Any, Dict, List, Optional, Set, Tuple, Union

from environments.grid_world.components.squares import *

class Grid():
    """# (Grid World) Grid
    
    Basic grid representation.
    """
    
    def __init__(self,
        # Dimensions.
        rows:               Optional[int] =                                 4,
        columns:            Optional[int] =                                 4,
        
        # Features.
        start:              Optional[Tuple[int, int]] =                     (0, 0),
        goal:               Optional[Set[Tuple[int, int]]] =                None,
        loss:               Optional[Set[Tuple[int, int]]] =                set(),
        walls:              Optional[Set[Tuple[int, int]]] =                set(),
        coins:              Optional[Set[Tuple[int, int]]] =                set(),
        portals:            Optional[List[Dict[str, Tuple[int, int]]]] =    [],
        wrap_map:           Optional[bool] =                                False,
        
        # Rewards/Penalties.
        goal_reward:        Optional[float] =                                1.0,
        step_penalty:       Optional[float] =                               -0.01,
        collision_penalty:  Optional[float] =                               -0.1,
        loss_penalty:       Optional[float] =                               -1.0,
        coin_reward:        Optional[float] =                                0.5,
        **kwargs
    ):
        """# Instantiate Grid World grid.
        
        NOTE: Column indices are in order from left to right, but row indices are in reverse order 
        (from bottom to top).

        ## Dimensions:
            * rows              (int):                              Number of rows with which grid 
                                                                    will be initialized (max = 10). 
                                                                    Defaults to 4.
            * columns           (int):                              Number of columns with which 
                                                                    grid will be initialized (max = 
                                                                    10). Defaults to 4.

        ## Features:
            * coins             (Set[Tuple[int, int]]):             Set of coordinates at which coin 
                                                                    squares will be located within 
                                                                    grid.
            * goal              (Set[Tuple[int, int]]):             Coordinate at which the goal 
                                                                    square will be located in the 
                                                                    grid. Defaults to the top right 
                                                                    corner.
            * loss              (Set[Tuple[int, int]]):             Set of coordinates at which loss 
                                                                    squares will be located within 
                                                                    grid.
            * portals           (List[Dict[str, Tuple[int, int]]]): List of entry -> exit coordinate 
                                                                    mappings at which portal entries 
                                                                    and exits will be located within 
                                                                    grid.
            * start             (Tuple[int, int]):                  Coordinate at which the agent 
                                                                    will begin the game at the start 
                                                                    of each episode. Defaults to 
                                                                    (0, 0) (bottom left corner).
            * walls             (Set[Tuple[int, int]]):             Set of coordinates at which wall 
                                                                    squares will be located within 
                                                                    grid.
            * wrap_map          (bool):                             If true, the agent will not 
                                                                    collide with grid boundaries, 
                                                                    but will instead appear at the 
                                                                    opposite side of the grid.

        ## Rewards/Penalties:
            * coin_reward       (float):                            Reward yielded by collecting 
                                                                    coins. NOTE: Coins are ephemeral 
                                                                    (they can only be collected once 
                                                                    per episode). If coin has 
                                                                    already been collected, the 
                                                                    penalty incurred for re-entering 
                                                                    the square will be the negative 
                                                                    of the reward.
            * collision_penalty (float):                            Penalty incurred for colliding 
                                                                    with wall squares or the grid 
                                                                    boundary (if wrap_map == False).
            * goal_reward       (float):                            Reward yielded by reaching goal 
                                                                    square.
            * loss_penalty      (float):                            Penalty incurred for landing on 
                                                                    loss square(s).
            * step_penalty      (float):                            Penalty incurred for each step 
                                                                    that the agent takes during an 
                                                                    episode.
        """
        # Define dimensions.
        self._columns_:             int =                               columns
        self._rows_:                int =                               rows
        
        # Define features.
        self._coins_:               Set[Tuple[int, int]] =              coins
        self._goal_:                Set[Tuple[int, int]] =              goal
        self._loss_:                Set[Tuple[int, int]] =              loss
        self._portals_:             List[Dict[str, Tuple[int, int]]] =  portals
        self._start_:               Tuple[int, int] =                   start
        self._walls_:               Set[Tuple[int, int]] =              walls
        self._wrap_map_:            bool =                              wrap_map
        
        # Define rewards/penalties.
        self._coin_reward_:         float =                             coin_reward
        self._collisision_penalty_: float =                             collision_penalty
        self._goal_reward_:         float =                             goal_reward
        self._loss_penalty_:        float =                             loss_penalty
        self._step_penalty_:        float =                             step_penalty
        
        # Set agent location to start square.
        self._agent_:               Tuple[int, int] =                   self._start_
        
        # Validate parameters.
        self.__post_init__()
        
        # Populate squares.
        self._populate_()
        
    def __post_init__(self) -> None:
        """# Verify Parameters.
        
        Verify parameters provided upon initialization.
        
        ## Raises:
            AssertionError: If any parameter violates constraints.
        """
        # Assert that no more than 10 rows and columns are specified.
        assert self.rows    <= 10, f"Maximum of 10 rows allowed, got {self.rows}"
        assert self.columns <= 10, f"Maximum of 10 columns allowed, got {self.columns}"
        
        # Create affidavit of coordinate sets.
        features:       Dict[str, Set[Tuple[int, int]]] =   {
                                                                "start":    {self._start_},
                                                                "goal":     self._goal_,
                                                                "loss":     self._loss_,
                                                                "walls":    self._walls_,
                                                                "coins":    self._coins_,
                                                                "entry":    {portal["entry"]    for portal in self._portals_},
                                                                "exit":     {portal["exit"]     for portal in self._portals_}
                                                            }
        
        # Flatten coordinates into a single set.
        coordinates:    Set[Tuple[int, int]] =              set.union(*features.values())
        
        # For each coordinate...
        for coordinate in coordinates:
            
            # Assert that coordinate is in bounds.
            assert self._is_in_bounds_(coordinate = coordinate), f"Coordinate is out of bounds: {coordinate}"
            
        # Initialize coordinate tracking.
        seen:           Set[Tuple[int, int]] =              set()
        
        # For each feature type and coordinate pair...
        for feature, coordinates in features.items():
            
            # Make intersection.
            intersection:   Set[Tuple[int, int]] =  seen & coordinates
            
            # Assert that there is not intersection with coordinates seen thus far.
            assert not intersection, f"Intersecting coordinates found for {feature} at {intersection}"
            
            # Update set of coordinates seen.
            seen |= coordinates
        
    # PROPERTIES ===================================================================================
    
    @property
    def coin_reward(self) -> float:
        """# Coin Reward

        Reward yielded by collecting a coin.
        """
        return self._coin_reward_
    
    @property
    def coins(self) -> Set[Tuple[int, int]]:
        """# Coins

        Set of coordinates at which coins are located.
        """
        return self._coins_
    
    @property
    def collision_penalty(self) -> float:
        """# Collision Penalty

        Penalty incurred for colliding with walls or grid boundaries (if not wrapped).
        """
        return self._collisision_penalty_
    
    @property
    def columns(self) -> int:
        """# Column

        Column in which square is located within grid.
        """
        return self._columns_
    
    @property
    def goal(self) -> Set[Tuple[int, int]]:
        """# Goal
        
        Set of coordinates at which goal squares are located.
        """
        return self._goal_
    
    @property
    def goal_reward(self) -> float:
        """# Goal Reward

        Reward yielded by reaching goal square.
        """
        return self._goal_reward_
    
    @property
    def loss(self) -> Set[Tuple[int, int]]:
        """# Loss
        
        Coordinates at which loss squares are located.
        """
        return self._loss_
    
    @property
    def loss_penalty(self) -> float:
        """# Loss Penalty
        
        Penalty incurred for landing on loss square.
        """
        return self._loss_penalty_
    
    @property
    def portals(self) -> List[Dict[str, Tuple[int, int]]]:
        """# Portals
        
        List of mappings for portal "entry" and "exit" coordinates.
        """
        return self._portals_
    
    @property
    def rows(self) -> int:
        """# Row

        Row in which square is located within grid.
        """
        return self._rows_
    
    @property
    def shape(self) -> Tuple[int, int]:
        """# Shape

        The two-dimensional shape of the grid.
        """
        return self.rows, self.columns
    
    @property
    def step_penalty(self) -> float:
        """# Step Penalty

        Expense incurred for taking an action.
        """
        return self._step_penalty_
    
    @property
    def walls(self) -> Set[Tuple[int, int]]:
        """# Walls
        
        Coordinates at which walls are located.
        """
        return self._walls_
    
    @property
    def wrapped(self) -> bool:
        """# (Map) is Wrapped?

        If true, the agent will not collide with grid boundaries, but will instead appear at the 
        opposite side of the grid.
        """
        return self._wrap_map_
    
    # METHODS ======================================================================================
    
    def move(self,
        action: Tuple[int, int]
    ) -> Tuple[float, Union[Tuple[int, int], int], bool, Dict[str, Any]]:
        """# Move
        
        Update agent location and the state of the grid based on the action submitted by the agent.
        
        ## Args:
            * action    (Tuple[int, int]):  Delta of action submitted.

        ## Returns:
            * Tuple[float, Union[Tuple[int, int], int], bool, Dict[str, Any]]:
                * Reward yielded/penalty incurred by action submitted.
                * New state/coordinate location of agent after action was taken.
                * True if agent has reached a terminal state.
                * Metadata/information related to result of action.
        """
        # Compute resulting location.
        new_coordinate: Tuple[int, int] =   (
                                                self._agent_[0] + action[0],
                                                self._agent_[1] + action[1]
                                            )
        
        # If new coordinate is out of bounds...
        if not self._is_in_bounds_(coordinate = new_coordinate):
            
            # If map is not wrapped...
            if not self.wrapped:
                
                # Return penalty for boundary collision.
                return  self.collision_penalty, \
                        self._agent_,    \
                        False,                  \
                        {"event": "collided with boundary"}
                        
            # Otherwise, modulate new coordinate based on dimensions.
            new_coordinate: Tuple[int, int] =   (
                                                    new_coordinate[0] % self.rows,
                                                    new_coordinate[1] % self.columns
                                                )
            
        # Interact with square.
        value, state, done, metadata =      self._get_square_(coordinate = new_coordinate).interact()
        
        # Update agent location.
        self._agent_:   Tuple[int, int] =   state if state is not None else self._agent_
            
        # Return result of action.
        return  value,                                                  \
                self._coordinate_to_state_(coordinate = self._agent_),  \
                done,                                                   \
                metadata
            
    def reset(self) -> int:
        """# Reset.
        
        Reset grid to initial state.

        ## Returns:
            * int: Agent's starting location.
        """
        # For each row...
        for row in self._grid_: 
            
            # Reset each square in row.
            for square in row: square.reset()
            
        # Reset agent.
        self._agent_:   Tuple[int, int] =   self._start_
            
        # Provide agent's starting location.
        return self._coordinate_to_state_(coordinate = self._agent_)
    
    # HELPERS ======================================================================================
    
    def _coordinate_to_state_(self,
        coordinate: Tuple[int, int]
    ) -> int:
        """# (Convert) Coordinate to State.

        ## Args:
            * coordinate    (Tuple[int, int]):  Coordinate being converted.

        ## Returns:
            * int:  State representation of coordinate.
        """
        return coordinate[0] * self.columns + coordinate[1]
    
    def _get_square_(self,
        coordinate: Tuple[int, int]
    ) -> Square:
        """# Get Square.
        
        Fetch square at specified coordinate.

        ## Args:
            * coordinate    (Tuple[int, int]):  Row, column coordinate of square being fetched.

        ## Returns:
            * Square:   Requested square.
        """
        # Assert that coordinate provided is valid.
        assert self._is_in_bounds_(coordinate = coordinate), f"Coordinates provided are out of bounds"
        
        # Return requested square.
        return self._grid_[coordinate[0]][coordinate[1]]
    
    def _is_in_bounds_(self,
        coordinate: Tuple[int, int]
    ) -> bool:
        """# (Coordinate) is in Bounds?

        ## Args:
            * coordinate    (Tuple[int, int]):  Coordinate being verified.

        ## Returns:
            * bool: True if coordinate is in bounds of grid.
        """
        return 0 <= coordinate[0] < self.rows and 0 <= coordinate[1] < self.columns
    
    def _populate_(self) -> None:
        """# Populate Grid.
        
        Populate grid with squares of types specified by feature parametters.
        """
        # Instantiate grid of empty squares.
        self._grid_:    List[List[Square]] =    [
                                                    [
                                                        Square(row = r, column = c, value = self.step_penalty)
                                                        for c in range(self.columns)
                                                    ]   for r in range(self.rows)
                                                ]
        
        # Populate features.
        for r, c in self.goal:  self._grid_[r][c] =   Goal(row = r, column = c, value = self.goal_reward)
        for r, c in self.loss:  self._grid_[r][c] =   Loss(row = r, column = c, value = self.loss_penalty)
        for r, c in self.coins: self._grid_[r][c] =   Coin(row = r, column = c, value = self.coin_reward)
        for r, c in self.walls: self._grid_[r][c] =   Wall(row = r, column = c, value = self.collision_penalty)
        
        # For each portal...
        for portal in self.portals:
            
            # Instantiate portal entry.
            self._grid_[portal["entry"][0]][portal["entry"][1]] = Portal(
                                                                    row =       portal["entry"][0],
                                                                    column =    portal["entry"][1],
                                                                    exit =      portal["exit"],
                                                                    value =     self.step_penalty
                                                                )
            
    # DUNDERS ======================================================================================
    
    def __repr__(self) -> str:
        """# Object Representation.

        Object representation of grid.
        """
        return f"<Grid(rows = {self.rows}, columns = {self.columns}, start = {self.start}, goal = {self.goal})>"
    
    def __str__(self) -> str:
        """# String Representation.
        
        String rendering of grid.
        """
        # Predefine border and index strings.
        column_index:   str =   (" " * 4) + " ".join(f" {column} " for column in range(self.columns))
        top_border:     str =   "\n   ┌" + ((("─" * 3) + "┬") * (self.columns - 1)) + ("─" * 3) + "┐"
        middle_line:    str =   "\n   ├" + ((("─" * 3) + "┼") * (self.columns - 1)) + ("─" * 3) + "┤"
        bottom_border:  str =   "\n   └" + ((("─" * 3) + "┴") * (self.columns - 1)) + ("─" * 3) + "┘"
        
        # Initialize grid string to which rendering will be appended.
        grid_string:    str =   column_index + top_border
        
        # For each row in grid...
        for r, row in enumerate(self._grid_):
            
            # Start new row with index.
            grid_string     += f"\n {r} │"
            
            # For each square in row...
            for c, square in enumerate(row):
                
                # Append square or agent symbol.
                grid_string += f""" {"A" if self._agent_ == (r, c) else square} │"""
                
            # Append row separator or bottom border.
            grid_string     += middle_line if r != self.rows - 1 else bottom_border
                                        
        # Return grid representation.
        return grid_string