from __future__ import annotations

import time
from typing import Optional, List, Dict, Any
import json
import gzip
import base64

from ..resource import Resource
from ...schemas import JobDetails, JobStatus, JobUpdate, JobRequest, JobProgress
from ...errors import UserCancelledError


def decompress(data: str):
    return json.loads(gzip.decompress(base64.b64decode(data)).decode("utf-8"))


def is_compressed(data: str) -> bool:
    try:
        decompress(data)
        return True
    except Exception:
        return False


class Job(Resource):

    def wait_for_results(self, id: str, polling_rate: float = 1.0) -> Dict[str, Any]:

        while True:
            job = self.get_job(id)  # Get the job and store it in a variable
            if job.status in (
                JobStatus.completed,
                JobStatus.failed,
                JobStatus.canceled,
            ):
                return self.get_job_results(job.id)
            time.sleep(polling_rate)

    def get_jobs(
        self,
        id: Optional[List[str]] = None,
        status: Optional[str] = None,
        limit: int = 25,
        next: Optional[str] = None,
    ) -> List[JobDetails]:
        query_params = {
            key: value
            for key, value in {
                "id": id,
                "status": status,
                "limit": limit,
                "next": next,
            }.items()
            if value is not None
        }
        response = self.client.request(
            "/jobs",
            method="GET",
            params=query_params,
        )

        return [JobDetails(**job) for job in response.get("jobs", [])] or []

    def get_job(
        self,
        job_id: str,
        exclude: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
    ) -> JobDetails:
        params = {
            "exclude": ",".join(exclude) if exclude else None,
            "include": ",".join(include) if include else None,
        }
        response = self.client.request(
            f"/jobs/{job_id}",
            method="GET",
            params=params,
        )

        job = JobDetails(**response)
        if isinstance(job.metadata, dict):
            for key, value in job.metadata.items():
                if is_compressed(str(value)):
                    job.metadata[key] = decompress(str(value))
        return job

    def get_job_results(self, id: str, sharpen: bool = False) -> Dict[str, Any]:
        params = {"sharpen": sharpen} if sharpen else {}

        response = self.client.request(
            f"/jobs/{id}/results",
            method="GET",
            params=params,
        )

        return response

    def get_job_progress(self, job_id: str) -> JobProgress:
        response = self.client.request(
            f"/jobs/{job_id}/progress",
            method="GET",
        )

        return JobProgress(**response)

    def create_job(self, job_request: JobRequest) -> JobUpdate:
        job_payload = job_request.dict(exclude_none=True)

        response = self.client.request(
            "/jobs",
            method="POST",
            json=job_payload,
        )
        job_data = JobUpdate(**response)

        return job_data

    def delete_many_jobs(self, job_ids: List[str], force: bool = False) -> JobUpdate:
        if not force:
            if (
                not input(
                    f"Are you sure you want to delete {len(job_ids)} jobs? (y/n): "
                )
                .lower()
                .startswith("y")
            ):
                raise UserCancelledError(
                    "The user canceled the bulk deletion operation."
                )
        response = self.client.request(
            "/jobs",
            method="DELETE",
            json={"ids": job_ids},
        )

        return JobUpdate(**response)

    def delete_job(self, job_id: str, force: bool = False) -> JobUpdate:
        if not force:
            if (
                not input("Are you sure you want to delete this job? (y/n): ")
                .lower()
                .startswith("y")
            ):
                raise UserCancelledError("The user canceled the deletion operation.")
        response = self.client.request(
            f"/jobs/{job_id}",
            method="DELETE",
        )

        return JobUpdate(**response)

    def cancel_job(self, job_id: str) -> JobUpdate:
        response = self.client.request(
            f"/jobs/{job_id}/status/cancel",
            method="PUT",
        )

        return JobUpdate(**response)

    def cancel_many_jobs(self, job_ids: List[str]) -> JobUpdate:
        response = self.client.request(
            "/jobs/status/cancel",
            method="PUT",
            json={"ids": job_ids},
        )

        return JobUpdate(**response)
