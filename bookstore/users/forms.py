from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm,
    AuthenticationForm
)

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserLogin(AuthenticationForm):
    class Meta:
        model = User
        fields = ('email', 'password')


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
