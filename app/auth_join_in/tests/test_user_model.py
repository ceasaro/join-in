import os

import pytest
from django.conf import settings

from auth_join_in.models import User


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(username="testuser", password="<PASSWORD>", email="ceesvw@test.nl")
    assert user.card_img, "A card image should present"
    assert "ceesvw" in user.card_img.name, "Card name should contains username of email"
    assert os.path.isfile(os.path.join(settings.MEDIA_ROOT, "user_card_images", "ceesvw.png"))
