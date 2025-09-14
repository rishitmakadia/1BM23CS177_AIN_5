from collections import deque

class PuzzleState:
    def __init__(self, board, parent=None, move="", depth=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth  # number of moves from start

    def find_blank(self):
        return self.board.index(0)

    def get_moves(self):
        """Generate possible moves from current state"""
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
        """Reconstruct the path from start to current state"""
        node, p = self, []
        while node:
            p.append((node.move, node.board))
            node = node.parent
        return list(reversed(p))

    def print_board(self):
        """Print the board in 3x3 format"""
        for i in range(0, 9, 3):
            print(self.board[i:i+3])
        print()


def bfs(start, goal):
    start_state = PuzzleState(start)
    if start == goal:
        return start_state.path()

    queue = deque([start_state])
    visited = set()
    visited.add(tuple(start))

    while queue:
        current = queue.popleft()

        if current.board == goal:
            return current.path()

        for neighbor in current.get_moves():
            t_board = tuple(neighbor.board)
            if t_board not in visited:
                visited.add(t_board)
                queue.append(neighbor)
    return None


if __name__ == "__main__":
    initial_state = [
        1, 2, 3,
        4, 7, 5,
        6, 8, 0
    ]

    goal_state = [
        1, 2, 3,
        4, 0, 5,
        6, 7, 8
    ]

    solution = bfs(initial_state, goal_state)

    if solution:
        print(f"Solution found in {len(solution)-1} moves:\n")
        for idx, (move, board) in enumerate(solution):
            print(f"Step {idx}: Move: {move}")
            for i in range(0, 9, 3):
                print(board[i:i+3])
            print()
    else:
        print("No solution found.")
