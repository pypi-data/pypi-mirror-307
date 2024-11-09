from typing import *
import pytest
import logging
from django.contrib.auth.models import User, AnonymousUser
from wcd_settings.registries import (
    SettingsDTO, UserSettingsDescriptor, AppSettingsDescriptor, Registry,
)
from wcd_settings.resolvers import (
    AppSettingsResolver, UserSettingsResolver,
    make_app_resolver, make_user_resolver,
)
from wcd_settings.setters import make_app_setter, make_user_setter
from wcd_settings.models import AppSettings, UserSettings
from wcd_settings.views import AppSettingsAll, UserSettingsAll


class RawResponseMixin:
    def render_to_response(self, context):
        return context


@pytest.mark.django_db
def test_app_view_empty(rf):
    registry = Registry()

    class Simple(SettingsDTO):
        title: Optional[str] = None

    registry.register(AppSettingsDescriptor(
        key='wcd_settings:test:simple',
        dto=Simple,
        schema=Simple.model_json_schema(),
    ))
    request = rf.get('/')
    request.app_settings = make_app_setter(make_app_resolver(registry))

    response = type('V', (RawResponseMixin, AppSettingsAll), {}).as_view()(request)

    assert len(response) == 1
    assert 'wcd_settings:test:simple' in response
    assert response['wcd_settings:test:simple']['title'] is None


@pytest.mark.django_db
def test_user_view_empty(rf):
    registry = Registry()

    class Simple(SettingsDTO):
        title: Optional[str] = None

    registry.register(UserSettingsDescriptor(
        key='wcd_settings:test:simple',
        dto=Simple,
        schema=Simple.model_json_schema(),
    ))
    request = rf.get('/')
    request.user_settings = make_user_setter(make_user_resolver(registry))
    request.user = AnonymousUser()

    response = type('V', (RawResponseMixin, UserSettingsAll), {}).as_view()(request)

    assert len(response) == 1
    assert 'wcd_settings:test:simple' in response
    assert response['wcd_settings:test:simple']['title'] is None


@pytest.mark.django_db
def test_user_view(rf):
    registry = Registry()

    class Simple(SettingsDTO):
        title: Optional[str] = None

    registry.register(UserSettingsDescriptor(
        key='wcd_settings:test:simple',
        dto=Simple,
        schema=Simple.model_json_schema(),
    ))

    user = User.objects.create_user(username='test', password='test')
    UserSettings.objects.create(
        key='wcd_settings:test:simple', config={"title": "test"},
        user_id=user.pk,
    )

    request = rf.get('/')
    request.user_settings = make_user_setter(make_user_resolver(registry))
    request.user = AnonymousUser()

    response = type('V', (RawResponseMixin, UserSettingsAll), {}).as_view()(request)

    assert len(response) == 1
    assert 'wcd_settings:test:simple' in response
    assert response['wcd_settings:test:simple']['title'] is None

    request2 = rf.get('/')
    request2.user_settings = make_user_setter(make_user_resolver(registry))
    request2.user = user

    response = type('V', (RawResponseMixin, UserSettingsAll), {}).as_view()(request2)

    assert len(response) == 1
    assert 'wcd_settings:test:simple' in response
    assert response['wcd_settings:test:simple']['title'] == 'test'
