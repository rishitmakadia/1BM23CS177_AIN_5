import heapq

class PuzzleState:
    def __init__(self, board, parent=None, move="", depth=0, cost=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost  # g(n) + h(n)

    def __lt__(self, other):
        return self.cost < other.cost

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
            print(self.board[i:i+3])  # Print rows of the board


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


# ----------------- A* Search -----------------
def a_star(start, goal, heuristic):
    open_list = []
    closed_set = set()
    start_state = PuzzleState(start)
    start_state.cost = heuristic(start_state, goal)
    heapq.heappush(open_list, start_state)

    while open_list:
        current = heapq.heappop(open_list)

        if current.board == goal:
            return current.path()

        closed_set.add(tuple(current.board))

        for neighbor in current.get_moves():
            if tuple(neighbor.board) in closed_set:
                continue
            neighbor.cost = neighbor.depth + heuristic(neighbor, goal)
            heapq.heappush(open_list, neighbor)

    return None


# ----------------- Example Run -----------------
# if __name__ == "__main__":
    initial_state = [1, 2, 3,
                     4, 7, 5,
                     6, 8, 0]

    goal_state =    [1, 2, 3,
                     4, 0, 5,
                     6, 7, 8]

    print("A* with Misplaced Tiles:")
    solution1 = a_star(initial_state, goal_state, misplaced_tiles)
    for move, state in solution1:
        print(f"Move: {move}")
        PuzzleState(state).print_board()  # Print the board as a matrix

    print("\nA* with Manhattan Distance:")
    solution2 = a_star(initial_state, goal_state, manhattan_distance)
    for move, state in solution2:
        print(f"Move: {move}")
        PuzzleState(state).print_board()  # Print the board as a matrix
if __name__ == "__main__":
    initial_state = [1, 2, 3,
                     4, 7, 5,
                     6, 8, 0]

    goal_state =    [1, 2, 3,
                     4, 0, 5,
                     6, 7, 8]

    print("A* with Misplaced Tiles:")
    solution1 = a_star(initial_state, goal_state, misplaced_tiles)
    for idx, (move, state) in enumerate(solution1):
        ps = PuzzleState(state)
        h = misplaced_tiles(ps, goal_state)
        g = idx  # depth = move number in path
        cost = g + h
        print(f"Move: {move}, Depth: {g}, Heuristic: {h}, Total cost: {cost}")
        ps.print_board()

    print("\nA* with Manhattan Distance:")
    solution2 = a_star(initial_state, goal_state, manhattan_distance)
    for idx, (move, state) in enumerate(solution2):
        ps = PuzzleState(state)
        h = manhattan_distance(ps, goal_state)
        g = idx  # depth
        cost = g + h
        print(f"Move: {move}, Depth: {g}, Heuristic: {h}, Total cost: {cost}")
        ps.print_board()

