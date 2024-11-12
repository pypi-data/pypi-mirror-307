import os
from pydantic import BaseModel


class Settings(BaseModel):
    PROJECT_BASE_URL: str = os.getenv('PROJECT_BASE_URL', 'localhost:8090')
    PROJECT_HOST_SCHEME: str = os.getenv('PROJECT_HOST_SCHEME', 'http')
    PROJECT_HOST_SERVICE_DICT: str = os.getenv(
        'PROJECT_HOST_SERVICE_DICT', 'service_dict')
    PROJECT_HOST_SERVICE_PATIENTS: str = os.getenv(
        'PROJECT_HOST_SERVICE_PATIENTS', 'service_patients')
    PROJECT_HOST_SERVICE_PRACTICES: str = os.getenv(
        'PROJECT_HOST_SERVICE_PRACTICES', 'service_practices')
    PROJECT_HOST_SERVICE_CONSULTATIONS: str = os.getenv(
        'PROJECT_HOST_SERVICE_CONSULTATIONS', 'service_consultations')
    PROJECT_HOST_SERVICE_PRODUCTS: str = os.getenv(
        'PROJECT_HOST_SERVICE_PRODUCTS', 'service_products')
    PROJECT_HOST_SERVICE_ML: str = os.getenv(
        'PROJECT_HOST_SERVICE_ML', 'service_ml')
    PROJECT_HOST_SERVICE_CMS: str = os.getenv(
        'PROJECT_HOST_SERVICE_CMS', 'service_cms')


settings = Settings()
