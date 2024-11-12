from typing import Union

import httpx
from fastapi import Request

from ..dto import ServiceResponse
from ..settings import settings
from .services_list import ServiceName


class ServiceProvider:
    def __init__(
            self,
            client: httpx.Client,
            service_name: ServiceName,
            service_host: str,
            token: str = None
    ):
        self.client = client
        self.token = token
        self.service_name = service_name
        self.service_host = service_host

    def fetch_data(self, request_path: str) -> ServiceResponse:
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        response_obj = self.client.get(
            f"{settings.PROJECT_HOST_SCHEME}://{self.service_host}/services/{self.service_name.value}{request_path}",
            headers=headers)

        try:
            response_data = response_obj.json()
        except ValueError:
            response_data = {}

        return ServiceResponse(
            code=response_obj.status_code,
            data=response_data
        )


def get_dictionary_service_provider(request: Request) -> ServiceProvider:
    client = httpx.Client()
    return ServiceProvider(
        client=client,
        token=get_token(request),
        service_name=ServiceName.dict,
        service_host=get_service_host(ServiceName.dict)
    )


def get_practice_service_provider(request: Request) -> ServiceProvider:
    client = httpx.Client()
    return ServiceProvider(
        client=client,
        token=get_token(request),
        service_name=ServiceName.practice,
        service_host=get_service_host(ServiceName.practice)
    )


def get_patient_service_provider(request: Request) -> ServiceProvider:
    client = httpx.Client()
    return ServiceProvider(
        client=client,
        token=get_token(request),
        service_name=ServiceName.patient,
        service_host=get_service_host(ServiceName.patient)
    )


def get_token(request: Request) -> Union[str, None]:
    authorization = request.headers.get("Authorization")
    if authorization and authorization.lower().startswith("bearer"):
        return authorization.split(" ")[1]
    return None


def get_service_host(service_name: ServiceName) -> str:
    service_hosts = {
        ServiceName.dict: settings.PROJECT_HOST_SERVICE_DICT,
        ServiceName.patient: settings.PROJECT_HOST_SERVICE_PATIENTS,
        ServiceName.practice: settings.PROJECT_HOST_SERVICE_PRACTICES,
        ServiceName.ml: settings.PROJECT_HOST_SERVICE_ML,
    }

    try:
        return service_hosts[service_name]
    except KeyError:
        raise ValueError(f"Unknown service name: {service_name}")
