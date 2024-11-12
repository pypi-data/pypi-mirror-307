from .services.aws_ses import AWSSesService
from .settings import settings


def get_mail_service() -> AWSSesService:
    return AWSSesService(
        region_name=settings.AWS_SES_REGION,
        source_email=settings.AWS_SES_SOURCE_EMAIL,
    )
