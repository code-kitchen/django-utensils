# encoding: utf-8
from django.conf import settings

from storages.backends.s3boto import S3BotoStorage


StaticRootS3BotoStorage = lambda: S3BotoStorage(**settings.AWS['STATIC'])
MediaRootS3BotoStorage = lambda: S3BotoStorage(**settings.AWS['MEDIA'])
