from django import template 
from django.utils.html import format_html
from django.shortcuts import render
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag(takes_context=True)
def render_content(context, item):
    request = context["request"]
    if item._meta.model_name == 'text':
        return format_html("<h3>{}</h3><p>{}</p>", item.title, item.content)
    elif item._meta.model_name == 'image':
        return format_html("<img src={} />", item.file.url)
    elif item._meta.model_name == 'file':
        return format_html("<p>{}</p>", item.content)
    elif item._meta.model_name == 'video':
        return render_to_string( 'courses/content/video.html', {'item' : item} )



    return format_html("<h1>hi i'm cotent</h1>")
    