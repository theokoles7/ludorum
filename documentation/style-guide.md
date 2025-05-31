# Ludorum Style Guide

*Research-Focused Python Coding Standards for Reproducible Reinforcement Learning*

## Philosophy

Ludorum prioritizes **clarity**, **reproducibility**, and **educational value** over brevity. Every implementation should serve as a reference that future researchers can understand, validate, and build upon.

## Code Formatting Standards

### Line Length
- **Docstrings and comments**: Wrapped at 100 characters from left border
- **Code lines**: Follow same 100-character guideline for consistency
- **Rationale**: Academic papers use wide margins; research code should match

### Variable Alignment
Align type annotations and values for visual clarity:

```python
# ✅ Correct - Ludorum Style
agent_id:           int =       0
learning_rate:      float =     0.1
discount_factor:    float =     0.95
exploration_rate:   float =     1.0

# ❌ Incorrect - Standard PEP8
agent_id: int = 0
learning_rate: float = 0.1
discount_factor: float = 0.95
exploration_rate: float = 1.0
```

### Import Alignment
Group and align imports by category:

```python
# ✅ Correct - Ludorum Style
from abc                    import ABC, abstractmethod
from typing                 import Dict, List, Tuple, Any
from pathlib                import Path

import matplotlib.pyplot    as plt
import numpy                as np
from scipy.optimize         import minimize

from ludorum.agents         import Agent
from ludorum.environments   import Environment
```

### Function Call Alignment
Align similar function calls for readability:

```python
# ✅ Correct - Ludorum Style
env.configure(
    rows =          5,
    columns =       5,
    goal =          (4, 4),
    start =         (0, 0),
    walls =         [(1, 1), (2, 2)],
    loss_squares =  [(1, 3)],
    coins =         [(3, 1), (4, 2)]
)
```

## Documentation Standards

### File-Level Docstrings
Every `.py` file must begin with a comprehensive docstring:

```python
"""
# Q-Learning Agent Implementation

Implementation of the Q-Learning algorithm as described in:
"Q-Learning" by Watkins & Dayan (1992)
https://link.springer.com/content/pdf/10.1007/BF00992698.pdf

This module provides a tabular Q-Learning agent that learns optimal action-value 
functions through temporal difference updates. The implementation follows the 
original paper specifications with additional features for modern RL research.

## Key Mathematical Concepts:
    Q-Learning Update Rule:
        Q(s,a) ← Q(s,a) + α[r + γ max_a' Q(s',a') - Q(s,a)]
    
    Where:
        α = learning rate (controls update magnitude)
        γ = discount factor (balances immediate vs future rewards)
        ε = exploration rate (epsilon-greedy policy parameter)

## Classes:
    QLearningAgent: Main Q-Learning implementation
    
## Functions:
    create_q_learning_agent:    Factory function for agent creation
    
Author:     [Your Name]
Date:       [Creation Date]
Version:    [Version Number]
"""
```

### Class Docstrings
Include mathematical foundation and paper references:

```python
class QLearningAgent(Agent):
    """
    # Q-Learning Agent with Epsilon-Greedy Exploration
    
    Implements the Q-Learning algorithm from Watkins & Dayan (1992). This agent
    learns optimal action-value functions Q*(s,a) through off-policy temporal
    difference learning.
    
    ## Mathematical Foundation:
        The agent maintains a table Q(s,a) representing expected cumulative reward
        for taking action 'a' in state 's'. Updates follow:
        
        Q(s,a) ← Q(s,a) + α[R_{t+1} + γ max_{a'} Q(s',a') - Q(s,a)]
        
        Action selection uses ε-greedy policy:
        π(a|s) = {
            1-ε + ε/|A| if a = argmax_a Q(s,a)
            ε/|A|       otherwise
        }
    
    ## Paper Reference:
        Watkins, C. J. C. H., & Dayan, P. (1992). Q-learning. Machine learning, 
        8(3-4), 279-292.
    
    ## Args:
        * agent_id          (int):      Unique identifier for this agent instance
        * state_space_size  (int):      Number of discrete states in environment
        * action_space_size (int):      Number of possible actions
        * learning_rate     (float):    Learning rate α ∈ (0,1] for Q-value updates
        * discount_factor   (float):    Discount factor γ ∈ [0,1] for future rewards
        * exploration_rate  (float):    Initial exploration rate ε ∈ [0,1]
        * exploration_decay (float):    Decay rate for exploration reduction
        * min_exploration   (float):    Minimum exploration rate (prevents pure exploitation)
        
    ## Attributes:
        * q_table       (Dict[Tuple, float]):   State-action value function Q(s,a)
        * episode_count (int):                  Number of completed training episodes
        * step_count    (int):                  Total number of learning steps taken
        
    ## Example:
        >>> agent = QLearningAgent(
        ...     agent_id=0,
        ...     state_space_size=25,    # 5x5 grid
        ...     action_space_size=4,    # UP, DOWN, LEFT, RIGHT
        ...     learning_rate=0.1,
        ...     discount_factor=0.95
        ... )
        >>> action = agent.select_action(state=(2, 3))
        >>> agent.learn(state, action, reward, next_state, done)
    """
```

