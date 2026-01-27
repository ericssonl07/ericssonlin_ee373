import random
from pprint import pprint

seed = 42
random.seed(seed)

rewards = [
    0, # Root
    1, 0, # Level 1
    0, 3, 2, -1, # Level 2
    59, 36, 30, 40, 60, # Level 3
    30, -4, 59, 30, 59, 29 # Leaf nodes
]

actions = [
    (1, 2), # 0
    (3, 4), # 1
    (5, 6), # 2
    (7, 8), # 3
    (8, 9), # 4
    (9, 10), # 5
    (10, 11), # 6
    (12, 13), # 7
    (13, 14), # 8
    (14, 15), # 9
    (15, 16), # 10
    (16, 17), # 11
    None, None, None, None, None, None # Leaf nodes
]

def up(node):
    return actions[node][0]

def down(node):
    return actions[node][1]


# EXHAUSTIVE SEARCH
def dfs(node, path, reward):
    path = path + [node]
    if not actions[node]:  # Leaf node
        return [(path, reward + rewards[node])]
    paths = []
    up_node = up(node)
    down_node = down(node)
    paths.extend(dfs(up_node, path, reward + rewards[node]))
    paths.extend(dfs(down_node, path, reward + rewards[node]))
    return paths

paths = dfs(0, [], 0)
max_reward = max(paths, key=lambda x: x[1])
print("Exhaustive Search:")
print(f"Max Reward Path: {' -> '.join(map(str, max_reward[0]))} with Reward = {max_reward[1]}")
# Result: 0 -> 2 -> 6 -> 11 -> 16 with reward = 118



# DYNAMIC PROGRAMMING SOLUTION WITH BELLMAN OPTIMALITY EQUATION (VALUE ITERATION)
values = {node: random.uniform(0, 1) if node < 12 else 0 for node in range(18)}
gamma = 0.9
max_iterations = 10 # For the seed 42, the minimum to obtain to the optimal path is 3 iterations
iteration = 0
threshold = 1e-6
while iteration < max_iterations:
    # Bellman optimality: V(s) <- maxa (R(s, a)+gamma*V(s'))
    last_values = values.copy()
    iteration += 1
    print(f"\n{'='*20}\nIteration {iteration}\n{'='*20}\n")
    for node in range(18):
        if actions[node]:
            up_node = up(node)
            down_node = down(node)
            up_value = rewards[up_node] + gamma * values[up_node]
            down_value = rewards[down_node] + gamma * values[down_node]
            values[node] = max(up_value, down_value)
            print(f"Node {node}: up_value = {up_value}, down_value = {down_value}, selected = {values[node]}")
    # inf norm of value difference
    norm = max(abs(values[node] - last_values[node]) for node in range(18))
    print(f"\nValue difference inf-norm = {norm:.10f}")
    if norm < threshold:
        print(f"\n\n{'='*20}\nCONVERGED after {iteration} iterations with value difference inf-norm = {norm:.10f}\n{'='*20}\n")
        break

print("\nFinal Values after iterations:")
pprint(values)

print("\nOptimal Policy:")
for node in range(18):
    if actions[node]:
        up_node = up(node)
        down_node = down(node)
        up_value = rewards[up_node] + gamma * values[up_node]
        down_value = rewards[down_node] + gamma * values[down_node]
        best_action = 'up' if up_value > down_value else 'down'
        print(f"Node {node}: Best Action = {best_action} (Value = {values[node]})")

print("\nFollowing optimal policy from node 0:")
reward = 0
current_node = 0
while actions[current_node]:
    up_node = up(current_node)
    down_node = down(current_node)
    up_value = rewards[up_node] + gamma * values[up_node]
    down_value = rewards[down_node] + gamma * values[down_node]
    if up_value > down_value:
        print(f"{current_node} == UP ==> {up_node} ({'+' if rewards[up_node] >= 0 else ''}{rewards[up_node]})")
        reward += rewards[up_node]
        current_node = up_node
    else:
        print(f"{current_node} == DOWN ==> {down_node} ({'+' if rewards[down_node] >= 0 else ''}{rewards[down_node]})")
        reward += rewards[down_node]
        current_node = down_node
print(f"Total Reward: {reward}")
# Result: 0 == DOWN ==> 2 (+0)
#         2 == DOWN ==> 6 (-1)
#         6 == UP ==> 11 (+60)
#         11 == UP ==> 16 (+59)
#         Total Reward: 118