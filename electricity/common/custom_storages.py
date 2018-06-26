from django.conf import settings
from storages.backends.s3boto import S3BotoStorage

if settings.USE_AWS:
    class StaticStorage(S3BotoStorage):
        location = settings.STATICFILES_LOCATION


    class MediaStorage(S3BotoStorage):
        location = settings.MEDIAFILES_LOCATION
