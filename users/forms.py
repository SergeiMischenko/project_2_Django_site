from datetime import date

from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       UserCreationForm)


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин или E-Mail")

    class Meta:
        model = get_user_model()


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователя")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput())
    this_year = date.today().year
    date_birth = forms.DateField(
        widget=forms.SelectDateWidget(
            years=tuple(range(this_year - 100, this_year - 5))
        ),
        label="День Рождения",
    )
    captcha = CaptchaField(
        label="Что на картинке", error_messages={"invalid": "Неправильная каптча"}
    )

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "date_birth",
            "photo",
            "password1",
            "password2",
        ]
        labels = {
            "email": "E-Mail",
            "first_name": "Имя",
            "last_name": "Фамилия",
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-Mail уже используется")
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label="Логин")
    email = forms.CharField(disabled=True, required=False, label="E-Mail")
    this_year = date.today().year
    date_birth = forms.DateField(
        widget=forms.SelectDateWidget(
            years=tuple(range(this_year - 100, this_year - 5))
        ),
        label="День Рождения",
    )

    class Meta:
        model = get_user_model()
        fields = ["photo", "username", "email", "date_birth", "first_name", "last_name"]
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput())
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput())
    new_password2 = forms.CharField(
        label="Повторите пароль", widget=forms.PasswordInput()
    )
