from typing import Dict, Any, Callable, Optional
import json
import gzip
import base64


def compress(obj) -> str:
    return base64.b64encode(gzip.compress(json.dumps(obj).encode("utf-8"))).decode(
        "utf-8"
    )


class Circuit:
    def __init__(
        self,
        n_qubits: int,
        shots: int = 100,
        format: str = "ionq.circuit.v0",
        gateset: str = "qis",
        registers: Optional[list] = None,
        name: Optional[str] = None,
        error_mitigation: Optional[Dict[str, bool]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        noise: Optional[Dict[str, str]] = None,
        target: str = "simulator",
    ):
        self.n_qubits = n_qubits
        self.shots = shots
        self.name = name
        self.error_mitigation = error_mitigation
        self.metadata = metadata
        self.noise = noise
        self.target = target
        self.input = {
            "format": format,
            "gateset": gateset,
            "qubits": n_qubits,
            "circuit": [],
        }
        self.circuit = self.input["circuit"]
        self.registers = registers

    def create_job_payload(self, *additional_circuits) -> dict:
        all_circuits = [self] + list(*additional_circuits)

        job_payload = {
            "shots": self.shots,
            "target": self.target,
            "noise": (
                {
                    "model": self.noise["model"] if self.noise else None,
                    "seed": (
                        self.noise["seed"]
                        if self.noise and "seed" in self.noise
                        else None
                    ),
                }
                if self.noise
                else None
            ),
            "error_mitigation": self.error_mitigation,
            "input": {
                "format": self.input["format"],
                "gateset": self.input["gateset"],
            },
        }

        job_payload["name"] = (
            ", ".join([circuit.name for circuit in all_circuits if circuit.name])
            or None
        )
        job_payload["metadata"] = {
            "compressed": compress(
                [circuit.metadata for circuit in all_circuits if circuit.metadata]
            )
        }
        job_payload["input"]["circuits"] = [
            {
                "qubits": circuit.n_qubits,
                "registers": circuit.registers,
                "circuit": circuit.circuit,
            }
            for circuit in all_circuits
        ]

        def remove_none(obj):  # https://stackoverflow.com/a/20558778
            if isinstance(obj, (list, tuple, set)):
                return type(obj)(remove_none(x) for x in obj if x is not None)
            elif isinstance(obj, dict):
                return type(obj)(
                    (remove_none(k), remove_none(v))
                    for k, v in obj.items()
                    if k is not None and v is not None
                )
            else:
                return obj

        job_payload = remove_none(job_payload)

        return job_payload

    def __bool__(self) -> bool:
        return self.n_qubits > 0 and bool(self.circuit)

    def __getattr__(self, name: str) -> Callable[..., Any]:
        def method(*args, **kwargs):
            self.append(name, *args, **kwargs)

        return method

    def append(self, name: str, *args, **kwargs):
        if not name:
            raise ValueError("No gate name provided")

        gate = {"gate": name, "targets": [], "controls": []}

        # Handling positional arguments for target and control qubits
        if args:
            # Single qubit target or first qubit as control in case of multiple args
            (
                gate["targets"].append(args[0])
                if len(args) == 1
                else gate["controls"].append(args[0])
            )
            if len(args) > 1:  # Additional targets if more than one arg
                gate["targets"].extend(args[1:])

        # Handling keyword arguments for gate configuration
        for key, value in kwargs.items():
            if key in ("control", "controls", "target", "targets", "rotation"):
                if isinstance(value, list):
                    gate[key + "s" if key[-1] != "s" else key] = value
                else:
                    gate[
                        (
                            key + "s"
                            if key[-1] != "s" and key not in ("rotation", "controls")
                            else key
                        )
                    ] = ([value] if key in ("target", "control") else value)
            else:
                gate[key] = value

        self.circuit.append(gate)
