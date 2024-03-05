from .base_settings import *

MEDIA_ROOT = "/tmp/django_join_in_unittest_media"

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "join_in_test",
        "USER": "",
        "PASSWORD": "welkom",
        "HOST": "127.0.0.1",
        "PORT": "5435",
    },
}