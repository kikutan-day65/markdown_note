from django.urls import path

from .views import (
    UserDeleteView,
    UserDetailView,
    UserLoginView,
    UserLogoutView,
    UserPasswordChangeView,
    UserPasswordResetCompleteView,
    UserPasswordResetConfirmView,
    UserPasswordResetDoneView,
    UserPasswordResetView,
    UserRegisterView,
    UserUpdateView,
)

# fmt: off
app_name = "user"
urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("detail/<int:pk>/", UserDetailView.as_view(), name="detail"),
    path("change-password/", UserPasswordChangeView.as_view(), name="change_password"),
    path("delete-user/<int:pk>/", UserDeleteView.as_view(), name="delete_user"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="update"),

    # URL patterns for password reset
    path("password-reset/", UserPasswordResetView.as_view(), name="password_reset"),
    path("password-reset-done/", UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password-reset-confirm/<str:uidb64>/<str:token>/", UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password-reset-complete/", UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
# fmt: on
