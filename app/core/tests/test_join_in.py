import pytest


@pytest.mark.django_db
def test_join_in(lunch_join_in, user_cees, user_john):
    assert lunch_join_in.name == "Lunch Test"
    users = lunch_join_in.users
    assert len(users) == 2
    assert user_cees in users, "User should be part of lunch JoinIn"
    assert user_john in users, "User should be part of lunch JoinIn"


@pytest.mark.django_db
def test_debit(lunch_join_in, user_cees):
    assert lunch_join_in.debit(user_cees) == 0.0, "User hasn't joined yet and should have no debit"
    lunch_join_in.pay_fee(user_cees)
    assert lunch_join_in.debit(user_cees) == 2.0, "User must have a debit"
    lunch_join_in.pay_fee(user_cees)
    lunch_join_in.fee = 2.5
    lunch_join_in.save()
    lunch_join_in.pay_fee(user_cees)
    assert lunch_join_in.debit(user_cees) == 6.5, "User must have higher debit"
