from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def is_past_date(date):
    return date.date() < timezone.now().date()

@register.filter
def is_future_date(date):
    return date.date() > timezone.now().date()
