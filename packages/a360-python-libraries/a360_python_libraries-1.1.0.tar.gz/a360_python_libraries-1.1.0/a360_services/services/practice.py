import uuid
from typing import Union
from urllib.parse import urlencode

from fastapi import status

from ..utils.service_provider import ServiceProvider


class PracticeService:
    def __init__(self, service_provider: ServiceProvider):
        self.service_provider = service_provider

    def get_expert(
            self,
            expert_id: Union[uuid.UUID, None] = None,
            user_id: Union[uuid.UUID, None] = None
    ) -> dict:
        if expert_id is None and user_id is None:
            raise ValueError("Either expert_id or user_id must be provided")
        if expert_id is not None and user_id is not None:
            raise ValueError(
                "Only one of expert_id or user_id should be provided")

        if expert_id is not None:
            request_path = f"/experts/{str(expert_id)}"
        else:
            request_path = f"/experts/by_user_id/{str(user_id)}"

        return self.service_provider.fetch_data(request_path).data

    def is_practice_active(self, practice_id: uuid.UUID) -> bool:
        request_path = f"/practices/{str(practice_id)}/is_active"
        response_code = self.service_provider.fetch_data(request_path).code

        return response_code == status.HTTP_200_OK

    def get_practice(self, practice_id: uuid.UUID) -> dict:
        request_path = f"/practices/{str(practice_id)}"

        return self.service_provider.fetch_data(request_path).data

    def get_practices(
            self,
            search: Union[str, None] = None,
            is_active: Union[bool, None] = None,
            country_iso_code: Union[str, None] = None,
            state_iso_code: Union[str, None] = None,
            city_id: Union[uuid.UUID, None] = None,
            page: Union[int, None] = None,
            page_size: Union[int, None] = None,
    ) -> dict:
        query_params = {}

        if search is not None:
            query_params['search'] = str(search)
        if is_active is not None:
            query_params['is_active'] = is_active
        if country_iso_code is not None:
            query_params['country_iso_code'] = country_iso_code
        if state_iso_code is not None:
            query_params['state_iso_code'] = state_iso_code
        if city_id is not None:
            query_params['city_id'] = str(city_id)
        if page is not None:
            query_params['page'] = page
        if page_size is not None:
            query_params['size'] = page_size

        request_path = f"/practices?{urlencode(query_params, doseq=True)}"

        return self.service_provider.fetch_data(request_path).data
