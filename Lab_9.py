def is_variable(x):
    return isinstance(x, str) and x[0].islower()

def occurs_check(var, expr):
    if var == expr:
        return True
    elif isinstance(expr, tuple):
        return any(occurs_check(var, sub) for sub in expr[1])
    return False

def unify(x, y, theta=None):
    if theta is None:
        theta = {}

    if x == y:
        return theta
    elif is_variable(x):
        if occurs_check(x, y):
            return None
        theta[x] = y
        return {k: substitute(v, theta) for k, v in theta.items()}
    elif is_variable(y):
        return unify(y, x, theta)
    elif isinstance(x, tuple) and isinstance(y, tuple) and x[0] == y[0]:
        for a, b in zip(x[1], y[1]):
            theta = unify(substitute(a, theta), substitute(b, theta), theta)
            if theta is None:
                return None
        return theta
    else:
        return None

def substitute(expr, theta):
    if isinstance(expr, str):
        return theta.get(expr, expr)
    elif isinstance(expr, tuple):
        return (expr[0], [substitute(arg, theta) for arg in expr[1]])
    return expr


# ---------- Example ----------
# Represent P(a, x, f(g(y))) as ('P', ['a','x',('f',[('g',['y'])])])
# Represent P(z, f(z), f(u)) as ('P', ['z',('f',['z']),('f',['u'])])̥

expr1 = ('P', ['a', 'x', ('f', [('g', ['y'])])])
expr2 = ('P', ['z', ('f', ['z']), ('f', ['u'])])

result = unify(expr1, expr2)
print("Most General Unifier (MGU):", result)