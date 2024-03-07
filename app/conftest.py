import shutil

import freezegun
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from core.models import JoinIn

User = get_user_model()


@pytest.fixture(autouse=True)
def delete_media_root():
    try:
        shutil.rmtree(settings.MEDIA_ROOT)
    except FileNotFoundError:
        pass


@pytest.fixture
def user_cees():
    return User.objects.create_user(username="cees", password=".", email="cees@joinin.com",
                                    first_name="Cees", last_name="Wieringen")


@pytest.fixture
def user_john():
    return User.objects.create_user(username="john", password=".", email="john@joinin.com",
                                    first_name="John", last_name="Doe")


@pytest.fixture
def lunch_join_in(user_cees, user_john):
    with freezegun.freeze_time("2024-02-29"):
        group = Group.objects.create(name="Lunch Test")
        join_in = JoinIn.objects.create(slug="lunch-join-in", group=group, fee=2.0)

    with freezegun.freeze_time("2024-03-10"):
        join_in.join(user_cees)

    with freezegun.freeze_time("2024-03-20"):
        join_in.join(user_john)
    return join_in
