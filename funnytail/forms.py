from captcha.fields import CaptchaField
from django import forms

from .models import Breed, Cats, Comment, TagPosts


class PostForm(forms.ModelForm):
    breed = forms.ModelChoiceField(
        queryset=Breed.objects.all(), empty_label="Не выбрана", label="Порода"
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=TagPosts.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Теги",
    )
    captcha = CaptchaField(
        label="Что на картинке", error_messages={"invalid": "Неправильная каптча"}
    )

    class Meta:
        model = Cats
        fields = [
            "title",
            "slug",
            "content",
            "preview",
            "is_published",
            "breed",
            "tags",
        ]
        labels = {"slug": "URL"}


class ContactForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=255)
    email = forms.EmailField(label="Email")
    message = forms.CharField(widget=forms.Textarea, label="Сообщение")
    captcha = CaptchaField(
        label="Что на картинке", error_messages={"invalid": "Неправильная каптча"}
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            "name",
            "email",
            "body",
        )


class SearchForm(forms.Form):
    query = forms.CharField(label="Что ищем?")
