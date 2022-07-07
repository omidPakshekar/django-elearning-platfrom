from django import template 
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def render_content(item):
    print()
    if item._meta.model_name == 'text':
        return format_html("<h3>{}</h3><p>{}</p>", item.title, item.content)
    elif item._meta.model_name == 'image':
        print(item.file)
        return format_html("<h3>{}</h3><img src={} /><p>{}</p>", item.title, item.file.url, item.content)
    elif item._meta.model_name == 'file':
        return format_html("<h3>{}</h3><p>{}</p>", item.title, item.content)
    elif item._meta.model_name == 'video':
        video_ = "{% video %s 'small' %}" % (item.url)
        return format_html("<h3>{}</h3> {} <p>{}</p>", item.title, video_, item.content)
        
    


    return format_html("<h1>hi i'm cotent</h1>")
    