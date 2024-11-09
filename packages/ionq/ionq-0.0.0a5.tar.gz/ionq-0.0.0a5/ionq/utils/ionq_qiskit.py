from typing import List, Literal, Tuple, Dict, Any
from qiskit import QuantumCircuit, qasm3
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit import controlledgate as q_cgates
from qiskit.circuit.library import standard_gates as q_gates
from ionq.jobs import Circuit
from ionq.schemas.job import Ansatz, Hamiltonian, HamiltonianPauliTerm


def to_ansatz(
    ansatz: QuantumCircuit,
):
    return Ansatz(
        format="qasm",
        data=qasm3.dumps(ansatz),
    )


def to_hamiltonian(
    hamiltonian: SparsePauliOp,
) -> Hamiltonian:

    return Hamiltonian(
        [
            HamiltonianPauliTerm(
                pauli_string=pauli_string, coefficient=coefficient.real
            )
            for pauli_string, coefficient in hamiltonian.to_list()
        ],
        hamiltonian.num_qubits,
    )


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


def _qiskit_circ_to_ionq_circ(input_circuit: QuantumCircuit):
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


def to_circuit(
    circuit: List[QuantumCircuit],
    gateset: Literal["qis", "native"] = "qis",
) -> Circuit:
    """Convert a Qiskit circuit to an IonQ-compatible Circuit workload"""
    ionq_circs: List[Tuple[List[Dict[str, Any]], list, str]] = []
    for circ in circuit:
        ionq_circ, _, meas_map = _qiskit_circ_to_ionq_circ(circ)
        ionq_circs.append((ionq_circ, meas_map, circ.name))

    return Circuit(
        format="ionq.circuit.v0",
        gateset=gateset,
        qubits=max(c.num_qubits for c in circuit),
        circuits=[
            {"name": name, "circuit": circuit, "registers": {"meas_mapped": mapping}}
            for circuit, mapping, name in ionq_circs
        ],
    )
