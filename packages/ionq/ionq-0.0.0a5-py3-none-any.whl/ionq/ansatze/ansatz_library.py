from typing import Optional

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector


def BrickworkLayoutAnsatz(
    num_qubits,
    num_layers=2,
    params=None,
    initial_state: Optional[QuantumCircuit] = None,
):
    # Construct a variational ansatz with a brickwork layout structure.
    qc = QuantumCircuit(num_qubits)
    if initial_state:
        qc = initial_state.compose(qc)
        if not qc:
            raise ValueError("Error when adding initial state.")
        qc.barrier()
    else:
        qc.h(range(num_qubits))

    if params is None:
        num_params = np.ceil(num_layers * (num_qubits - 1) / 2).astype(int)
        params = ParameterVector("θ", num_params)
    param_it = iter(params)

    for layer in range(num_layers):
        start_qubit = layer % 2
        for qubit in range(start_qubit, num_qubits - 1, 2):
            qc.cx(qubit, qubit + 1)
            qc.ry(next(param_it), qubit + 1)

    return qc
