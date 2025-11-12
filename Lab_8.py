import copy

# ---------- Knowledge Base and Query Setup ----------

# Each clause is a disjunction of literals
# Each literal is represented as a tuple: ('predicate', [args], is_negated)
# Example: ('Human', ['x'], False) means Human(x)
# Example: ('Mortal', ['x'], True) means ¬Mortal(x)

# Example KB:
# 1. ¬Human(x) ∨ Mortal(x)   (All humans are mortal)
# 2. Human(Socrates)
# Query: Mortal(Socrates)

KB = [
    [('Human', ['x'], True), ('Mortal', ['x'], False)],
    [('Human', ['Socrates'], False)]
]

query = ('Mortal', ['Socrates'], False)


# ---------- Unification Function ----------

def unify(x, y, theta=None):
    if theta is None:
        theta = {}
    if x == y:
        return theta
    elif isinstance(x, str) and x.islower():  # variable
        return unify_var(x, y, theta)
    elif isinstance(y, str) and y.islower():  # variable
        return unify_var(y, x, theta)
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        for xi, yi in zip(x, y):
            theta = unify(xi, yi, theta)
            if theta is None:
                return None̥
        return theta
    elif isinstance(x, tuple) and isinstance(y, tuple):
        return unify(list(x), list(y), theta)
    else:
        return None


def unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    elif x in theta:
        return unify(var, theta[x], theta)
    else:
        theta[var] = x
        return theta


# ---------- Apply Substitution ----------

def substitute(clause, theta):
    new_clause = []
    for (pred, args, neg) in clause:
        new_args = [theta.get(a, a) for a in args]
        new_clause.append((pred, new_args, neg))
    return new_clause


# ---------- Resolution ----------

def resolve(ci, cj):
    resolvents = []
    for (pi, args_i, neg_i) in ci:
        for (pj, args_j, neg_j) in cj:
            if pi == pj and neg_i != neg_j:
                theta = unify(args_i, args_j)
                if theta is not None:
                    new_ci = [lit for lit in ci if lit != (pi, args_i, neg_i)]
                    new_cj = [lit for lit in cj if lit != (pj, args_j, neg_j)]
                    merged = new_ci + new_cj
                    resolvent = substitute(merged, theta)
                    # remove duplicates
                    resolvent = [lit for lit in resolvent if lit not in []]
                    resolvents.append(resolvent)
    return resolvents


def resolution(KB, query):
    negated_query = [(query[0], query[1], not query[2])]
    clauses = KB + [negated_query]
    new = []
    print("\nInitial clauses:")
    for c in clauses:
        print(" ", c)̥

    while True:
        n = len(clauses)
        pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i + 1, n)]
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            for r in resolvents:
                if r == []:
                    print("\nDerived empty clause → Query proven")
                    return True
                new.append(r)
        if all(x in clauses for x in new):
            print("\nNo new clauses → Query cannot be proven")
            return False
        for c in new:
            if c not in clauses:
                clauses.append(c)


# ---------- Run the Resolution ----------

if __name__ == "__main__":
    print("Proving:", query)
    result = resolution(KB, query)
    print("\nResult:", "Proved" if result else "Not Proved")