### Method Docstrings with Mathematical Detail
```python
def learn(self, 
          state:        Tuple[int, int], 
          action:       int, 
          reward:       float, 
          next_state:   Tuple[int, int], 
          done:         bool) -> Dict[str, float]:
    """
    Update Q-value using temporal difference learning.
    
    Implements the core Q-Learning update rule from Watkins & Dayan (1992):
    
        Q(s,a) ← Q(s,a) + α[r + γ max_a' Q(s',a') - Q(s,a)]
    
    The temporal difference error δ = r + γ max_a' Q(s',a') - Q(s,a) represents
    the difference between expected and actual returns. Positive δ increases 
    Q(s,a), negative δ decreases it.
    
    Implementation Details:
        1. Convert state tuples to hashable keys for Q-table lookup
        2. Retrieve current Q-value Q(s,a) from table (default: 0.0)
        3. Calculate target value:
           - If terminal: target = reward
           - If non-terminal: target = reward + γ * max_a' Q(s',a')
        4. Compute TD error: δ = target - Q(s,a)
        5. Update: Q(s,a) ← Q(s,a) + α * δ
        6. Store updated value in Q-table
    
    Args:
        state (Tuple[int, int]):        Current state coordinates (row, col)
        action (int):                   Action taken (0=DOWN, 1=UP, 2=LEFT, 3=RIGHT)
        reward (float):                 Immediate reward r_{t+1} received
        next_state (Tuple[int, int]):   Resulting state coordinates 
        done (bool):                    Whether episode terminated (affects target calculation)
        
    Returns:
        Dict[str, float]: Learning diagnostics containing:
            - 'td_error': Temporal difference error δ
            - 'old_q_value': Q-value before update
            - 'new_q_value': Q-value after update
            - 'target_value': Target value used in update
            
    Mathematical Note:when done=True, we use target = reward because there are no 
        future states to consider. This corresponds to Q(s_terminal, a) = 0 for all 
        actions in terminal states.
        
    Example:
        >>> learning_info = agent.learn(
        ...     state=(1, 2), 
        ...     action=3,           # RIGHT
        ...     reward=-0.01,       # Step penalty
        ...     next_state=(1, 3), 
        ...     done=False
        ... )
        >>> print(f"TD Error: {learning_info['td_error']:.4f}")
    """
```

## Package Structure Standards

### Required __init__.py Files
Every package and subpackage must contain `__init__.py` with proper exports:

```python
"""
Ludorum Agents Package

Collection of reinforcement learning agent implementations, each following
their original paper specifications for research reproducibility.

Available Agents:
    QLearningAgent:     Tabular Q-Learning (Watkins & Dayan, 1992)
    DQNAgent:          Deep Q-Network (Mnih et al., 2015) [Future]
    MADDPGAgent:       Multi-Agent DDPG (Lowe et al., 2017) [Future]

Usage:
    >>> from ludorum.agents import QLearningAgent
    >>> agent = QLearningAgent(state_space_size=25, action_space_size=4)
"""

__all__ = [
    "QLearningAgent",
    # Future agents will be added here
]

from .q_learning import QLearningAgent
```

## Code Comments for Algorithm Implementation

### Verbose Algorithmic Comments
```python
def select_action(self, state: Tuple[int, int]) -> int:
    """Select action using ε-greedy policy (Watkins & Dayan, 1992, Section 3)"""
    
    # Convert state to hashable key for Q-table lookup
    state_key: str = self._state_to_key(state)
    
    # ε-greedy exploration vs exploitation decision
    # With probability ε: explore (random action)
    # With probability 1-ε: exploit (greedy action selection)
    if np.random.random() < self.exploration_rate:
        
        # Exploration: uniform random action selection
        # This ensures all actions have non-zero probability of being selected,
        # satisfying the exploration requirement for Q-learning convergence
        action: int = np.random.randint(0, self.action_space_size)
        
        # Log exploration decision for debugging
        self._log_action_selection(state, action, exploration=True)
        
    else:
        
        # Exploitation: select action with highest Q-value
        # argmax_a Q(s,a) - ties broken randomly for robustness
        q_values: List[float] = [
            self.q_table.get((state_key, a), 0.0) 
            for a in range(self.action_space_size)
        ]
        
        # Handle ties in Q-values by random selection among maximal actions
        # This prevents bias toward lower-indexed actions
        max_q_value: float = max(q_values)
        best_actions: List[int] = [
            a for a, q in enumerate(q_values) 
            if q == max_q_value
        ]
        action: int = np.random.choice(best_actions)
        
        # Log exploitation decision for debugging
        self._log_action_selection(state, action, exploration=False, q_values=q_values)
    
    return action
```

## Testing Standards

### Comprehensive Test Coverage
```python
def test_q_learning_convergence_simple_mdp():
    """
    Test Q-Learning convergence on a simple 2-state MDP.
    
    Validates that the agent learns optimal policy for a deterministic MDP
    where the optimal strategy is clearly defined. This test ensures:
    1. Q-values converge to theoretical optimal values
    2. Policy converges to optimal actions
    3. Learning is stable across multiple runs
    
    Test MDP:
        States: {0, 1}
        Actions: {0, 1} 
        Transitions: Deterministic
        Rewards: State 1 gives +1, State 0 gives 0
        Optimal Policy: Always move toward State 1
    """
    # Test implementation with mathematical validation
    pass
```

## Benefits of This Style

1. **Research Reproducibility**: Every implementation can be validated against original papers
2. **Educational Value**: New researchers can learn algorithms from reading the code
3. **Debugging Efficiency**: Verbose comments make bug identification faster
4. **Long-term Maintenance**: Future developers understand design decisions
5. **Academic Standards**: Matches the precision expected in research publications

---

*This style guide prioritizes research integrity over coding brevity. In academic software, clarity and correctness matter more than conciseness.*