import pytest


@pytest.mark.django_db
def test_join_in(lunch_join_in, user_cees, user_john):
    assert lunch_join_in.name == "Lunch Test"
    users = lunch_join_in.users
    assert len(users) == 2
    assert user_cees in users, "User should be part of lunch JoinIn"
    assert user_john in users, "User should be part of lunch JoinIn"
