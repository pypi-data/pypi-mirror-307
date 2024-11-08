import random
import string
import time
import typing

from planqk.service.auth import DEFAULT_TOKEN_ENDPOINT, PlanqkServiceAuth
from planqk.service.sdk import Job, JobStatus, GetResultResponse, GetInterimResultsResponse, InputData, InputParams, InputRef, HealthCheckResponse
from planqk.service.sdk.client import PlanqkServiceApi
from planqk.service.sdk.errors.not_found_error import NotFoundError

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class PlanqkServiceExecution:
    def __init__(self, client: 'PlanqkServiceClient', job: Job):
        self._client = client
        self._job = job

    @property
    def id(self) -> str:
        return self._job.id

    @property
    def status(self) -> JobStatus:
        return self._client.get_status(self._job.id).status

    def result(self) -> GetResultResponse:
        return self._client.get_result(self._job.id)

    def interim_results(self) -> GetInterimResultsResponse:
        return self._client.get_interim_results(self._job.id)

    def cancel(self) -> None:
        self._client.cancel_execution(self._job.id)


class PlanqkServiceClient:
    def __init__(
            self,
            service_endpoint: str,
            consumer_key: typing.Union[str, None],
            consumer_secret: typing.Union[str, None],
            token_endpoint: str = DEFAULT_TOKEN_ENDPOINT
    ):
        self._service_endpoint = service_endpoint
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._token_endpoint = token_endpoint

        if (self._consumer_key is not None) or (self._consumer_secret is not None):
            self._auth = PlanqkServiceAuth(consumer_key=self._consumer_key,
                                           consumer_secret=self._consumer_secret,
                                           token_endpoint=self._token_endpoint)
            self._api = PlanqkServiceApi(token=self._auth.get_token, base_url=self._service_endpoint)
        else:
            random_token = "".join(random.choices(string.ascii_letters + string.digits, k=21))
            self._api = PlanqkServiceApi(token=random_token, base_url=self._service_endpoint)

    def health_check(self) -> HealthCheckResponse:
        return self._api.status_api.health_check()

    def start_execution(
            self,
            data: typing.Optional[InputData] = OMIT,
            data_ref: typing.Optional[InputRef] = OMIT,
            params: typing.Optional[InputParams] = OMIT,
    ) -> PlanqkServiceExecution:
        job = self._api.service_api.start_execution(data=data, data_ref=data_ref, params=params)
        return PlanqkServiceExecution(self, job)

    def get_status(self, job_id: str) -> Job:
        return self._api.service_api.get_status(job_id)

    def get_result(self, job_id: str) -> GetResultResponse:
        self.wait_for_final_state(job_id)
        delay = 1  # Start with a small delay
        max_delay = 16  # Maximum delay
        while True:
            try:
                result = self._api.service_api.get_result(job_id)
                break  # If the operation succeeds, break out of the loop
            except NotFoundError as e:
                time.sleep(delay)  # If the operation fails, wait
                delay *= 2  # Double the delay
                if delay >= max_delay:
                    raise e  # If the delay is too long, raise the exception
        return result

    def get_interim_results(self, job_id: str) -> GetInterimResultsResponse:
        return self._api.service_api.get_interim_results(job_id)

    def cancel_execution(self, job_id: str) -> Job:
        return self._api.service_api.cancel_execution(job_id)

    def wait_for_final_state(self, job_id: str, timeout: typing.Optional[float] = None, wait: float = 5) -> None:
        """
        Poll the job status until it progresses to a final state.

        Parameters:
            - job_id: str. The id of a service execution.
            - timeout: Seconds to wait for the job. If ``None``, wait indefinitely.
            - wait: Seconds between queries.

        Raises:
            Exception: If the job does not reach a final state before the specified timeout.
        """
        start_time = time.time()
        job = self.get_status(job_id)
        while self.__job_has_finished(job) is False:
            elapsed_time = time.time() - start_time
            if timeout is not None and elapsed_time >= timeout:
                raise Exception(f"Timeout while waiting for job '{job_id}'.")
            time.sleep(wait)
            job = self.get_status(job_id)
        return

    @staticmethod
    def __job_has_finished(job: Job) -> bool:
        return (job.status == JobStatus.SUCCEEDED
                or job.status == JobStatus.FAILED
                or job.status == JobStatus.CANCELLED)
