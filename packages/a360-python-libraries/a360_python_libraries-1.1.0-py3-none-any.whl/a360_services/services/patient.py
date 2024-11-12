import uuid
from datetime import datetime
from typing import Union
from urllib.parse import urlencode

from ..utils.service_provider import ServiceProvider


class PatientService:
    def __init__(self, service_provider: ServiceProvider):
        self.service_provider = service_provider

    def get_patients(
            self,
            practice_id: Union[uuid.UUID, None] = None,
            search: Union[str, None] = None,
            gender: Union[str, None] = None,
            bio_gender: Union[str, None] = None,
            ethnic_group: Union[str, None] = None,
            age_from: Union[int, None] = None,
            age_to: Union[int, None] = None,
            home_address_country_iso_code: Union[str, None] = None,
            home_address_state_iso_code: Union[str, None] = None,
            home_address_city_id: Union[uuid.UUID, None] = None,
            page: Union[int, None] = None,
            page_size: Union[int, None] = None,
    ) -> dict:
        query_params = {}

        if practice_id is not None:
            query_params['practice_id'] = str(practice_id)
        if search is not None:
            query_params['search'] = search
        if gender is not None:
            query_params['gender'] = gender
        if bio_gender is not None:
            query_params['bio_gender'] = bio_gender
        if ethnic_group is not None:
            query_params['ethnic_group'] = ethnic_group
        if age_from is not None:
            query_params['age_from'] = age_from
        if age_to is not None:
            query_params['age_to'] = age_to
        if home_address_country_iso_code is not None:
            query_params['home_address_country_iso_code'] = home_address_country_iso_code
        if home_address_state_iso_code is not None:
            query_params['home_address_state_iso_code'] = home_address_state_iso_code
        if home_address_city_id is not None:
            query_params['home_address_city_id'] = str(home_address_city_id)
        if page is not None:
            query_params['page'] = page
        if page_size is not None:
            query_params['size'] = page_size

        request_path = f"/patients?{urlencode(query_params, doseq=True)}"

        return self.service_provider.fetch_data(request_path).data

    def get_patient(self, patient_id: uuid.UUID) -> dict:
        request_path = f"/patients/{patient_id}"

        return self.service_provider.fetch_data(request_path).data

    def get_visits(
            self,
            practice_id: Union[uuid.UUID, None] = None,
            office_id: Union[uuid.UUID, None] = None,
            expert_id: Union[uuid.UUID, None] = None,
            patient_id: Union[uuid.UUID, None] = None,
            interaction_type: Union[str, None] = None,
            appointment_status: Union[str, None] = None,
            appointment_type: Union[str, None] = None,
            appointment_at_from: Union[datetime, None] = None,
            appointment_at_to: Union[datetime, None] = None,
            page: Union[int, None] = None,
            page_size: Union[int, None] = None,
    ) -> dict:
        query_params = {}

        if practice_id is not None:
            query_params['practice_id'] = str(practice_id)
        if office_id is not None:
            query_params['office_id'] = str(office_id)
        if expert_id is not None:
            query_params['expert_id'] = str(expert_id)
        if patient_id is not None:
            query_params['patient_id'] = str(patient_id)
        if interaction_type is not None:
            query_params['interaction_type'] = interaction_type
        if appointment_status is not None:
            query_params['appointment_status'] = appointment_status
        if appointment_type is not None:
            query_params['appointment_type'] = appointment_type
        if appointment_at_from is not None:
            query_params['appointment_at_from'] = appointment_at_from.isoformat()
        if appointment_at_to is not None:
            query_params['appointment_at_to'] = appointment_at_to.isoformat()
        if page is not None:
            query_params['page'] = page
        if page_size is not None:
            query_params['size'] = page_size

        request_path = f"/visits?{urlencode(query_params, doseq=True)}"

        return self.service_provider.fetch_data(request_path).data

    def get_visit(self, visit_id: uuid.UUID) -> dict:
        request_path = f"/visits/{visit_id}"

        return self.service_provider.fetch_data(request_path).data

    def get_patient_attachments(
            self,
            patient_id: uuid.UUID,
            attachment_type: Union[str, None] = None,
            page: Union[int, None] = None,
            page_size: Union[int, None] = None,
    ) -> dict:
        query_params = {}

        if attachment_type is not None:
            query_params['attachment_type'] = attachment_type
        if page is not None:
            query_params['page'] = page
        if page_size is not None:
            query_params['size'] = page_size

        request_path = f"/patients/{str(patient_id)}/attachments?{urlencode(query_params, doseq=True)}"

        return self.service_provider.fetch_data(request_path).data

    def get_visit_attachments(
            self,
            visit_id: uuid.UUID,
            attachment_type: Union[str, None] = None,
            page: Union[int, None] = None,
            page_size: Union[int, None] = None,
    ) -> dict:
        query_params = {}

        if attachment_type is not None:
            query_params['attachment_type'] = attachment_type
        if page is not None:
            query_params['page'] = page
        if page_size is not None:
            query_params['size'] = page_size

        request_path = f"/visits/{str(visit_id)}/attachments?{urlencode(query_params, doseq=True)}"

        return self.service_provider.fetch_data(request_path).data

    def get_audio_attachment(self, attachment_id: uuid.UUID) -> dict:
        request_path = f"/attachments/audio/{attachment_id}"

        return self.service_provider.fetch_data(request_path).data
