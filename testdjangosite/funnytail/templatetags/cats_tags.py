from django import template
import funnytail.views as views
from funnytail.models import Breed, TagPosts

register = template.Library()


@register.inclusion_tag('funnytail/list_categories.html')
def show_categories(category_selected=0):
    categories = Breed.objects.all()
    return {'categories': categories, 'category_selected': category_selected}


@register.inclusion_tag('funnytail/list_tags.html')
def show_all_tags():
    return {'tags': TagPosts.objects.all()}
