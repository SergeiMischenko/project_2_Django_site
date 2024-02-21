from django import template
from django.db.models import Count

import funnytail.views as views
from funnytail.models import Breed, TagPosts

register = template.Library()


@register.inclusion_tag('funnytail/list_categories.html')
def show_categories(category_selected):
    categories = Breed.objects.filter(posts__gte=1).distinct()
    return {'categories': categories, 'category_selected': category_selected}


@register.inclusion_tag('funnytail/list_tags.html')
def show_all_tags():
    return {'tags': TagPosts.objects.filter(posts__gte=1).distinct()}
