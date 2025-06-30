"""# ludorum.environments.grid_world.base

Grid World game implementation.
"""

from typing                 import Dict, List, Optional, Set, Tuple

from environments.__base__  import Environment

class GridWorld(Environment):
    """# Grid World
    
    Discrete, deterministic grid environment.
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
        """# Instantiate Grid World Environment.
        
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
        