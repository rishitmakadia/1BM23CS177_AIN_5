import itertools
import re


def extract_variables(expressions):
    """Extracts all unique, single-letter uppercase variables from a list of logical expressions."""
    vars = set()
    # Matches a single uppercase letter word boundary (to avoid 'and', 'or', 'not' as variables)
    pattern = r'\b[A-Z]\b'
    for expr in expressions:
        vars.update(re.findall(pattern, expr))
    return sorted(vars)


def eval_expr(expr, assignment):
    """
    Evaluates a logical expression given a truth assignment.
    It converts logical symbols (¬, ∧, ∨, →) to Python operators (not, and, or, negation/implication).
    """

    # 1. Substitute variable assignments (e.g., 'P' -> 'True')
    for var, val in assignment.items():
        # Use word boundaries to ensure 'P' isn't confused with part of 'OR' or 'AND' (though they are lower-cased)
        expr = re.sub(r'\b' + var + r'\b', str(val), expr)

    # 2. Substitute Negation (¬) FIRST
    # This must happen before implication (→) substitution to avoid '¬True' or '¬False' being
    # incorrectly parsed by the implication logic.
    expr = expr.replace('¬', ' not ')
    expr = expr.replace('-', ' → ')
    # 3. Substitute Conjunction (∧) and Disjunction (∨)
    expr = expr.replace('∧', ' and ')
    expr = expr.replace('∨', ' or ')

    # 4. Substitute Implication (→): 'A → B' is equivalent to '¬A ∨ B'
    # Use a loop to handle multiple implications in one expression.
    # The regex matches an expression on the left and right of '→'.
    while '→' in expr:
        # Match groups of any characters (including 'not', 'True', 'False', parentheses, and spaces)
        # to correctly capture the antecedent and consequent.
        match = re.search(r'([^() ]+|[() ])+ *→ *([^() ]+|[() ])+', expr)

        # A simpler, more robust regex to find the next implication:
        # Match anything on the left and right, stopping at the operator.
        match = re.search(r'(.+?) *→ *(.+)', expr)

        if not match:
            # If the complex search fails, fall back to Python's less-strict operator
            expr = expr.replace('→', ' <= ')
            break

        left = match.group(1).strip()
        right = match.group(2).strip()

        # Construct the replacement: ¬A ∨ B
        replacement = f'((not ({left})) or ({right}))'

        # Replace the first occurrence of the implication
        expr = expr.replace(f'{left} → {right}', replacement, 1)

    try:
        # Evaluate the final, pure Python boolean expression
        return eval(expr)
    except Exception as e:
        # This block catches the original error and provides the corrected context
        raise ValueError(f"Error evaluating expression '{expr}': {e}")


def entails(KB, query):
    """Checks if the Knowledge Base (KB) entails the query using the truth table method."""
    all_exprs = KB + [query]
    variables = extract_variables(all_exprs)

    # Iterate through all possible truth assignments for the variables
    for values in itertools.product([False, True], repeat=len(variables)):
        assignment = dict(zip(variables, values))

        # Check if the KB is true under the current assignment
        try:
            KB_true = all(eval_expr(kb, assignment) for kb in KB)
        except ValueError as e:
            # Re-raise with a specific context (which assignment caused the issue)
            print(f"Error during KB evaluation with assignment {assignment}: {e}")
            raise

        # If KB is true, check if the query is also true (i.e., KB → Query is True)
        if KB_true:
            try:
                query_true = eval_expr(query, assignment)
            except ValueError as e:
                print(f"Error during query evaluation with assignment {assignment}: {e}")
                raise

            # If KB is true but the query is false, we found a counter-model, so KB does not entail the query.
            if not query_true:
                return False

    # If no counter-model was found after checking all assignments, KB entails the query.
    return True


if __name__ == "__main__":
    # The eval() on input is unsafe in a real-world application, but used here to match the user's apparent usage pattern.
    KB_input = input(
        "Enter Knowledge Base (KB) in the form of a list of logical formulas (e.g., ['(A ∨ C)', '(B ∨ ¬C)']): ")
    KB = eval(KB_input)

    query1 = input("Enter query 1 (e.g., 'R'): ")
    query2 = input("Enter query 2 (e.g., 'R → P'): ")
    query3 = input("Enter query 3 (e.g., 'Q → R'): ")

    # The actual execution with the user's input:
    # KB = ['(Q → P)', '(P → ¬Q)', '(Q ∨ R)']
    # query1 = 'R'
    # query2 = 'R → P'
    # query3 = 'Q → R'

    print(f"\n--- Entailment Results ---")

    # Run the entailment checks
    try:
        print(f"Does KB entail '{query1}'? {entails(KB, query1)}")
        print(f"Does KB entail '{query2}'? {entails(KB, query2)}")
        print(f"Does KB entail '{query3}'? {entails(KB, query3)}")
    except ValueError as e:
        print(f"\n[Error] The program could not complete due to an evaluation error: {e}")