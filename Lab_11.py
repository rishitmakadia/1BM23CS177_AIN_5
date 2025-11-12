from collections import defaultdict

# ---------- Step 1: Define Knowledge Base ----------
facts = set(["Human(Socrates)"])

# Rules are stored as (premises, conclusion)
rules = [
    (["Human(x)"], "Mortal(x)"),
    (["Mortal(x)"], "Dies(x)")
]

query = "Mortal(Socrates)"  # What we want to prove


# ---------- Step 2: Substitute variables ----------
def substitute(expr, var, val):
    return expr.replace(var, val)


# ---------- Step 3: Forward Chaining Function ----------
def forward_chain(facts, rules, query):
    new_facts = set(facts)
    added = True

    while added:
        added = False
        for premises, conclusion in rules:
            for fact in list(new_facts):
                # Check if any variable substitution is possible
                if '(' in fact:
                    const = fact[fact.find('(')+1:fact.find(')')]
                    temp = conclusion
                    for p in premises:
                        temp = substitute(temp, 'x', const)

                    if all(substitute(p, 'x', const) in new_facts for p in premises):
                        if temp not in new_facts:
                            print(f"Inferred: {temp}")
                            new_facts.add(temp)
                            added = True

    return query in new_facts


# ---------- Step 4: Run the reasoning ----------
print("Initial Facts:", facts)
result = forward_chain(facts, rules, query)
print("\nQuery:", query)
print("Result:", "PROVED" if result else "NOT PROVED")