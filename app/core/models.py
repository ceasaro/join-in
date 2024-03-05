from django.contrib.auth.models import Group
from django.db import models


class JoinIn(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, primary_key=True)
    slug = models.SlugField(max_length=20, null=False, blank=False)

    @property
    def name(self):
        return self.group.name

    @property
    def users(self):
        return self.group.user_set.all()