from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserRegistrationForm, UserLogin


class RegisterFormView(CreateView):

    template_name = 'registration/register.html'
    form_class = UserRegistrationForm

    def get_success_url(self):
        return reverse_lazy('login')


class UserLoginView(LoginView):

    template_name = 'registration/login.html'
    form_class = UserLogin

    def get_success_url(self):
        return reverse_lazy('main_page_url')


class UserLogoutView(LogoutView):
    template_name = 'registration/logout.html'


class UserPasswordResetView(PasswordResetView):
    template_name = 'password/password-reset.html'


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password/password-reset-done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password/password-reset-confirm.html'

    def get_success_url(self):
        return reverse_lazy('password_reset_complete')


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password/password-reset-complete.html'
