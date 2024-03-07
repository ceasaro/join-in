import freezegun
import pytest

from core.utils.datetime_utils import str_to_datetime


@pytest.mark.django_db
def test_join_in_ok(lunch_join_in, user_cees, user_john):
    assert lunch_join_in.name == "Lunch Test"
    with freezegun.freeze_time("2024-03-29"):
        users = lunch_join_in.users
        assert len(users) == 2
        assert user_cees in users, "User should be part of lunch JoinIn"
        assert user_john in users, "User should be part of lunch JoinIn"


@pytest.mark.django_db
@pytest.mark.parametrize("for_date, user_count, mesage", [
    ('2024-03-09', 0, "no users joined yet"),
    ('2024-03-10', 1, "Only user cees joined"),
    ('2024-03-19', 1, "Only user cees joined"),
    ('2024-03-20', 2, "Both user cees and john joined"),
])
def test_membership(for_date, user_count, mesage, lunch_join_in, user_cees, user_john):
    assert lunch_join_in.name == "Lunch Test"
    assert lunch_join_in.get_users(
        for_datetime=str_to_datetime(for_date)).count() == user_count, f"On {for_date}, {mesage}"


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


@pytest.mark.django_db
def test_revert_payment(lunch_join_in, user_cees):
    payment = lunch_join_in.pay_fee(user_cees)
    assert lunch_join_in.debit(user_cees) == 2.0, "User must have a debit"
    lunch_join_in.revert_payment(payment)
    assert lunch_join_in.debit(user_cees) == 0.0, "Payment reverted, debit should be 0.0."


