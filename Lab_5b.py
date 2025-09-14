class PuzzleState:
    def __init__(self, board, parent=None, move="", depth=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth

    def find_blank(self):
        return self.board.index(0)

    def get_moves(self):
        """Generate possible moves"""
        blank = self.find_blank()
        moves = []
        row, col = divmod(blank, 3)
        directions = {
            "Up": (row - 1, col),
            "Down": (row + 1, col),
            "Left": (row, col - 1),
            "Right": (row, col + 1)
        }
        for move, (r, c) in directions.items():
            if 0 <= r < 3 and 0 <= c < 3:
                new_blank = r * 3 + c
                new_board = self.board[:]
                new_board[blank], new_board[new_blank] = new_board[new_blank], new_board[blank]
                moves.append(PuzzleState(new_board, self, move, self.depth + 1))
        return moves

    def path(self):
        """Reconstruct solution path"""
        node, p = self, []
        while node:
            p.append((node.move, node.board))
            node = node.parent
        return list(reversed(p))

    def print_board(self):
        """Print the board in 3x3 matrix form"""
        for i in range(0, 9, 3):
            print(self.board[i:i+3])
        print()


# ----------------- Heuristics -----------------
def misplaced_tiles(state, goal):
    return sum(1 for i in range(9) if state.board[i] != 0 and state.board[i] != goal[i])

def manhattan_distance(state, goal):
    dist = 0
    for i in range(9):
        if state.board[i] != 0:
            r1, c1 = divmod(i, 3)
            r2, c2 = divmod(goal.index(state.board[i]), 3)
            dist += abs(r1 - r2) + abs(c1 - c2)
    return dist


# ----------------- Hill Climbing Algorithm -----------------
def hill_climbing(start, goal, heuristic):
    current = PuzzleState(start)
    current_heuristic = heuristic(current, goal)

    while True:
        neighbors = current.get_moves()
        best_neighbor = None
        best_heuristic = float('inf')

        for neighbor in neighbors:
            h = heuristic(neighbor, goal)
            if h < best_heuristic:
                best_heuristic = h
                best_neighbor = neighbor

        # Stop if no better neighbor found (local optimum)
        if best_heuristic >= current_heuristic:
            return current.path()

        current = best_neighbor
        current_heuristic = best_heuristic


# ----------------- Example Run -----------------
if __name__ == "__main__":
    initial_state = [1, 2, 3,
                     4, 7, 5,
                     6, 8, 0]

    goal_state =    [1, 2, 3,
                     4, 0, 5,
                     6, 7, 8]

    print("Hill Climbing with Manhattan Distance:")
    solution = hill_climbing(initial_state, goal_state, manhattan_distance)

    for move, state in solution:
        h_value = manhattan_distance(PuzzleState(state), goal_state)
        print(f"Move: {move}, Heuristic: {h_value}")
        PuzzleState(state).print_board()
