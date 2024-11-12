import uuid
from typing import Union
from urllib.parse import urlencode

from ..utils.service_provider import ServiceProvider


class DictionaryService:
    def __init__(self, service_provider: ServiceProvider):
        self.service_provider = service_provider

    def get_allergies(
            self,
            icd10_codes: Union[list[str], None] = None,
            page: Union[int, None] = None,
            page_size: Union[int, None] = None,
    ) -> dict:
        query_params = {}
        if icd10_codes is not None:
            query_params = {'icd10_code': icd10_codes}
        if page is not None:
            query_params['page'] = page
        if page_size is not None:
            query_params['size'] = page_size

        request_path = f"/allergies?{urlencode(query_params, doseq=True)}"
        response = self.service_provider.fetch_data(request_path)

        return response.data.get('items')

    def get_medical_conditions(
            self,
            icd10_codes: Union[list[str], None] = None,
            page: Union[int, None] = None,
            page_size: Union[int, None] = None,
    ) -> dict:
        query_params = {}
        if icd10_codes is not None:
            query_params = {'icd10_code': icd10_codes}
        if page is not None:
            query_params['page'] = page
        if page_size is not None:
            query_params['size'] = page_size

        request_path = f"/medical_conditions?{urlencode(query_params, doseq=True)}"
        response = self.service_provider.fetch_data(request_path)

        return response.data.get('items')

    def get_countries(
            self,
            iso_codes: Union[list[str], None] = None,
            page: Union[int, None] = None,
            page_size: Union[int, None] = None,
    ) -> dict:
        query_params = {}
        if iso_codes is not None:
            query_params = {'iso_codes': iso_codes}
        if page is not None:
            query_params['page'] = page
        if page_size is not None:
            query_params['size'] = page_size

        request_path = f"/countries?{urlencode(query_params, doseq=True)}"
        response = self.service_provider.fetch_data(request_path)

        return response.data.get('items')

    def get_states(
            self,
            country_iso_code: Union[None, str] = None,
            iso_codes: Union[list[str], None] = None,
            page: Union[int, None] = None,
            page_size: Union[int, None] = None,
    ) -> dict:
        query_params = {}
        if iso_codes is not None:
            query_params = {'iso_codes': iso_codes}
        if page is not None:
            query_params['page'] = page
        if page_size is not None:
            query_params['size'] = page_size

        request_path = f"/states?{urlencode(query_params, doseq=True)}"
        if country_iso_code:
            request_path = f"/countries/{country_iso_code}/states?{urlencode(query_params, doseq=True)}"
        response = self.service_provider.fetch_data(request_path)

        return response.data.get('items')

    def get_cities(
            self,
            city_ids: Union[list[str], None] = None,
            page: Union[int, None] = None,
            page_size: Union[int, None] = None,
    ) -> dict:
        query_params = {}
        if city_ids is not None:
            query_params = {'id': city_ids}
        if page is not None:
            query_params['page'] = page
        if page_size is not None:
            query_params['size'] = page_size

        request_path = f"/cities?{urlencode(query_params, doseq=True)}"
        response = self.service_provider.fetch_data(request_path)

        return response.data.get('items')

    def get_tag_categories(
            self,
            search: Union[str, None] = None,
            is_core: Union[bool, None] = None,
            is_active: Union[bool, None] = None,
            page: Union[int, None] = None,
            page_size: Union[int, None] = None
    ) -> dict:
        query_params = {}

        if search is not None:
            query_params['search'] = search
        if is_core is not None:
            query_params['is_core'] = is_core
        if is_active is not None:
            query_params['is_active'] = is_active
        if page is not None:
            query_params['page'] = page
        if page_size is not None:
            query_params['size'] = page_size

        request_path = f"/tag_categories?{urlencode(query_params, doseq=True)}"

        response = self.service_provider.fetch_data(request_path)
        return response.data

    def get_tag_category(self, tag_category_id: str) -> dict:
        request_path = f"/tag_categories/{tag_category_id}"
        response = self.service_provider.fetch_data(request_path)
        return response.data

    def get_tags(
            self,
            search: str = None,
            is_active: bool = None,
            page: int = None,
            page_size: int = None
    ) -> dict:
        query_params = {}

        if search is not None:
            query_params['search'] = search
        if is_active is not None:
            query_params['is_active'] = is_active
        if page is not None:
            query_params['page'] = page
        if page_size is not None:
            query_params['size'] = page_size

        request_path = f"/tags?{urlencode(query_params, doseq=True)}"

        response = self.service_provider.fetch_data(request_path)
        return response.data

    def get_tag(self, tag_id: str) -> dict:
        request_path = f"/tags/{tag_id}"
        response = self.service_provider.fetch_data(request_path)
        return response.data

    def get_services(
            self,
            search: Union[str, None] = None,
            page: Union[int, None] = None,
            page_size: Union[int, None] = None
    ) -> dict:
        query_params = {}

        if search is not None:
            query_params['search'] = search
        if page is not None:
            query_params['page'] = page
        if page_size is not None:
            query_params['size'] = page_size

        request_path = f"/services?{urlencode(query_params, doseq=True)}"

        response = self.service_provider.fetch_data(request_path)
        return response.data

    def get_service(self, service_id: str) -> dict:
        request_path = f"/services/{service_id}"
        response = self.service_provider.fetch_data(request_path)
        return response.data

    def get_products(
            self,
            search: Union[str, None] = None,
            page: Union[int, None] = None,
            page_size: Union[int, None] = None
    ) -> dict:
        query_params = {}

        if search is not None:
            query_params['search'] = search
        if page is not None:
            query_params['page'] = page
        if page_size is not None:
            query_params['size'] = page_size

        request_path = f"/products?{urlencode(query_params, doseq=True)}"

        response = self.service_provider.fetch_data(request_path)
        return response.data

    def get_product(self, product_id: str) -> dict:
        request_path = f"/products/{product_id}"
        response = self.service_provider.fetch_data(request_path)
        return response.data

    def get_visit_workflows(
            self,
            search: Union[str, None] = None,
            page: Union[int, None] = None,
            page_size: Union[int, None] = None
    ) -> dict:
        query_params = {}

        if search is not None:
            query_params['search'] = search
        if page is not None:
            query_params['page'] = page
        if page_size is not None:
            query_params['size'] = page_size

        request_path = f"/visit_workflows?{urlencode(query_params, doseq=True)}"

        response = self.service_provider.fetch_data(request_path)
        return response.data

    def get_visit_workflow(self, id: str) -> dict:
        request_path = f"/visit_workflows/{id}"
        response = self.service_provider.fetch_data(request_path)
        return response.data

    def get_b_a_albums(
            self,
            search: Union[str, None] = None,
            page: Union[int, None] = None,
            page_size: Union[int, None] = None,
    ) -> dict:
        query_params = {}

        if search is not None:
            query_params['search'] = search
        if page is not None:
            query_params['page'] = page
        if page_size is not None:
            query_params['size'] = page_size

        request_path = f"/b_a_albums?{urlencode(query_params, doseq=True)}"

        response = self.service_provider.fetch_data(request_path)
        return response.data

    def get_b_a_album(self, album_id: str) -> dict:
        request_path = f"/b_a_albums/{album_id}"
        response = self.service_provider.fetch_data(request_path)
        return response.data

    def get_b_a_pairs(
            self,
            album_id: Union[uuid.UUID, None] = None,
            search: Union[str, None] = None,
            page: Union[int, None] = None,
            page_size: Union[int, None] = None
    ) -> dict:
        query_params = {}

        if album_id is not None:
            query_params['album_id'] = str(album_id)
        if search is not None:
            query_params['search'] = search
        if page is not None:
            query_params['page'] = page
        if page_size is not None:
            query_params['size'] = page_size

        request_path = f"/b_a_pairs?{urlencode(query_params, doseq=True)}"

        response = self.service_provider.fetch_data(request_path)
        return response.data

    def get_b_a_pair(self, pair_id: str) -> dict:
        request_path = f"/b_a_pairs/{pair_id}"
        response = self.service_provider.fetch_data(request_path)
        return response.data
