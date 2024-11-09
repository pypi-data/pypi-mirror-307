from typing import *
from functools import partial
from django.http import HttpRequest
from django.utils.functional import SimpleLazyObject

from wcd_settings.resolvers import (
    make_app_resolver, make_user_resolver,
)
from wcd_settings.setters import make_app_setter, make_user_setter


__all__ = 'settings_middleware',


def settings_middleware(get_reqponse, request: Optional[HttpRequest] = None):
    if request is None:
        return partial(settings_middleware, get_reqponse)

    if not hasattr(request, 'app_settings'):
        request.app_settings = SimpleLazyObject(lambda: make_app_setter(make_app_resolver()))

    if not hasattr(request, 'user_settings'):
        request.user_settings = SimpleLazyObject(lambda: make_user_setter(make_user_resolver()))

    return get_reqponse(request)
