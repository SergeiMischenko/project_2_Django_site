from django import template
from django.db.models import Count

import funnytail.views as views
from funnytail.models import Breed, TagPosts

register = template.Library()


@register.inclusion_tag('funnytail/list_categories.html')
def show_categories(category_selected=0):
    categories = Breed.objects.annotate(total=Count("posts")).filter(total__gt=0)
    return {'categories': categories, 'category_selected': category_selected}


@register.inclusion_tag('funnytail/list_tags.html')
def show_all_tags():
    return {'tags': TagPosts.objects.annotate(total=Count("posts")).filter(total__gt=0)}
