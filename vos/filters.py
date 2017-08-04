from django import template

register = template.Library()

@register.filter()

def get(dict, index):
	retrun dict[index]
