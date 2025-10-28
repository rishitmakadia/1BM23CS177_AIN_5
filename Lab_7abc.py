import itertools
import re


def extract_variables(expressions):
    vars = set()
    pattern = r'\b[A-Z]\b'
    for expr in expressions:
        vars.update(re.findall(pattern, expr))
    return sorted(vars)


def eval_expr(expr, assignment):
    for var, val in assignment.items():
        expr = re.sub(r'\b' + var + r'\b', str(val), expr)

    expr = expr.replace('¬', ' not ')
    expr = expr.replace('∧', ' and ')
    expr = expr.replace('∨', ' or ')

    while '→' in expr:
        match = re.search(r'([^() ]+) *→ *([^() ]+)', expr)
        if not match:
            expr = expr.replace('→', ' <= ')
            break
        left = match.group(1)
        right = match.group(2)
        replacement = f'((not ({left})) or ({right}))'
        expr = expr[:match.start()] + replacement + expr[match.end():]

    try:
        return eval(expr)
    except Exception as e:
        raise ValueError(f"Error evaluating expression '{expr}': {e}")


def entails(KB, query):
    all_exprs = KB + [query]
    variables = extract_variables(all_exprs)

    truth_table = []

    # Generate all possible truth assignments
    for values in itertools.product([False, True], repeat=len(variables)):
        assignment = dict(zip(variables, values))

        KB_true = all(eval_expr(kb, assignment) for kb in KB)
        query_true = eval_expr(query, assignment)

        truth_table.append((assignment, KB_true, query_true))

        if KB_true and not query_true:
            return False, truth_table

    return True, truth_table


# Hardcoded KB and query as per your example
if __name__ == "__main__":
    # Define KB and Query for the problem
    KB = ['(A ∨ C)', '(B ∨ ¬C)']  # Knowledge Base (KB)
    query = '(A ∨ B)'  # Query (α)

    # Check entailment and get truth table
    entails_result, truth_table = entails(KB, query)

    # Output entailment result
    print(f"Does KB entail '{query}'? {entails_result}")

    # Print the truth table
    print("\nTruth Table:")
    header = ["Assignment", "KB Evaluation", "Query Evaluation"]
    print(f"{header[0]:<25} {header[1]:<20} {header[2]:<20}")

    for assignment, KB_true, query_true in truth_table:
        print(f"{str(assignment):<25} {str(KB_true):<20} {str(query_true):<20}")
