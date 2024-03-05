from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models

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

    def participated(self, user):
        Participation.objects.create(join_in=self, user=user, fee=self.fee)

    def debit(self, user):
        total_fees = Participation.objects.filter(join_in=self, user=user).aggregate(models.Sum('fee'))
        return total_fees['fee__sum'] or 0.0

    @property
    def name(self):
        return self.group.name

    @property
    def users(self):
        return self.group.user_set.all()


class Participation(BaseModel):
    join_in = models.ForeignKey(JoinIn, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fee = models.DecimalField(max_digits=10, decimal_places=4)
