# Simple FOL-to-CNF converter (educational version)

# ---------------------------------------------------------
# Data structures
# ---------------------------------------------------------

class Var(str):
    pass

class Const(str):
    pass

class Func:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"{self.name}({', '.join(map(str, self.args))})"

class Pred:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"{self.name}({', '.join(map(str, self.args))})"

# Logical operators
class Not:
    def __init__(self, p):
        self.p = p

    def __repr__(self):
        return f"¬{self.p}"

class And:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"({self.left} ∧ {self.right})"

class Or:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"({self.left} ∨ {self.right})"

class Implies:
    def __init__(self, p, q):
        self.p = p
        self.q = q

class Forall:
    def __init__(self, var, body):
        self.var = var
        self.body = body

    def __repr__(self):
        return f"∀{self.var}.({self.body})"

class Exists:
    def __init__(self, var, body):
        self.var = var
        self.body = body

    def __repr__(self):
        return f"∃{self.var}.({self.body})"


# ---------------------------------------------------------
# CNF Conversion Functions
# ---------------------------------------------------------

def eliminate_implications(expr):
    if isinstance(expr, Implies):
        print(f"Eliminating Implication: {expr} → {Or(Not(eliminate_implications(expr.p)),
                  eliminate_implications(expr.q))}")
        return Or(Not(eliminate_implications(expr.p)),
                  eliminate_implications(expr.q))
    elif isinstance(expr, And):
        return And(eliminate_implications(expr.left),
                   eliminate_implications(expr.right))
    elif isinstance(expr, Or):
        return Or(eliminate_implications(expr.left),
                  eliminate_implications(expr.right))
    elif isinstance(expr, Not):
        return Not(eliminate_implications(expr.p))
    elif isinstance(expr, (Forall, Exists)):
        return type(expr)(expr.var, eliminate_implications(expr.body))
    else:
        return expr


def move_negations(expr):
    if isinstance(expr, Not):
        p = expr.p
        if isinstance(p, Not):
            return move_negations(p.p)
        if isinstance(p, And):
            return Or(move_negations(Not(p.left)), move_negations(Not(p.right)))
        if isinstance(p, Or):
            return And(move_negations(Not(p.left)), move_negations(Not(p.right)))
        if isinstance(p, Forall):
            return Exists(p.var, move_negations(Not(p.body)))
        if isinstance(p, Exists):
            return Forall(p.var, move_negations(Not(p.body)))
    if isinstance(expr, And):
        return And(move_negations(expr.left), move_negations(expr.right))
    if isinstance(expr, Or):
        return Or(move_negations(expr.left), move_negations(expr.right))
    if isinstance(expr, (Forall, Exists)):
        return type(expr)(expr.var, move_negations(expr.body))
    return expr


def skolemize(expr, scope_vars=None):
    if scope_vars is None:
        scope_vars = []

    if isinstance(expr, Forall):
        return Forall(expr.var, skolemize(expr.body, scope_vars + [expr.var]))

    if isinstance(expr, Exists):
        # Create Skolem func/constant
        if scope_vars:
            skolem = Func("f_" + expr.var, scope_vars)
        else:
            skolem = Const("c_" + expr.var)
        return skolemize(substitute(expr.body, expr.var, skolem), scope_vars)

    if isinstance(expr, And):
        return And(skolemize(expr.left, scope_vars),
                   skolemize(expr.right, scope_vars))
    if isinstance(expr, Or):
        return Or(skolemize(expr.left, scope_vars),
                  skolemize(expr.right, scope_vars))
    return expr


def substitute(expr, var, val):
    if isinstance(expr, Pred):
        new_args = [val if a == var else a for a in expr.args]
        return Pred(expr.name, new_args)
    if isinstance(expr, Func):
        new_args = [val if a == var else a for a in expr.args]
        return Func(expr.name, new_args)
    if isinstance(expr, And):
        return And(substitute(expr.left, var, val), substitute(expr.right, var, val))
    if isinstance(expr, Or):
        return Or(substitute(expr.left, var, val), substitute(expr.right, var, val))
    if isinstance(expr, Not):
        return Not(substitute(expr.p, var, val))
    return expr


def drop_universal(expr):
    if isinstance(expr, Forall):
        return drop_universal(expr.body)
    return expr


def distribute_or(expr):
    if isinstance(expr, And):
        return And(distribute_or(expr.left), distribute_or(expr.right))
    if isinstance(expr, Or):
        A, B = expr.left, expr.right
        if isinstance(A, And):
            return And(distribute_or(Or(A.left, B)),
                       distribute_or(Or(A.right, B)))
        if isinstance(B, And):
            return And(distribute_or(Or(A, B.left)),
                       distribute_or(Or(A, B.right)))
        return Or(distribute_or(A), distribute_or(B))
    return expr


# ---------------------------------------------------------
# Full pipeline
# ---------------------------------------------------------

def to_cnf(expr):
    print("Initial Expression:", expr)
    
    # Step 1: Eliminate implications
    expr1 = eliminate_implications(expr)
    print("\nAfter eliminating implications:", expr1)

    # Step 2: Move negations inward (NNF)
    expr2 = move_negations(expr1)
    print("\nAfter moving negations inward (NNF):", expr2)

    # Step 3: Skolemization
    expr3 = skolemize(expr2)
    print("\nAfter Skolemization:", expr3)

    # Step 4: Drop universal quantifiers
    expr4 = drop_universal(expr3)
    print("\nAfter dropping universal quantifiers:", expr4)

    # Step 5: Distribute OR over AND (CNF)
    expr5 = distribute_or(expr4)
    print("\nAfter distributing OR over AND (CNF):", expr5)

    return expr5


# ---------------------------------------------------------
# Example
# ---------------------------------------------------------

# ∀x (P(x) → ∃y Q(x,y))
formula = Forall("x",
            Implies(
                Pred("P", ["x"]),
                Exists("y", Pred("Q", ["x", "y"]))
            )
         )

cnf = to_cnf(formula)
print("\nFinal CNF:", cnf)
