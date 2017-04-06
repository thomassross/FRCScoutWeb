from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse, reverse_lazy

from jinja2 import Environment


def environment(**options):
    env = Environment(**options)

    env.globals.update({
        "static": staticfiles_storage.url,
        "url": reverse,
        "url_lazy": reverse_lazy
    })

    return env
