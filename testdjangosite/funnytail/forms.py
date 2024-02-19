from django import forms

from .models import Breed, TagPosts, Cats


class PostForm(forms.ModelForm):
    breed = forms.ModelChoiceField(queryset=Breed.objects.all(), empty_label='Не выбрана', label='Порода')
    tags = forms.ModelMultipleChoiceField(queryset=TagPosts.objects.all(), widget=forms.CheckboxSelectMultiple,
                                          required=False, label='Теги')

    class Meta:
        model = Cats
        fields = ['title', 'slug', 'content', 'preview', 'is_published', 'breed', 'tags']
        labels = {
            'slug': 'URL'
        }

