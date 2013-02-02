from django import template
from pipeye.utils.urls import url

register = template.Library()


@register.inclusion_tag('watches/_watch_button.html', takes_context=True)
def watch_button(context, package):
    user = context['user']
    if package.watch_set.filter(user=user).exists():
        action, text = url('delete_watch', package), 'Stop watching this package'
    else:
        action, text = url('create_watch', package), 'Watch this package'
    return {'action': action, 'text': text}
