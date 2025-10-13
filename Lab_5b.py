import random

def conflicts(state):
    """Count number of pairs of queens attacking each other."""
    n = len(state)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                count += 1
    return count

def generate_neighbors(state):
    """Generate all neighbors by moving one queen to another row in its column."""
    neighbors = []
    n = len(state)
    for col in range(n):
        for row in range(n):
            if row != state[col]:
                neighbor = state.copy()
                neighbor[col] = row
                neighbors.append(neighbor)
    return neighbors

def print_board(state):
    """Print the board configuration."""
    n = len(state)
    for row in range(n):
        line = ""
        for col in range(n):
            if state[col] == row:
                line += " Q "
            else:
                line += " . "
        print(line)
    print("\n")

def hill_climbing_n_queens(n, max_iterations=1000, max_restarts=50):
    def random_state():
        return [random.randint(0, n - 1) for _ in range(n)]

    current_state = random_state()
    current_conflicts = conflicts(current_state)

    print("Initial board:")
    print_board(current_state)
    print(f"Initial conflicts: {current_conflicts}\n")

    restarts = 0
    iteration = 0

    while restarts < max_restarts:
        improved = True
        while improved and iteration < max_iterations:
            iteration += 1
            neighbors = generate_neighbors(current_state)
            neighbor_conflicts = [conflicts(neigh) for neigh in neighbors]

            min_conflicts = min(neighbor_conflicts)
            min_indices = [i for i, val in enumerate(neighbor_conflicts) if val == min_conflicts]

            if min_conflicts < current_conflicts:
                chosen_index = random.choice(min_indices)
                next_state = neighbors[chosen_index]
                # Find which column changed and rows before/after
                for col in range(n):
                    if current_state[col] != next_state[col]:
                        moved_col = col
                        old_row = current_state[col]
                        new_row = next_state[col]
                        break
                direction = "up" if new_row < old_row else "down"
                print(f"Iteration {iteration}: Moved queen in column {moved_col} from row {old_row} {direction} to row {new_row}, conflicts {min_conflicts}")
                current_state = next_state
                current_conflicts = min_conflicts

            elif min_conflicts == current_conflicts:
                chosen_index = random.choice(min_indices)
                next_state = neighbors[chosen_index]
                # Find which column changed and rows before/after
                for col in range(n):
                    if current_state[col] != next_state[col]:
                        moved_col = col
                        old_row = current_state[col]
                        new_row = next_state[col]
                        break
                direction = "up" if new_row < old_row else "down"
                print(f"Iteration {iteration}: Moved queen in column {moved_col} from row {old_row} {direction} to row {new_row} (equal objective), conflicts {min_conflicts}")
                current_state = next_state
                current_conflicts = min_conflicts

            else:
                print(f"Iteration {iteration}: Local optimum reached with conflicts {current_conflicts}")
                improved = False

        if current_conflicts == 0:
            print("\nGlobal optimum found!")
            break

        restarts += 1
        current_state = random_state()
        current_conflicts = conflicts(current_state)
        print(f"\nRestart {restarts}: New random state with conflicts {current_conflicts}")

    print("\nFinal board:")
    print_board(current_state)
    print(f"Final conflicts: {current_conflicts}")
    print(f"Total iterations: {iteration}")
    print(f"Total restarts: {restarts}")
    return current_state

# Example: Solve 8-Queens
n = 5
hill_climbing_n_queens(n)
