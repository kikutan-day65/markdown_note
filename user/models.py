from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# fmt: off
class CustomUser(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=150, null=False, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, null=False, blank=False)
    email = models.EmailField(_("email address"), null=False, blank=False)
    # profile_image = models.ImageField()
# fmt: on
