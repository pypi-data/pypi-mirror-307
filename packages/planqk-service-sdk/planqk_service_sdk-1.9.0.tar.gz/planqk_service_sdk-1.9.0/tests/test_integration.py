import os
import unittest

from planqk.service.auth import PlanqkServiceAuth
from planqk.service.client import PlanqkServiceClient
from planqk.service.sdk import JobStatus, InputRef
from planqk.service.sdk.client import PlanqkServiceApi

service_endpoint = os.getenv('SERVICE_ENDPOINT', "http://localhost:8081")
consumer_key = os.getenv('CONSUMER_KEY', None)
consumer_secret = os.getenv('CONSUMER_SECRET', None)


class IntegrationTestSuite(unittest.TestCase):

    def test_should_use_client(self):
        client = PlanqkServiceClient(service_endpoint, consumer_key, consumer_secret)

        health = client.health_check()
        assert health.status == "Service is up and running"

        data = {
            "values": [
                1,
                5.2,
                20,
                7,
                9.4
            ]
        }
        params = {
            "round_off": True
        }

        job = client.start_execution(data=data, params=params)
        assert job.id is not None
        assert job.status is not None

        result = client.get_result(job.id)
        assert result is not None

        job = client.get_status(job.id)
        assert job.id is not None
        assert job.status == JobStatus.SUCCEEDED

        print(job, result)

    def test_should_use_raw_client(self):
        if (consumer_key is not None) or (consumer_secret is not None):
            auth = PlanqkServiceAuth(consumer_key, consumer_secret)
            api = PlanqkServiceApi(token=auth.get_token, base_url=service_endpoint)
        else:
            api = PlanqkServiceApi(token="random_token", base_url=service_endpoint)

        health = api.status_api.health_check()
        assert health.status == "Service is up and running"

        data = {
            "values": [
                1,
                5.2,
                20,
                7,
                9.4
            ]
        }
        params = {
            "round_off": True
        }

        job = api.service_api.start_execution(data=data, params=params)
        assert job.id is not None
        assert job.status == JobStatus.PENDING

        job = api.service_api.get_status(job.id)
        while job.status != JobStatus.SUCCEEDED and job.status != JobStatus.FAILED:
            job = api.service_api.get_status(job.id)

        assert job.status == JobStatus.SUCCEEDED or job.status == JobStatus.FAILED

        result = api.service_api.get_result(job.id)
        assert result is not None

        print(job, result)

    def test_should_use_client_with_datapool_ref(self):
        client = PlanqkServiceClient(service_endpoint, consumer_key, consumer_secret)

        health = client.health_check()
        assert health.status == "Service is up and running"

        data = InputRef(data_pool_id="e3859bb2-1959-4d3d-852b-62ee81b28a72",
                        data_source_descriptor_id="1c8d341e-1c86-4e19-acae-2f84bcab55ca",
                        file_id="f5251675-49c6-49f3-a3a6-de75b8335d76")
        params = {
            "round_off": True
        }

        job = client.start_execution(data_ref=data, params=params)
        assert job.id is not None
        assert job.status is not None

        result = client.get_result(job.id)
        assert result is not None

        job = client.get_status(job.id)
        assert job.id is not None
        assert job.status == JobStatus.SUCCEEDED

        print(job, result)

    def test_should_use_job_to_retrieve_dynamic_data(self):
        client = PlanqkServiceClient(service_endpoint, consumer_key, consumer_secret)

        data = {
            "values": [
                1,
                5.2,
                20,
                7,
                9.4
            ]
        }
        params = {
            "round_off": True
        }

        job = client.start_execution(data=data, params=params)

        assert job.id is not None
        assert job.status is not None

        assert job.result() is not None
        assert job.interim_results() is not None

        assert job.cancel() is None
