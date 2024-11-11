print("""import numpy as np
import random

# Define the maze environment
maze = np.array([
    [0, 0, 0, 0, 1],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
])

# Parameters
start = (0, 0)
goal = (4, 4)
actions = ["up", "down", "left", "right"]
action_dict = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

# Hyperparameters
alpha = 0.1      # Learning rate
gamma = 0.9      # Discount factor
epsilon = 0.1    # Exploration rate
episodes = 5000

# Q-table initialization
q_table = np.zeros((maze.shape[0], maze.shape[1], len(actions)))

# Helper functions
def is_valid_move(state):
    x, y = state
    return 0 <= x < maze.shape[0] and 0 <= y < maze.shape[1] and maze[x, y] == 0

def get_next_state(state, action):
    x, y = state
    dx, dy = action_dict[action]
    next_state = (x + dx, y + dy)
    return next_state if is_valid_move(next_state) else state

def get_reward(state):
    return 100 if state == goal else -1

# Training loop
for episode in range(episodes):
    state = start
    done = False
    while not done:
        # Epsilon-greedy action selection
        if random.uniform(0, 1) < epsilon:
            action_index = random.choice(range(len(actions)))  # Explore
        else:
            action_index = np.argmax(q_table[state[0], state[1]])  # Exploit
        action = actions[action_index]
        
        # Take action and observe result
        next_state = get_next_state(state, action)
        reward = get_reward(next_state)
        
        # Update Q-value using the Q-learning formula
        best_next_action = np.argmax(q_table[next_state[0], next_state[1]])
        q_table[state[0], state[1], action_index] += alpha * (
            reward + gamma * q_table[next_state[0], next_state[1], best_next_action] -
            q_table[state[0], state[1], action_index]
        )
        
        # Transition to the next state
        state = next_state
        
        # Check if goal is reached
        if state == goal:
            done = True

# Print the Q-values for each state
print("Q-Table after training:")
print(q_table)

# Test the agent
def test_agent(start):
    state = start
    path = [state]
    while state != goal:
        action_index = np.argmax(q_table[state[0], state[1]])
        action = actions[action_index]
        state = get_next_state(state, action)
        path.append(state)
    return path

# Display path
print("Path taken by the agent from start to goal:")
print(test_agent(start))""")
