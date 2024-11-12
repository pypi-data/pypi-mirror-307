import os
from pydantic import BaseModel


class Settings(BaseModel):
    PROJECT_BASE_URL: str = os.getenv('PROJECT_BASE_URL', 'localhost:8090')
    PROJECT_HOST_SCHEME: str = os.getenv('PROJECT_HOST_SCHEME', 'http')

    AWS_SES_REGION: str = os.getenv('AWS_SES_REGION')
    AWS_SES_SOURCE_EMAIL: str = os.getenv('AWS_SES_SOURCE_EMAIL')


settings = Settings()
