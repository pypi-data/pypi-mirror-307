from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar, Optional, List, Union, Dict, Literal

import networkx as nx

from qiskit import QuantumCircuit, qasm3
from qiskit.quantum_info import SparsePauliOp
import matplotlib.pyplot as plt

from ionq.schemas.job import (
    JobRequest,
    JobDetails,
    WorkloadInput,
    QuantumFunctionInput,
    WorkloadType,
    HamiltonianEnergyQuantumFunction,
    HamiltonianEnergyData,
    HamiltonianPauliTerm,
    LinearConstraint,
    QuadraticConstraint,
    Ansatz,
    OptimizationWorkload,
    OptimizationMethod,
    OptimizationResult as OptimizationResultSchema,
    JobProgress,
)
from ionq.hybrid.utils import (
    qiskit_to_ionq_workload,
)


if TYPE_CHECKING:
    from .backend import Backend

R = TypeVar("R", bound="Result")
JobType = TypeVar("JobType", bound="Job")


class Job(ABC, Generic[R]):

    def __init__(self, id: str, details: JobRequest | JobDetails, backend: Backend):
        self.id = id
        self.details = details
        self.backend = backend

    @abstractmethod
    def results(self) -> R:
        pass


class Workload(ABC, Generic[JobType]):
    @abstractmethod
    def to_workload_input(
        self,
        params: Optional[List[float]] = None,
    ) -> WorkloadInput:
        pass

    @abstractmethod
    def create_job(self, id: str, job: JobRequest, backend: Backend) -> JobType:
        pass


class Result(ABC):
    @abstractmethod
    def plot_results(self, ax=None):
        pass


class QuantumFunctionResult(Result):
    def __init__(self, value: float, variance: float):
        self.value = value
        self.variance = variance

    def plot_results(self, ax=None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))

        ax.errorbar(
            ["Value"],
            [self.value],
            yerr=[self.variance],
            fmt="o",
            capsize=10,
        )
        ax.set_ylabel("Value")
        ax.set_title("Quantum Function Result")

        if ax is None:
            plt.show()


class QuantumFunctionJob(Job[QuantumFunctionResult]):

    def results(self) -> QuantumFunctionResult:
        if self.id is None:
            raise ValueError("Quantum Function not yet run")
        results_data = self.backend.results(self.id)

        return QuantumFunctionResult(
            value=results_data["value"],
            variance=results_data["variance"],
        )


class QuantumFunction(Workload[QuantumFunctionJob]):
    def __init__(
        self,
        ansatz: QuantumCircuit,
        hamiltonian: SparsePauliOp,
        linear_constraints: List[LinearConstraint] = [],
        quadratic_constraints: List[QuadraticConstraint] = [],
        penalty: Optional[float] = None,
    ):
        assert (
            ansatz.num_qubits == hamiltonian.num_qubits
        ), "Ansatz and Hamiltonian must have the same number of qubits"
        self.ansatz = self._prepare_ansatz(ansatz)
        self.hamiltonian = self._prepare_hamiltonian(hamiltonian)
        self.linear_constraints = linear_constraints
        self.quadratic_constraints = quadratic_constraints
        self.penalty = penalty

    def _prepare_ansatz(self, ansatz):
        return qasm3.dumps(ansatz)

    def _prepare_hamiltonian(
        self, hamiltonian: SparsePauliOp
    ) -> List[HamiltonianPauliTerm]:
        return [
            HamiltonianPauliTerm(
                pauli_string=pauli_string, coefficient=coefficient.real
            )
            for pauli_string, coefficient in hamiltonian.to_list()
        ]

    def to_workload_input(
        self,
        params: Optional[List[float]] = None,
    ) -> WorkloadInput:
        return QuantumFunctionInput(
            data=HamiltonianEnergyQuantumFunction(
                data=HamiltonianEnergyData(
                    hamiltonian=self.hamiltonian,
                    ansatz=Ansatz(data=self.ansatz),
                    linear_constraints=self.linear_constraints or None,
                    quadratic_constraints=self.quadratic_constraints or None,
                    penalty=self.penalty,
                ),
            ),
            params=params,
        )

    def create_job(
        self, id: str, job: JobRequest, backend: Backend
    ) -> QuantumFunctionJob:
        return QuantumFunctionJob(id, job, backend)


