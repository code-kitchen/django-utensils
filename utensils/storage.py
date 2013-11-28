# encoding: utf-8
from django.conf import settings

from storages.backends.s3boto import S3BotoStorage


"""
Store your static and media files on Amazon S3 easily.

Example settings config:

  AWS = {
      'STATIC': {
          'location': 'static',           # AWS_LOCATION
          'querystring_auth': False,      # AWS_QUERYSTRING_AUTH
          'default_acl': 'public-read',   # AWS_DEFAULT_ACL
      },
      'MEDIA': {
          'location': 'media',            # AWS_LOCATION
          'querystring_auth': True,       # AWS_QUERYSTRING_AUTH
          'default_acl': 'private',       # AWS_DEFAULT_ACL
      },
  }
  
  AWS_ACCESS_KEY_ID = 'XXXXXXXXXXXXXXXXXXXX'
  AWS_SECRET_ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
  AWS_STORAGE_BUCKET_NAME = 'bucket'
  AWS_PRELOAD_METADATA = True
  AWS_S3_SECURE_URLS = False
  
  STATICFILES_STORAGE = 'utensils.storage.StaticRootS3BotoStorage'
  DEFAULT_FILE_STORAGE = 'utensils.storage.MediaRootS3BotoStorage'
"""
StaticRootS3BotoStorage = lambda: S3BotoStorage(**settings.AWS['STATIC'])
MediaRootS3BotoStorage = lambda: S3BotoStorage(**settings.AWS['MEDIA'])
