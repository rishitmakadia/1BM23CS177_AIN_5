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

    for values in itertools.product([False, True], repeat=len(variables)):
        assignment = dict(zip(variables, values))

        KB_true = all(eval_expr(kb, assignment) for kb in KB)

        if KB_true and not eval_expr(query, assignment):
            return False

    return True


if __name__ == "__main__":
    KB = input("Enter Knowledge Base (KB) in the form of a list of logical formulas (e.g., ['(A ∨ C)', '(B ∨ ¬C)']): ")
    KB = eval(KB)

    query1 = input("Enter query 1 (e.g., 'R'): ")
    query2 = input("Enter query 2 (e.g., 'R → P'): ")
    query3 = input("Enter query 3 (e.g., 'Q → R'): ")

    print(f"Does KB entail '{query1}'? {entails(KB, query1)}")
    print(f"Does KB entail '{query2}'? {entails(KB, query2)}")
    print(f"Does KB entail '{query3}'? {entails(KB, query3)}")
