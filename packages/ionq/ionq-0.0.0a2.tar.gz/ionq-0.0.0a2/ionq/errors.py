class IonQAPIError(Exception):
    """Base class for all API errors."""

    def __init__(self, error=None):
        super().__init__(error or "An unspecified error occurred.")


class UserCancelledError(Exception):
    """Exception raised when the user cancels an operation."""

    def __init__(self, error=None):
        super().__init__(error or "The user cancelled the operation.")


class PreflightError(IonQAPIError):
    """Exception raised for errors that occur before execution starts."""

    pass


class InternalError(IonQAPIError):
    """Exception raised for internal errors within the API."""

    pass


class TooManyGates(IonQAPIError):
    """Exception raised when too many gates are requested."""

    pass


class SystemCancel(IonQAPIError):
    """Exception raised when a system administrator cancels a process."""

    pass


class QuotaExhaustedError(IonQAPIError):
    """Exception raised when the quota for resources has been exhausted."""

    pass


class TimedOut(IonQAPIError):
    """Exception raised when the operation times out."""

    pass


class TooLongPredictedExecutionTime(IonQAPIError):
    """Exception raised when the predicted execution time is too long."""

    pass


class CircuitTooLarge(IonQAPIError):
    """Exception raised when the circuit size exceeds the limit."""

    pass


class TooManyShots(IonQAPIError):
    """Exception raised when the number of shots exceeds the limit."""

    pass


class ContractExpiredError(IonQAPIError):
    """Exception raised when the contract has expired."""

    pass


class SimulationTimeout(IonQAPIError):
    """Exception raised when a simulation times out."""

    pass


class OptimizationError(IonQAPIError):
    """Exception raised during optimization process errors."""

    pass


class UnsupportedGate(IonQAPIError):
    """Exception raised for using unsupported gates."""

    pass


class CompilationError(IonQAPIError):
    """Exception raised during compilation errors."""

    pass


class SimulationError(IonQAPIError):
    """Exception raised during simulation errors."""

    pass


class Invalid(IonQAPIError):
    """Exception raised for invalid operations."""

    pass


class BillingError(IonQAPIError):
    """Exception raised for billing errors."""

    pass


class TooManyControls(IonQAPIError):
    """Exception raised when too many control gates are used."""

    pass


class DebiasingError(IonQAPIError):
    """Exception raised during debiasing process errors."""

    pass


class Failed(IonQAPIError):
    """Exception raised when a process fails without a specific category."""

    pass


class QuantumComputerError(IonQAPIError):
    """Exception raised for errors specific to quantum computer operations."""

    pass


class Expired(IonQAPIError):
    """Exception raised when a session or token has expired."""

    pass


class ExecutionError(IonQAPIError):
    """Exception raised for execution failures."""

    pass


class NotEnoughQubits(IonQAPIError):
    """Exception raised when there are not enough qubits available."""

    pass
