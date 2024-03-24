from datetime import datetime

import freezegun
import pytest

from core.exceptions import JoinInException
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
@pytest.mark.parametrize("for_date, user_count, message", [
    ('2024-03-09', 0, "no users joined yet"),
    ('2024-03-10', 1, "Only user cees joined"),
    ('2024-03-19', 1, "Only user cees joined"),
    ('2024-03-20', 2, "Both user cees and john joined"),
])
def test_membership(for_date, user_count, message, lunch_join_in, user_cees, user_john):
    assert lunch_join_in.name == "Lunch Test"
    assert lunch_join_in.get_users(
        for_datetime=str_to_datetime(for_date)).count() == user_count, f"On {for_date}, {message}"


@pytest.mark.django_db
def test_balance(lunch_join_in, user_cees):
    # day 8 March
    d_2024_03_08 = str_to_datetime("2024-03-08")
    assert lunch_join_in.balance(d_2024_03_08,
                                 user_cees) == 0.0, "User hasn't joined yet and should have no debit"
    lunch_join_in.add_fee(user_cees, d_2024_03_08)
    assert lunch_join_in.balance(d_2024_03_08, user_cees) == -2.0, "User must have a debit"

    # day 9 March
    lunch_join_in.add_fee(user_cees, str_to_datetime("2024-03-09"))

    # day 10 March
    d_2024_03_10 = str_to_datetime("2024-03-10")
    lunch_join_in.fee = 2.5
    lunch_join_in.save()
    lunch_join_in.add_fee(user_cees, str_to_datetime("2024-03-10 12:35"))
    assert lunch_join_in.balance(d_2024_03_10, user_cees) == -6.5, "User must have higher debit"
    with freezegun.freeze_time(d_2024_03_10):
        lunch_join_in.payment(user_cees, 10)
    assert lunch_join_in.balance(d_2024_03_10,
                                 user_cees) == 3.5, "User paid and have some credit now"


@pytest.mark.django_db
def test_join_within_period(lunch_join_in, user_cees):
    lunch_join_in.add_fee(user_cees)
    with pytest.raises(JoinInException, match=f"{user_cees} already added the fee for this period"):
        lunch_join_in.add_fee(user_cees)


@pytest.mark.django_db
def test_revert_loan(lunch_join_in, user_cees):
    payment = lunch_join_in.add_fee(user_cees, datetime.now())
    assert lunch_join_in.balance(datetime.now(), user_cees) == -2.0, "User must have a debit"
    lunch_join_in.revert_loan(payment)
    assert lunch_join_in.balance(datetime.now(),
                                 user_cees) == 0.0, "Payment reverted, debit should be 0.0."


