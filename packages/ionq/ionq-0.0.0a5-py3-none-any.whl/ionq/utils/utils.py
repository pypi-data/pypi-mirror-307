import numpy as np
import sympy as sp
import random
import json
import networkx as nx
from qiskit.quantum_info import SparsePauliOp


def generate_random_quadratic_equation(
    num_variables, coeff_range=(-3, 3), constant_range=(-3, 3)
):
    # Create symbolic variables x1, x2, ..., xn
    variables = [sp.Symbol(f"x{i+1}") for i in range(num_variables)]

    # Generate random coefficients for the linear and quadratic terms
    linear_terms = [random.randint(*coeff_range) * var for var in variables]
    quadratic_terms = [
        random.randint(*coeff_range) * var1 * var2
        for i, var1 in enumerate(variables)
        for var2 in variables[i:]
    ]

    # Generate random constant term
    constant = random.randint(*constant_range)

    # Construct the quadratic equation
    quadratic_expr = sum(linear_terms) + sum(quadratic_terms)
    equation = sp.Eq(quadratic_expr, constant)

    return f"{sp.simplify(equation.lhs)} = {equation.rhs}"


def graph_to_qubo(graph: nx.Graph) -> np.ndarray:
    num_nodes = graph.number_of_nodes()
    Q = np.zeros((num_nodes, num_nodes))

    for u, v, data in graph.edges(data=True):
        weight = data.get("weight", 1)  # Assume a default weight of 1 if not specified
        Q[u, v] -= weight
        Q[v, u] -= weight
        Q[u, u] += weight
        Q[v, v] += weight

    return Q


def qubo_obj_to_ising_ham(Q: np.ndarray):
    num_qubits = Q.shape[0]
    hamiltonian = [("I" * num_qubits, 1 / 4 * (Q.sum() + Q.trace()))]

    # Linear terms
    for j, sj in enumerate(filter(lambda v: not np.isclose(v, 0), Q.sum(axis=1))):
        lin = "".join("I" if k != j else "Z" for k in reversed(range(num_qubits)))
        hamiltonian += [(lin, -1 / 2 * sj)]

    # Quadratic terms
    for i in range(num_qubits):
        for j in range(i + 1, num_qubits):
            if not np.isclose(Q[i, j], 0):
                quad = "".join(
                    "I" if k not in [i, j] else "Z" for k in reversed(range(num_qubits))
                )
                hamiltonian += [(quad, 1 / 2 * Q[i, j])]
    return SparsePauliOp.from_list(hamiltonian)


class SafeEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle non-JSON-safe objects."""

    def default(self, o):
        try:
            return super().default(o)
        except Exception:
            return str(o)
