from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from .messages import LOGOUT_SUCCESS

CustomUser = get_user_model()


@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    messages.success(request, LOGOUT_SUCCESS)
