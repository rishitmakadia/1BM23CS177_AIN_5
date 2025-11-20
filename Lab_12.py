import math

# -----------------------------
# Pretty Print Tree (Level Order)
# -----------------------------
def print_tree(root):
    print("\n--- Game Tree (Level Order) ---")
    queue = [root]
    level = 0
    while queue:
        next_level = []
        print(f"Level {level}: ", end="")
        for node in queue:
            if isinstance(node, int):
                print(node, end="  ")
            else:
                print("[*]", end="  ")
                next_level.extend(node)
        print()
        queue = next_level
        level += 1
    print("--------------------------------\n")


# -----------------------------
# Alpha-Beta Pruning with Logging
# -----------------------------
node_id_counter = 1

def alphabeta(node, depth, alpha, beta, maximizing):
    global node_id_counter
    my_id = node_id_counter
    node_id_counter += 1

    # Terminal leaf
    if depth == 0 or isinstance(node, int):
        print(f"Leaf Node {my_id}: value={node}")
        return node

    if maximizing:
        value = -math.inf
        print(f"MAX Node {my_id}: depth={depth}, alpha={alpha}, beta={beta}")

        for child in node:
            child_value = alphabeta(child, depth - 1, alpha, beta, False)
            value = max(value, child_value)
            alpha = max(alpha, value)
            print(f"  MAX Node {my_id} updated: value={value}, alpha={alpha}, beta={beta}")

            if alpha >= beta:
                print(f"  >>> PRUNING at MAX Node {my_id}: alpha >= beta ({alpha} >= {beta})")
                break

        print(f"MAX Node {my_id} returns {value}")
        return value

    else:
        value = math.inf
        print(f"MIN Node {my_id}: depth={depth}, alpha={alpha}, beta={beta}")

        for child in node:
            child_value = alphabeta(child, depth - 1, alpha, beta, True)
            value = min(value, child_value)
            beta = min(beta, value)
            print(f"  MIN Node {my_id} updated: value={value}, alpha={alpha}, beta={beta}")

            if beta <= alpha:
                print(f"  >>> PRUNING at MIN Node {my_id}: beta <= alpha ({beta} <= {alpha})")
                break

        print(f"MIN Node {my_id} returns {value}")
        return value


# -----------------------------
# Build FULL BINARY TREE
# -----------------------------
def build_tree(values):
    """Build binary tree bottom-up from leaf list."""
    level = values
    while len(level) > 1:
        next_level = []
        for i in range(0, len(level), 2):
            next_level.append([level[i], level[i + 1]])
        level = next_level
    return level[0]


# -----------------------------
# MAIN PROGRAM
# -----------------------------
if __name__ == "__main__":
    depth = int(input("Enter depth of tree: "))

    leaf_count = 2 ** depth
    print(f"Enter {leaf_count} leaf node values:")

    leaves = list(map(int, input().split()))
    if len(leaves) != leaf_count:
        print("Error: incorrect number of leaf values.")
        exit()

    # Build tree
    tree = build_tree(leaves)

    # Print tree
    print_tree(tree)

    # Run Alpha-Beta
    print("\n--- Alpha-Beta Evaluation ---")
    best_value = alphabeta(tree, depth, -math.inf, math.inf, True)

    print("\nOptimal value found by Alpha–Beta:", best_value)
