import shutil

import pytest
from django.conf import settings


@pytest.fixture(autouse=True)
def delete_media_root():
    try:
        shutil.rmtree(settings.MEDIA_ROOT)
    except FileNotFoundError:
        pass
