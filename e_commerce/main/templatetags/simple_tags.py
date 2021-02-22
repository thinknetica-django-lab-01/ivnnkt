from django.template.defaultfilters import stringfilter
from django import template
import datetime


register = template.Library()


@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


@register.filter
@stringfilter
def revers_string(a_string):
    return a_string[::-1]