class OptimizationResult(Result):
    def __init__(
        self,
        minimum_value: float,
        optimal_parameters: List[float],
        progress: JobProgress,
        optimal_bitstrings: Optional[List[str]] = None,
        # graph: Optional[nx.Graph] = None,
        # variables: Optional[List[str]] = None,
        # quadratic_expression: Optional[str] = None,
    ):
        self.minimum_value = minimum_value
        self.optimal_parameters = optimal_parameters
        self.progress = progress.progress
        self.optimal_bitstrings = optimal_bitstrings
        # self.graph = graph
        # self.variables = variables
        # self.quadratic_expression = quadratic_expression

    # def bitstring_to_assignment(
    #     self, bitstring: str
    # ) -> Union[Dict[int, int], Dict[str, int]]:
    #     """Map each bit in the bitstring to a node in the graph or a variable."""
    #     if self.graph is not None:
    #         nodes = list(self.graph.nodes())
    #         return {node: int(bit) for node, bit in zip(nodes, bitstring)}
    #     elif self.variables is not None:
    #         return {var: int(bit) for var, bit in zip(self.variables, bitstring)}
    #     else:
    #         raise ValueError("Neither graph nor variables are provided.")

    # def evaluate_solution(self, bitstring: str) -> float:
    #     """Evaluate the solution on the graph or quadratic expression."""
    #     assignment = self.bitstring_to_assignment(bitstring)
    #     if self.graph is not None:
    #         # Evaluate for graph (e.g., Max-Cut)
    #         cut_value = 0
    #         for u, v, data in self.graph.edges(data=True):
    #             if assignment[u] != assignment[v]:
    #                 cut_value += data.get("weight", 1)
    #         return cut_value
    #     elif self.quadratic_expression is not None:
    #         # Evaluate quadratic expression
    #         expr = self.quadratic_expression
    #         for var, value in assignment.items():
    #             expr = expr.replace(var, str(value))
    #         return eval(expr)
    #     else:
    #         raise ValueError("Neither graph nor quadratic_expression is provided.")

    # def plot_assignment(self, bitstring: str):
    #     """Visualize the assignment of nodes based on the bitstring for graph problems."""
    #     if self.graph is None:
    #         raise ValueError("Graph not provided.")
    #     assignment = self.bitstring_to_assignment(bitstring)
    #     color_map = [
    #         "lightblue" if assignment[node] == 0 else "lightgreen"
    #         for node in self.graph.nodes()
    #     ]
    #     pos = nx.spring_layout(self.graph)
    #     nx.draw(
    #         self.graph, pos, node_color=color_map, with_labels=True, edge_color="gray"
    #     )
    #     plt.title(f"Graph Partition for Bitstring: {bitstring}")
    #     plt.show()

    def plot_results(self, ax=None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))

        x = [item.iteration for item in self.progress if item.iteration is not None]
        y = [item.value for item in self.progress if item.value is not None]
        ax.plot(x, y, label="Optimization Progress")

        # Mark the minimum energy point
        min_energy = self.minimum_value
        min_energy_iteration = x[y.index(min_energy)]
        opt_params = [round(param, 3) for param in self.optimal_parameters]
        label = (
            f"Minimum Value: {min_energy}\nOptimal Parameters: {opt_params}\n"
            f"Optimal Bitstrings: {self.optimal_bitstrings[:3] if self.optimal_bitstrings is not None else 'N/A'}"
        )

        ax.axvline(
            min_energy_iteration, color="r", linestyle="--", label="Optimal Iteration"
        )
        ax.text(
            min_energy_iteration, min_energy + 0.1 * (max(y) - min(y)), label, color="r"
        )
        ax.set_ylabel("Value")
        ax.set_xlabel("Iteration")
        ax.set_title("Optimization Result")
        ax.legend()

        if ax is None:
            plt.show()


class OptimizationJob(Job[OptimizationResult]):

    def results(self) -> OptimizationResult:
        if self.id is None:
            raise ValueError("Optimization Job not yet run")
        results = OptimizationResultSchema.parse_obj(self.backend.results(self.id))
        progress = self.backend.get_job_progress(self.id)

        return OptimizationResult(
            minimum_value=results.solution.minimum_value,
            optimal_parameters=results.solution.optimal_parameters,
            progress=progress,
            # optimal_bitstrings=optimal_bitstrings,
            # graph=self.graph,
            # variables=self.variables,
            # quadratic_expression=self.quadratic_expression,
        )

    # def _get_optimal_bitstrings(
    #     self, results: OptimizationResultSchema, progress: JobProgress
    # ) -> List[str]:

    #     # best_job_child = self.client.jobs.get_job(results.solution.job_id)

    #     # best_job_child_results = self.backend.(best_job_child.id)
    #     results_keys = sorted(
    #         best_job_child_results.probabilities,
    #         key=lambda x: best_job_child_results.probabilities[x],
    #         reverse=True,
    #     )
    #     return [
    #         bin(int(state))[2:].zfill(best_job_child.qubits) for state in results_keys
    #     ]


