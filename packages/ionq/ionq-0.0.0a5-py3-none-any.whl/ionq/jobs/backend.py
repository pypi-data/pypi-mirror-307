from typing import Optional, List, Dict, Any, Type

from ionq.schemas.job import (
    JobRequest,
    TargetOptions,
    JobProgress,
    NoiseOptions,
    NoiseModel,
)
from ionq import Client

from .jobs import JobType, Workload, OptimizationJob, CircuitJob, QuantumFunctionJob


class Backend:
    def __init__(
        self, name: str, client: Optional[Client] = None, gateset: str = "qis"
    ):
        self.name = name
        self.client = client if client is not None else Client()
        self.gateset = gateset

    def run(
        self,
        workload: Workload[JobType],
        name: Optional[str] = None,
        shots: Optional[int] = None,
        params: Optional[List[float]] = None,
        noise: Optional[str] = None,
    ) -> JobType:

        workload_input = workload.to_workload_input(params)
        request = JobRequest(
            name=name,
            backend=TargetOptions(self.name),
            workload=workload_input,
            shots=shots,
            noise=NoiseOptions(model=NoiseModel(noise)) if noise else None,
        )

        job = self.client.jobs.create_job(request)

        return workload.create_job(job.id, request, self)

    def get_job_progress(self, job_id: str) -> JobProgress:
        return self.client.jobs.get_job_progress(job_id)

    def get_optimization_job(self, job_id: str) -> OptimizationJob:
        return self.get_job(job_id, OptimizationJob)

    def get_circuit_job(self, job_id: str) -> CircuitJob:
        return self.get_job(job_id, CircuitJob)

    def get_quantum_function_job(self, job_id: str) -> QuantumFunctionJob:
        return self.get_job(job_id, QuantumFunctionJob)

    def get_job(self, job_id: str, job_type: Type[JobType]) -> JobType:
        job = self.client.jobs.get_job(job_id)
        return job_type(job_id, job, self)

    def results(
        self,
        job_id: str,
    ) -> Dict[str, Any]:
        return self.client.jobs.wait_for_results(job_id)
