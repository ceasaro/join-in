from io import BytesIO

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from join_in.utils.image_generator import text_to_image


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    card_img = models.ImageField(upload_to="user_card_images", blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.card_img:
            if self.email:
                text = self.email.split('@')[0]
                img = text_to_image(text)
                image_bytes = BytesIO()
                img.save(image_bytes, format='PNG')
                # breakpoint()
                self.card_img.save(f"{text}.png", image_bytes)

    def __str__(self):
        return self.email
