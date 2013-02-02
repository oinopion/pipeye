from django import template
from pipeye.utils.urls import url

register = template.Library()


@register.inclusion_tag('watches/_watch_button.html', takes_context=True)
def watch_button(context, package):
    action, text = url('create_watch', package), 'Watch this package'
    return {'action': action, 'text': text}
