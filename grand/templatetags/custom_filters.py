from django import template

register = template.Library()

@register.filter
def sum_attribute(queryset, attr):
    return sum(getattr(obj, attr, 0) for obj in queryset)
