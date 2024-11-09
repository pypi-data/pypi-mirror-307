from typing import List, Tuple
from pydantic import BaseModel


class FidelityDetail(BaseModel):
    mean: float


class Fidelity(BaseModel):
    _1q: FidelityDetail
    _2q: FidelityDetail
    spam: FidelityDetail


class Timing(BaseModel):
    readout: float
    reset: float
    t1: float
    t2: float
    _1q: float
    _2q: float


class Characterization(BaseModel):
    id: str
    date: int
    backend: str
    qubits: int
    connectivity: List[Tuple[int, int]]
    fidelity: Fidelity
    timing: Timing

    def __repr__(self):
        # Create a summary of the connectivity showing the first two and the last connection
        if len(self.connectivity) > 2:
            connectivity_summary = f"{self.connectivity[0]}, {self.connectivity[1]}, ..., {self.connectivity[-1]}"
        else:
            connectivity_summary = ", ".join(str(pair) for pair in self.connectivity)

        # Return a formatted string with the summary
        return (
            f"Characterization(id={self.id}, date={self.date}, backend={self.backend}, "
            f"qubits={self.qubits}, connectivity=[{connectivity_summary}], "
            f"fidelity={self.fidelity}, timing={self.timing})"
        )

    class Config:
        schema_extra = {
            "example": {
                "id": "42450d37-33ff-4c92-8d6c-fbe8857e1b5c",
                "date": 1713860166,
                "backend": "qpu.aria-1",
                "qubits": 25,
                "connectivity": [
                    (0, 1),
                    # ...
                    (23, 24),
                ],
                "fidelity": {
                    "1q": {"mean": 0.9997},
                    "2q": {"mean": 0.9706},
                    "spam": {"mean": 0.9948},
                },
                "timing": {
                    "readout": 0.0003,
                    "reset": 0.00002,
                    "t1": 100,
                    "t2": 1,
                    "1q": 0.000135,
                    "2q": 0.0006,
                },
            }
        }
