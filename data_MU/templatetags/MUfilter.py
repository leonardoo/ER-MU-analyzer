from django import template

register = template.Library()

@register.filter(is_safe=True)
def type(obj):
	print type(obj)
	return type(obj)