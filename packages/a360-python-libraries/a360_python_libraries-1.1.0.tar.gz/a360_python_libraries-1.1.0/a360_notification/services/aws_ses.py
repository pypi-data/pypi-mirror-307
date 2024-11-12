import boto3
from typing import Union
from ..utils.email_utils import html_to_text


class AWSSesService:
    def __init__(self, region_name: str, source_email: str):
        self.client = boto3.client('ses', region_name=region_name)
        self.source_email = source_email

    def send_email(
            self,
            recipient_name: str,
            recipient_address: str,
            subject: str,
            html_content: str,
            text_content: Union[str, None] = None
    ):
        if text_content is None:
            text_content = html_to_text(html_content)

        response = self.client.send_email(
            Source=self.source_email,
            Destination={
                'ToAddresses': [f"{recipient_name} <{recipient_address}>"]
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': text_content
                    },
                    'Html': {
                        'Data': html_content
                    }
                }
            }
        )
        return response
