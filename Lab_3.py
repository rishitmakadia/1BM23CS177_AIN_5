from collections import deque

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

MOVES = {
    'up': -3,
    'down': 3,
    'left': -1,
    'right': 1
}

def is_valid_move(blank_idx, move):
    if move == 'left' and blank_idx % 3 == 0:
        return False
    if move == 'right' and blank_idx % 3 == 2:
        return False
    if move == 'up' and blank_idx < 3:
        return False
    if move == 'down' and blank_idx > 5:
        return False
    return True

def get_successors(state):
    successors = []
    blank_idx = state.index(0)
    
    for move in MOVES:
        if is_valid_move(blank_idx, move):
            swap_idx = blank_idx + MOVES[move]
            new_state = list(state)
            new_state[blank_idx], new_state[swap_idx] = new_state[swap_idx], new_state[blank_idx]
            successors.append(tuple(new_state))
    return successors

def DLS(state, goal, limit, path, visited, last_state_holder):
    last_state_holder[0] = state
    
    if state == goal:
        return path
    if limit == 0:
        return None
    
    visited.add(state)
    
    for successor in get_successors(state):
        if successor not in visited:
            result = DLS(successor, goal, limit - 1, path + [successor], visited, last_state_holder)
            if result is not None:
                return result
    
    visited.remove(state)
    return None

def IDDFS(start, goal):
    depth = 0
    iteration = 1
    while True:
        visited = set()
        last_state_holder = [start]
        path = DLS(start, goal, depth, [start], visited, last_state_holder)
        
        print(f"Iteration {iteration} completed at Depth limit = {depth}")
        print("Last visited puzzle state in this iteration:")
        print_puzzle(last_state_holder[0])
        
        if path is not None:
            return path
        depth += 1
        iteration += 1

def print_puzzle(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

if __name__ == "__main__":
    start_state = (1, 2, 4,
                   0, 8, 6,
                   7, 5, 3)
    
    print("Starting state:")
    print_puzzle(start_state)
    
    solution_path = IDDFS(start_state, GOAL_STATE)
    
    print(f"Solution found in {len(solution_path) - 1} moves:")
    for step in solution_path:
        print_puzzle(step)
