import math
import random

# Objective function: modify this for your problem
def objective_function(x):
    return x**2  # Simple example: minimize x^2

# Generate a neighbor solution near the current solution
def get_neighbor(x):
    step_size = random.uniform(-1, 1)  # small random change
    return x + step_size

# Acceptance probability function
def acceptance_probability(current_cost, new_cost, temperature):
    if new_cost < current_cost:
        return 1.0
    else:
        return math.exp((current_cost - new_cost) / temperature)

# Simulated Annealing algorithm
def simulated_annealing(initial_solution, initial_temp, final_temp, alpha, max_iterations):
    current_solution = initial_solution
    current_cost = objective_function(current_solution)
    best_solution = current_solution
    best_cost = current_cost
    temperature = initial_temp

    for i in range(max_iterations):
        # Generate new candidate solution
        new_solution = get_neighbor(current_solution)
        new_cost = objective_function(new_solution)

        # Decide whether to accept the new solution
        if random.random() < acceptance_probability(current_cost, new_cost, temperature):
            current_solution = new_solution
            current_cost = new_cost

        # Track the best solution found so far
        if new_cost < best_cost:
            best_solution = new_solution
            best_cost = new_cost

        # Cool down the temperature
        temperature *= alpha
        if temperature < final_temp:
            break

        # Optional: print progress
        print(f"Iteration {i+1}: Temp={temperature:.4f}, Current={current_solution:.4f}, Best={best_solution:.4f}")

    return best_solution, best_cost

# -------------------------
# Run the Simulated Annealing
# -------------------------
if __name__ == "__main__":
    initial_solution = 10          # starting point
    initial_temp = 100             # initial temperature
    final_temp = 0.001             # stopping temperature
    alpha = 0.95                   # cooling rate
    max_iterations = 500           # max steps

    best_solution, best_cost = simulated_annealing(
        initial_solution,
        initial_temp,
        final_temp,
        alpha,
        max_iterations
    )

    print("\n==============================")
    print(f"Best solution found: {best_solution}")
    print(f"Best cost: {best_cost}")
    print("==============================")
