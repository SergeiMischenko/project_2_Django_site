from django import template
import funnytail.views as views

register = template.Library()


@register.inclusion_tag('funnytail/list_categories.html')
def show_categories(category_selected=0):
    categories = views.cats_db
    return {'categories': categories, 'category_selected': category_selected}
