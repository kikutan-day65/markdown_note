from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from .forms import (
    UserLoginForm,
    UserPasswordChangeForm,
    UserRegisterForm,
    UserUpdateForm,
)
from .messages import (
    ACCOUNT_DELETE_SUCCESS,
    LOGIN_SUCCESS,
    PASSWORD_CHANGE_SUCCESS,
    REGISTER_SUCCESS,
    USER_UPDATE_SUCCESS,
)

CustomUser = get_user_model()


class UserRegisterView(SuccessMessageMixin, CreateView):
    template_name = "user/user_register.html"
    model = CustomUser
    form_class = UserRegisterForm
    success_url = reverse_lazy("user:login")
    success_message = REGISTER_SUCCESS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["register_form"] = context.get("form")
        return context

    def form_invalid(self, form):
        for field, error in form.errors.items():
            error_message = strip_tags(error)
            messages.error(self.request, error_message)
        return super().form_invalid(form)


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = "user/user_login.html"
    next_page = reverse_lazy("home:home_page")
    form_class = UserLoginForm
    success_message = LOGIN_SUCCESS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_form"] = context.get("form")
        return context

    def form_invalid(self, form):
        for field, error in form.errors.items():
            error_message = strip_tags(error)
            messages.error(self.request, error_message)
        return super().form_invalid(form)


class UserLogoutView(SuccessMessageMixin, LogoutView):
    next_page = reverse_lazy("home:home_page")


class UserDetailView(DetailView):
    template_name = "user/user_detail.html"
    model = CustomUser
    context_object_name = "user_detail"


class UserPasswordChangeView(
    LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView
):
    template_name = "user/user_password_change.html"
    form_class = UserPasswordChangeForm
    login_url = reverse_lazy("user:login")
    success_message = PASSWORD_CHANGE_SUCCESS

    def get_success_url(self):
        return reverse("user:detail", kwargs={"pk": self.request.user.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["password_change_form"] = context.get("form")
        return context

    def form_invalid(self, form):
        for field, error in form.errors.items():
            error_message = strip_tags(error)
            messages.error(self.request, error_message)
        return super().form_invalid(form)


class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = "common/delete.html"
    model = CustomUser
    context_object_name = "user_obj"
    login_url = reverse_lazy("user:login")
    success_url = reverse_lazy("home:home_page")
    success_message = ACCOUNT_DELETE_SUCCESS

    def get_queryset(self):
        return CustomUser.objects.filter(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_delete"] = True
        return context


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "user/user_update.html"
    model = CustomUser
    form_class = UserUpdateForm
    login_url = reverse_lazy("user:login")
    success_message = USER_UPDATE_SUCCESS

    def get_queryset(self):
        return super().get_queryset().filter(pk=self.request.user.pk)

    def get_success_url(self):
        return reverse("user:detail", kwargs={"pk": self.request.user.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_update_form"] = context.get("form")
        return context

    def form_invalid(self, form):
        for field, error in form.errors.items():
            error_message = strip_tags(error)
            messages.error(self.request, error_message)
        return super().form_invalid(form)


class UserPasswordResetView(PasswordResetView):
    template_name = "user/user_password_reset.html"
    email_template_name = "user/email/user_password_reset_body.txt"
    html_email_template_name = "user/email/user_password_reset_body.html"
    subject_template_name = "user/email/user_password_reset_subject.txt"
    success_url = reverse_lazy("user:password_reset_done")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["password_reset_form"] = context.get("form")
        return context


class UserPasswordResetDoneView(PasswordResetDoneView):
    """パスワードリセットメールが送信後に表示されるビュー"""

    template_name = "user/user_password_reset_done.html"


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    """パスワードリセットメールのリンクを押下した時に表示されるビュー"""

    template_name = "user/user_password_reset_confirm.html"
    success_url = reverse_lazy("user:password_reset_complete")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["password_reset_confirm_form"] = context.get("form")
        return context

    def form_invalid(self, form):
        for field, error in form.errors.items():
            error_message = strip_tags(error)
            messages.error(self.request, error_message)
        return super().form_invalid(form)


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    """パスワードリセットが完了したあとに表示されるビュー"""

    template_name = "user/user_password_reset_complete.html"
