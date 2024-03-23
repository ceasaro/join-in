from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models

from core.exceptions import TransactionException, JoinInException
from core.utils.datetime_utils import utc_now

User = get_user_model()


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class JoinIn(BaseModel):
    DAILY = 'daily'
    PERIOD_CHOICES = [(DAILY, 'Daily')]
    group = models.OneToOneField(Group, on_delete=models.CASCADE, primary_key=True)
    slug = models.SlugField(max_length=20, null=False, blank=False)
    fee = models.DecimalField(max_digits=10, decimal_places=4)
    membership_period = models.CharField(choices=PERIOD_CHOICES, default=DAILY, max_length=50)

    def join(self, user):
        self.group.user_set.add(user)
        Membership.objects.create(join_in=self, user=user)

    def toggle_fee(self, user, for_datetime=utc_now()):
        try:
            self.add_fee(user, for_datetime)
        except JoinInException:
            self.revert_loan(Loan.objects.get(join_in=self, user=user, created__day=for_datetime.day))

    def add_fee(self, user, for_datetime=utc_now()):
        if self.membership_period == self.DAILY:
            if Loan.objects.filter(join_in=self, user=user, created__day=for_datetime.day).exists():
                raise JoinInException(f"{user} already added the fee for this period")
        return Loan.objects.create(join_in=self, user=user, amount=self.fee)

    def revert_loan(self, loan):
        if loan.join_in != self:
            raise TransactionException(f"Cannot revert loan {loan}, it was not for JoinIn {self}")
        loan.delete()

    def payment(self, user, amount):
        return Payment.objects.create(join_in=self, user=user, amount=amount)

    def revert_payment(self, payment):
        if payment.join_in is not self:
            raise TransactionException(f"Cannot revert payment {payment},"
                                       f" it was not for JoinIn {self}")
        payment.delete()

    def balance(self, user, for_datetime):
        loans = Loan.objects.filter(join_in=self, user=user, created__lte=for_datetime).aggregate(models.Sum('amount'))
        payments = Payment.objects.filter(join_in=self, user=user, created__lte=for_datetime).aggregate(models.Sum('amount'))
        return (payments['amount__sum'] or Decimal(0.0)) - (loans['amount__sum'] or Decimal(0.0))

    @property
    def name(self):
        return self.group.name

    @property
    def users(self):
        return self.get_users(for_datetime=utc_now())

    def get_users(self, for_datetime):
        users = (self.group.user_set.filter(
            joined__join_in=self, joined__join_datetime__lte=for_datetime).filter(
            models.Q(joined__left_datetime__gte=for_datetime)
            | models.Q(joined__left_datetime__isnull=True)))
        return users


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='joined')
    join_in = models.ForeignKey(JoinIn, on_delete=models.CASCADE, related_name='joined')
    join_datetime = models.DateTimeField(auto_now_add=True)
    left_datetime = models.DateTimeField(null=True, blank=True)


class Loan(BaseModel):
    join_in = models.ForeignKey(JoinIn, on_delete=models.CASCADE, related_name="loans")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")
    amount = models.DecimalField(max_digits=10, decimal_places=4)


class Payment(BaseModel):
    join_in = models.ForeignKey(JoinIn, on_delete=models.CASCADE, related_name="payments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=4)
