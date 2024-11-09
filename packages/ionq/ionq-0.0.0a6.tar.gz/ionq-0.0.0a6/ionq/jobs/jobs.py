from __future__ import annotations
from abc import ABC, abstractmethod
from typing import (
    TYPE_CHECKING,
    Generic,
    TypeVar,
    Optional,
    List,
    Union,
    Dict,
    Literal,
    Any,
)

import networkx as nx

import matplotlib.pyplot as plt

from ionq.schemas.job import (
    JobRequest,
    JobDetails,
    WorkloadInput,
    QuantumFunctionInput,
    WorkloadType,
    HamiltonianEnergyQuantumFunction,
    HamiltonianEnergyData,
    Hamiltonian,
    LinearConstraint,
    QuadraticConstraint,
    Ansatz,
    OptimizationWorkload,
    OptimizationMethod,
    OptimizationResult as OptimizationResultSchema,
    JobProgress,
    CircuitWorkload,
    GateSet,
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
        ansatz: Ansatz,
        hamiltonian: Hamiltonian,
        linear_constraints: List[LinearConstraint] = [],
        quadratic_constraints: List[QuadraticConstraint] = [],
        penalty: Optional[float] = None,
    ):
        assert (
            ansatz.num_qubits == hamiltonian.num_qubits
        ), "Ansatz and Hamiltonian must have the same number of qubits"
        self.ansatz = ansatz
        self.hamiltonian = hamiltonian
        self.linear_constraints = linear_constraints
        self.quadratic_constraints = quadratic_constraints
        self.penalty = penalty

    def to_workload_input(
        self,
        params: Optional[List[float]] = None,
    ) -> WorkloadInput:
        return QuantumFunctionInput(
            data=HamiltonianEnergyQuantumFunction(
                data=HamiltonianEnergyData(
                    hamiltonian=self.hamiltonian.terms,
                    ansatz=self.ansatz,
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
    ):
        self.minimum_value = minimum_value
        self.optimal_parameters = optimal_parameters
        self.progress = progress.progress
        self.optimal_bitstrings = optimal_bitstrings

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
        )


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

    gateset: Literal["qis", "native"]

    def __init__(
        self,
        circuits: List[Dict[str, Any]],
        format: str = "ionq.circuit.v0",
        gateset: Literal["qis", "native"] = "qis",
        qubits: Optional[int] = None,
        name: Optional[str] = None,
    ):
        self.circuits = circuits
        self.format = format
        self.gateset = gateset
        self.qubits = qubits
        self.name = name

    def to_workload_input(
        self,
        params: Optional[List[float]] = None,
    ) -> WorkloadInput:
        return WorkloadInput(
            type=WorkloadType.circuit,
            data=CircuitWorkload(
                format=self.format,
                gateset=GateSet(self.gateset),
                qubits=self.qubits,
                circuits=self.circuits,
            ),
        )

    def create_job(self, id: str, request: JobRequest, backend: Backend) -> CircuitJob:
        return CircuitJob(id, request, backend)
