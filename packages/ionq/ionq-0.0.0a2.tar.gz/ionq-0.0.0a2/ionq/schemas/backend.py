from pydantic import HttpUrl, BaseModel, validator
from typing import Optional
from enum import Enum
from .characterization import Characterization
from ..defaults import DEFAULT_API_URL


class SystemStatus(str, Enum):
    available = "available"
    unavailable = "unavailable"
    running = "running"
    reserved = "reserved"
    calibrating = "calibrating"
    offline = "offline"
    retired = "retired"


class Backend(BaseModel):
    backend: str
    status: SystemStatus
    average_queue_time: int
    last_updated: int
    degraded: Optional[bool] = None
    characterization_url: Optional[HttpUrl] = None
    characterization: Optional[Characterization] = None

    @validator("characterization_url", pre=True)
    def prepend_url_prefix(cls, v: str):
        return DEFAULT_API_URL + v

    class Config:
        schema_extra = {
            "example": {
                "backend": "qpu.aria-1",
                "status": "available",
                "average_queue_time": 1181215,
                "last_updated": 1490932820,
                "degraded": True,
                "characterization_url": "/characterizations/617a1f8b-59d4-435d-aa33-695433d7155e",
                "characterization": {
                    "id": "3c90c3cc-0d44-4b50-8888-8dd25736052a",
                    "date": 123,
                    "target": "qpu.harmony",
                    "qubits": 1,
                    "connectivity": [[0, 1], [0, 2], [10, 9]],
                    "fidelity": {"spam": {"mean": 1, "stderr": 1}},
                    "timing": {"readout": 123, "reset": 123},
                },
            }
        }
