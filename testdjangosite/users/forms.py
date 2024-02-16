from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = get_user_model()


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-Mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists:
            raise forms.ValidationError('Такой E-Mail уже используется')
        return email
