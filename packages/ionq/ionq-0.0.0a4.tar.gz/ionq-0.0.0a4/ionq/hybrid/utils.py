import numpy as np
import sympy as sp
import random
import json
import gzip
import base64
from typing import Union, List, Literal, Tuple, Dict, Any
import networkx as nx
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit import controlledgate as q_cgates
from qiskit.circuit.library import standard_gates as q_gates
from ionq.schemas.job import GateSet, CircuitWorkload


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


# IonQ-specific constants and mappings
ionq_basis_gates = [
    "ccx",
    "ch",
    "cnot",
    "cp",
    "crx",
    "cry",
    "crz",
    "csx",
    "cx",
    "cy",
    "cz",
    "h",
    "i",
    "id",
    "mcp",
    "mcphase",
    "mct",
    "mcx",
    "mcx_gray",
    "measure",
    "p",
    "rx",
    "rxx",
    "ry",
    "ryy",
    "rz",
    "rzz",
    "s",
    "sdg",
    "swap",
    "sx",
    "sxdg",
    "t",
    "tdg",
    "toffoli",
    "x",
    "y",
    "z",
]

ionq_api_aliases = {
    "cp": "cz",
    "csx": "cv",
    "mcphase": "cz",
    "cx": "x",  # TODO: replace all controlled gates with their single-qubit counterparts
    "ccx": "x",
    "mcx": "x",
    "mcx_gray": "x",
    "tdg": "ti",
    "p": "z",
    "rxx": "xx",
    "ryy": "yy",
    "rzz": "zz",
    "sdg": "si",
    "sx": "v",
    "sxdg": "vi",
}

multi_target_uncontrolled_gates = (
    q_gates.SwapGate,
    q_gates.RXXGate,
    q_gates.RYYGate,
    q_gates.RZZGate,
)


def qiskit_circ_to_ionq_circ(input_circuit: QuantumCircuit):
    """Converts Qiskit circuit to IonQ instructions format."""
    output_circuit = []
    num_meas = 0
    meas_map = [None] * len(input_circuit.clbits)
    for instruction, qargs, cargs in input_circuit.data:
        instruction_name = instruction.name
        if instruction_name == "measure":
            meas_map[input_circuit.clbits.index(cargs[0])] = input_circuit.qubits.index(
                qargs[0]
            )
            num_meas += 1
            continue
        if instruction_name == "id":
            continue
        if instruction_name not in ionq_basis_gates:
            raise ValueError(f"Unsupported instruction: {instruction_name}")

        targets = [input_circuit.qubits.index(qargs[0])]
        if isinstance(instruction, multi_target_uncontrolled_gates):
            targets.extend(input_circuit.qubits.index(q) for q in qargs[1:])

        converted = {
            "gate": ionq_api_aliases.get(instruction_name, instruction_name),
            "targets": targets,
        }
        if len(instruction.params) > 0:
            converted["rotation"] = float(instruction.params[0])
        if isinstance(instruction, q_cgates.ControlledGate):
            converted["controls"] = [input_circuit.qubits.index(qargs[0])]
            converted["targets"] = [input_circuit.qubits.index(qargs[1])]

        output_circuit.append(converted)

    return output_circuit, num_meas, meas_map


def get_register_sizes_and_labels(
    registers: List[Union[QuantumRegister, ClassicalRegister]]
):
    """Returns sizes and labels for Qiskit registers."""
    sizes, labels = [], []
    for register in registers:
        for index, _ in enumerate(register):
            size, label = [register.name, register.size], [register.name, index]
            if size not in sizes:
                sizes.append(size)
            labels.append(label)
    return sizes, labels


def compress_to_metadata_string(metadata: Union[dict, list]):
    """Compresses metadata to a base64-encoded string."""
    serialized = json.dumps(metadata)
    compressed = gzip.compress(serialized.encode("utf-8"))
    encoded = base64.b64encode(compressed)
    return encoded.decode()


class SafeEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle non-JSON-safe objects."""

    def default(self, o):
        try:
            return super().default(o)
        except Exception:
            return str(o)


def qiskit_to_ionq_workload(
    circuit: List[QuantumCircuit],
    gateset: Literal["qis", "native"],
) -> CircuitWorkload:
    """Convert a Qiskit circuit to an IonQ-compatible Circuit workload"""
    ionq_circs: List[Tuple[List[Dict[str, Any]], list, str]] = []
    for circ in circuit:
        ionq_circ, _, meas_map = qiskit_circ_to_ionq_circ(circ)
        ionq_circs.append((ionq_circ, meas_map, circ.name))

    return CircuitWorkload(
        format="ionq.circuit.v0",
        gateset=GateSet(gateset),
        qubits=max(c.num_qubits for c in circuit),
        circuits=[
            {"name": name, "circuit": circuit, "registers": {"meas_mapped": mapping}}
            for circuit, mapping, name in ionq_circs
        ],
    )
