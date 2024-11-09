from typing import Optional
from abc import ABC, abstractmethod

from qiskit import QuantumCircuit
from ionq.jobs import QuantumFunction


class Problem(ABC):
    """
    An abstract class to model an optimization problem.

    The constructor, defined in a child class, ingests problem instance data.
    Then the class's main method, :meth:`.quantum_function_objective`
    constructs the problem's objective function as a :class:`.QuantumFunction`
    object that can be passed to a hybrid solver for optimization.
    """

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def quantum_function_objective(
        self,
        ansatz: Optional[QuantumCircuit] = None,
        **kwargs,
    ) -> QuantumFunction:
        pass