class Optimization(Workload[OptimizationJob]):
    def __init__(
        self,
        quantum_function: QuantumFunction,
        method: str,
        initial_params: Optional[List[Union[float, int]]] = None,
        log_interval: int = 1,
        options: Optional[dict] = None,
        maxiter: Optional[int] = None,
        graph: Optional[nx.Graph] = None,
        variables: Optional[List[str]] = None,
        quadratic_expression: Optional[str] = None,
    ):
        self.quantum_function = quantum_function
        self.method = method
        self.initial_params = initial_params
        self.log_interval = log_interval
        self.options = options
        self.maxiter = maxiter
        self.graph = graph
        self.variables = variables
        self.quadratic_expression = quadratic_expression

    def to_workload_input(
        self,
        params: Optional[List[float]] = None,
    ) -> WorkloadInput:
        return WorkloadInput(
            type=WorkloadType.optimization,
            data=OptimizationWorkload(
                quantum_function=self.quantum_function.to_workload_input().data,
                method=OptimizationMethod(self.method),
                initial_params=self.initial_params,
                log_interval=self.log_interval,
                options=self.options,
                maxiter=self.maxiter,
            ),
        )

    def create_job(self, id: str, job: JobRequest, backend: Backend) -> OptimizationJob:
        return OptimizationJob(id, job, backend)


class CircuitResult(Result):
    def __init__(
        self, probabilities: Dict[str, float], counts: Optional[Dict[str, int]] = None
    ):
        self.counts = counts
        self.probabilities = probabilities

    def top_candidates(self, n: Optional[int] = None) -> List[str]:
        if n is None:
            n = len(self.probabilities)
        return sorted(self.probabilities, key=self.probabilities.get, reverse=True)[:n]  # type: ignore

    def plot_results(self, ax=None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))

        ax.bar(list(self.probabilities.keys()), list(self.probabilities.values()))
        ax.set_ylabel("Probability")
        ax.set_xlabel("State")
        ax.set_title("Circuit Result")

        if ax is None:
            plt.show()


class CircuitJob(Job[CircuitResult]):

    def _get_counts(self, probabilities: Dict[str, float]) -> Optional[Dict[str, int]]:
        if self.details.shots is None:
            return None
        return {k: int(v * self.details.shots) for k, v in probabilities.items()}

    def results(self) -> List[CircuitResult]:
        if self.id is None:
            raise ValueError("Circuit Job not yet run")
        results = self.backend.results(self.id)

        # If the results contain multiple results, create a list of CircuitResult objects
        if all(isinstance(value, dict) for value in results.values()):
            return [
                CircuitResult(
                    probabilities=probabilities,
                    counts=self._get_counts(probabilities),
                )
                for probabilities in results.values()
            ]
        else:
            return [
                CircuitResult(
                    probabilities=results,
                    counts=self._get_counts(results),
                )
            ]


class Circuit(Workload[CircuitJob]):

    quantum_circuits: List[QuantumCircuit]
    gateset: Literal["qis", "native"]

    def __init__(
        self,
        quantum_circuits: Union[QuantumCircuit, List[QuantumCircuit]],
        gateset: Literal["qis", "native"] = "qis",
        name: Optional[str] = None,
    ):
        self.gateset = gateset
        if isinstance(quantum_circuits, QuantumCircuit):
            quantum_circuits.name = name or quantum_circuits.name
            self.quantum_circuits = [quantum_circuits]
        if isinstance(quantum_circuits, List):
            self.quantum_circuits = quantum_circuits

    def to_workload_input(
        self,
        params: Optional[List[float]] = None,
    ) -> WorkloadInput:
        return WorkloadInput(
            type=WorkloadType.circuit,
            data=qiskit_to_ionq_workload(self.quantum_circuits, self.gateset),
        )

    def create_job(self, id: str, request: JobRequest, backend: Backend) -> CircuitJob:
        return CircuitJob(id, request, backend)
