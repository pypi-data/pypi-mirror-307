from typing import List, Optional
from pydantic import BaseModel


class CircuitOperation(BaseModel):
    gate: str
    target: Optional[int] = None
    targets: Optional[List[int]] = None
    control: Optional[int] = None
    controls: Optional[List[int]] = None
    rotation: Optional[float] = None


class CircuitList(BaseModel):
    qubits: Optional[int] = None
    registers: Optional[Optional[List[int]]] = None
    circuit: List[CircuitOperation]
