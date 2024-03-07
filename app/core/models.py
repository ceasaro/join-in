from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models

from core.exceptions import PaymentException
from core.utils.datetime_utils import utc_now

User = get_user_model()


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class JoinIn(BaseModel):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, primary_key=True)
    slug = models.SlugField(max_length=20, null=False, blank=False)
    fee = models.DecimalField(max_digits=10, decimal_places=4)

    def join(self, user):
        self.group.user_set.add(user)
        Membership.objects.create(join_in=self, user=user)

    def pay_fee(self, user):
        return Payment.objects.create(join_in=self, user=user, fee=self.fee)

    def revert_payment(self, payment):
        if not self.payments.filter(id=payment.id).exists():
            raise PaymentException(f"Cannot revert payment {payment}, it was not for JoinIn {self}")
        payment.delete()

    def debit(self, user):
        fees = Payment.objects.filter(join_in=self, user=user).aggregate(models.Sum('fee'))
        return fees['fee__sum'] or 0.0

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
        for user in users:
            user.payed_for_period = True
        return users


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='joined')
    join_in = models.ForeignKey(JoinIn, on_delete=models.CASCADE, related_name='joined')
    join_datetime = models.DateTimeField(auto_now_add=True)
    left_datetime = models.DateTimeField(null=True, blank=True)


class Payment(BaseModel):
    join_in = models.ForeignKey(JoinIn, on_delete=models.CASCADE, related_name="payments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    fee = models.DecimalField(max_digits=10, decimal_places=4)
