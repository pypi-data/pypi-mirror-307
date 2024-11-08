from typing import Any, Dict, Optional
import os
import time

import requests
from requests.exceptions import ConnectionError, Timeout

from ..errors import IonQAPIError
from ..defaults import DEFAULT_API_URL, SDK_VERSION
from . import resources
from .. import errors


def handle_error(response_json: dict):
    if "failure" in response_json:
        error_code = response_json["failure"]["code"]
        error = response_json["failure"].get("error") or response_json["failure"].get(
            "message"
        )
        if error_code in code_to_class:
            # Raise the appropriate error class
            raise code_to_class[error_code](error=error)
        else:
            raise errors.IonQAPIError(error=error)


code_to_class = {
    "PreflightError": errors.PreflightError,
    "InternalError": errors.InternalError,
    "TooManyGates": errors.TooManyGates,
    "SystemCancel": errors.SystemCancel,
    "QuotaExhaustedError": errors.QuotaExhaustedError,
    "TimedOut": errors.TimedOut,
    "TooLongPredictedExecutionTime": errors.TooLongPredictedExecutionTime,
    "CircuitTooLarge": errors.CircuitTooLarge,
    "TooManyShots": errors.TooManyShots,
    "ContractExpiredError": errors.ContractExpiredError,
    "SimulationTimeout": errors.SimulationTimeout,
    "OptimizationError": errors.OptimizationError,
    "UnsupportedGate": errors.UnsupportedGate,
    "CompilationError": errors.CompilationError,
    "SimulationError": errors.SimulationError,
    "Invalid": errors.Invalid,
    "BillingError": errors.BillingError,
    "TooManyControls": errors.TooManyControls,
    "DebiasingError": errors.DebiasingError,
    "Failed": errors.Failed,
    "QuantumComputerError": errors.QuantumComputerError,
    "Expired": errors.Expired,
    "ExecutionError": errors.ExecutionError,
    "NotEnoughQubits": errors.NotEnoughQubits,
}


class Client:

    jobs: resources.Job
    backends: resources.Backend

    api_key: str
    base_url: str

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:

        if api_key is None:
            api_key = os.environ.get("IONQ_API_KEY")
        if api_key is None:
            raise IonQAPIError(
                "The api_key client option must be set either by passing api_key to the client or by setting the IONQ_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("IONQ_BASE_URL") or DEFAULT_API_URL
        self.base_url = base_url

        self.jobs = resources.Job(self)
        self.backends = resources.Backend(client=self)

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"apiKey {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": f"ionq/{SDK_VERSION}",
        }

    def request(
        self,
        url: str,
        method: str,
        max_retries: int = 3,
        timeout_seconds: int = 10,
        sleep_seconds: int = 2,
        **kwargs,
    ) -> Dict[str, Any]:
        retries = 0
        while retries < max_retries:
            try:
                response = requests.request(
                    method,
                    f"{self.base_url}{url}",
                    timeout=timeout_seconds,
                    headers=self.headers,
                    **kwargs,
                )
                response.raise_for_status()  # Raises HTTPError for bad HTTP responses
                response_json: Dict[str, Any] = response.json()  # Raises ValueError
                handle_error(response_json)  # Raises API-specific errors
                return response_json
            except (ConnectionError, Timeout):
                if retries == max_retries - 1:
                    raise  # Re-raise the last exception if out of retries
                retries += 1
                time.sleep(sleep_seconds * (2 ** (retries - 1)))  # Exponential backoff
            except ValueError:
                # Handling JSON parsing failure
                print(f"Failed to parse JSON response: {response.text}")
                raise
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                raise  # For non-retriable exceptions, we raise them immediately
        raise Timeout(f"Request timed out after {max_retries} retries")
