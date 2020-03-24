from storages.backends.s3boto3 import S3Boto3Storage
from storages.utils import setting


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
    default_acl = setting("AWS_DEFAULT_ACL_MEDIA", None)
