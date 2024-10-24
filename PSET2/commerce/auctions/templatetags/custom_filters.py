from django import template
import re

register = template.Library()

@register.filter
def first_sentence(value):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', value)
    return sentences[0] if sentences else value