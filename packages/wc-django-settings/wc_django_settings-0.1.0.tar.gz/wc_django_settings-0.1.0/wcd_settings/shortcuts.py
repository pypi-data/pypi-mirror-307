from typing import *
from django.http import HttpRequest

from wcd_settings.resolvers import (
    make_app_resolver, make_user_resolver,
)
from wcd_settings.setters import (
    make_app_setter, make_user_setter,
    AppSettingsSetter, UserSettingsSetter,
)


__all__ = 'app_settings', 'user_settings',


def app_settings(request: Optional[HttpRequest] = None) -> AppSettingsSetter:
    setter = getattr(request, 'app_settings', None)

    if setter is not None:
        return setter

    return make_app_setter(make_app_resolver())


def user_settings(request: Optional[HttpRequest] = None) -> UserSettingsSetter:
    setter = getattr(request, 'user_settings', None)

    if setter is not None:
        return setter

    return make_user_setter(make_user_resolver())
