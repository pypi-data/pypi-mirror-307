import os
from pydantic import BaseModel


class Settings(BaseModel):
    AWS_COGNITO_REGION: str = os.getenv('AWS_COGNITO_REGION')
    AWS_COGNITO_USER_POOL_ID: str = os.getenv('AWS_COGNITO_USER_POOL_ID')
    AWS_COGNITO_APP_CLIENT_ID: str = os.getenv('AWS_COGNITO_APP_CLIENT_ID')
    AWS_COGNITO_APP_CLIENT_SECRET: str = os.getenv(
        'AWS_COGNITO_APP_CLIENT_SECRET')


settings = Settings()
