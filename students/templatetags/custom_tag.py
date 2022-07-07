from django import template 
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def render_content(item):
    print()
    if item._meta.model_name == 'text':
        return format_html("<h4>{}</h4><p>{}</p>", item.title, item.content)
    return format_html("<h1>hi i'm cotent</h1>")
    