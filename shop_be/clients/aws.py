import uuid

import aioboto3
from fastapi import UploadFile
from pydantic import AnyHttpUrl

from shop_be.conf.settings import settings
from shop_be.schemas.customer.customer import CognitoCustomerSchema


class AWSClient:
    class ROUTES:
        IMAGE: str = '{env}/attachments/{uuid}.{type}'

    def __init__(self):
        self.session = aioboto3.Session()
        self.bucket_name = settings.S3_BUCKET_NAME

    async def cognito_get_user(self, username: str) -> CognitoCustomerSchema:
        """Get user from cognito by access token"""
        async with self.session.client('cognito-idp') as cognito:
            user_data = await cognito.admin_get_user(UserPoolId=settings.COGNITO_POOL_ID, Username=username)
            attributes = {attr['Name']: attr['Value'] for attr in user_data['UserAttributes']}
            return CognitoCustomerSchema(**attributes)

    async def save_image(self, file: UploadFile) -> AnyHttpUrl:
        """Upload avatar to S3bucket"""
        async with self.session.client('s3') as s3:
            s3_route = self.ROUTES.IMAGE.format(
                env=settings.ENV,
                uuid=str(uuid.uuid4()),
                type=file.filename.split('.')[-1],
            )
            await s3.upload_fileobj(file, self.bucket_name, s3_route, ExtraArgs={'ACL': 'public-read'})
            return self._generate_s3_path(s3_route)

    def _generate_s3_path(self, path: str) -> AnyHttpUrl:
        url = 'https://{bucket_name}.s3.{region}.amazonaws.com/{path}'.format(
            bucket_name=self.bucket_name,
            region=settings.AWS_DEFAULT_REGION,
            path=path,
        )
        return AnyHttpUrl(url=url)

    async def delete_s3_obj(self, url: AnyHttpUrl) -> None:
        """Delete file from S3 bucket"""
        file_key = '/'.join(url.split('/')[-3:])
        async with self.session.resource('s3') as s3:
            bucket = await s3.Bucket(self.bucket_name)
            await bucket.objects.filter(Key=file_key).delete()
