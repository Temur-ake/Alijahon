from datetime import datetime

from django.template import Library

register = Library()


@register.filter()
def current_cat_slug(path: str):
    return path.split('/')[-1]


@register.filter()
def customlen(itr):
    return len(itr)


@register.filter()
def minus(price, discount):
    return price - discount


@register.filter('spliter')
def split_path(path) -> str:
    return path.split('/')[-2]


@register.filter('distinct')
def distinct(value) -> set:
    category_list = set()
    if value not in category_list:
        category_list.add(value)
        return category_list
    return set()


@register.filter('remove_nulls')
def remove_nulls(value):
    return str(value)[:-2]
