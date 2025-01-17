from numpy                                          import max

from agents.value_based.tabular_based.q_learning    import QLearningAgent
from games.grid_world                               import GridWorld

# Initialize game
environment:    GridWorld =         GridWorld()

# Print game for demonstration
print(f"Game prompt:\n{environment}")

# Initialize agent
agent:          QLearningAgent =    QLearningAgent(state_size = (3, 4), action_size = 4)

# Initialize array for storing episodic rewards
rewards:        list =              []

# For each episode
for episode in range(50):

    # Reset environment
    state = environment.reset()

    # Reset reward
    total_reward: float = 0

    # For no more than 100 steps...
    for step in range(100):

        # Choose an action
        action: int = agent._choose_action_(state)

        # Record the resulting state & reward, 
        # and check if end state was reached
        next_state, reward, done = environment.step(action)

        # Update agent
        agent._update_(state, action, reward, next_state, done)

        # Update reward
        total_reward += reward

        # Update state
        state = next_state

        # End episode if end state was reached
        if done: break

    # Append episode's reward for the record
    rewards.append(total_reward)

    # Administer epsilon (exploration rate) decay
    agent._decay_epsilon_()

    # Log results of episode
    print(f"Episode {episode + 1}: Reward: {total_reward}")

# Log max reward for training session
print(f"Maximum reward: {max(rewards)}")