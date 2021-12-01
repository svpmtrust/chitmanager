from django import template
from collections import defaultdict

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if key in dictionary:
        return dictionary.get(key)
    else:
        return '-'

counters = defaultdict(int)

@register.filter
def counter_subtract(value, counter_name):
    counters[counter_name] -= int(value)
    return counters[counter_name]

@register.filter
def counter_add(value, counter_name):
    counters[counter_name] += int(value)
    return counters[counter_name]

@register.filter
def counter_subtract_only(value, counter_name):
    counters[counter_name] -= int(value)
    return ''

@register.filter
def counter_add_only(value, counter_name):
    counters[counter_name] += int(value)
    return ''

@register.filter
def counter_reset(value, counter_name):
    counters.pop(counter_name, None)
    return ''

@register.filter
def counter_recall(value, counter_name):
    return counters[counter_name]

@register.filter
def add_loan(a,b):
    return a + b
