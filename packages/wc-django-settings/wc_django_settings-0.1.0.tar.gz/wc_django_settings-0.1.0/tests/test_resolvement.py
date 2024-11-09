from typing import *
import pytest
import logging
from django.contrib.auth.models import User
from wcd_settings.registries import (
    SettingsDTO, UserSettingsDescriptor, AppSettingsDescriptor, Registry,
)
from wcd_settings.resolvers import AppSettingsResolver, UserSettingsResolver
from wcd_settings.models import AppSettings, UserSettings


@pytest.mark.django_db
def test_registration(caplog):

    registry = Registry()

    class Simple(SettingsDTO):
        title: str

    with caplog.at_level(logging.WARNING):
        registry.register(AppSettingsDescriptor(
            key='wcd_settings:test:simple',
            dto=Simple,
            schema=Simple.model_json_schema(),
        ))

    assert 'Model for wcd_settings:test:simple can\'t be initialized empty.' in caplog.text

    caplog.clear()


    class Simple2(SettingsDTO):
        title: Optional[str] = None


    with caplog.at_level(logging.WARNING):
        registry.register(AppSettingsDescriptor(
            key='wcd_settings:test:simple2',
            dto=Simple2,
            schema=Simple2.model_json_schema(),
        ))

    assert caplog.text == ''


@pytest.mark.django_db
def test_app_resolver_empty():
    registry = Registry()

    class Simple(SettingsDTO):
        title: Optional[str] = None

    registry.register(AppSettingsDescriptor(
        key='wcd_settings:test:simple',
        dto=Simple,
        schema=Simple.model_json_schema(),
    ))

    resolver = AppSettingsResolver(
        registry=registry, queryset=AppSettings.objects.all(),
    )
    entry: Optional[Simple] = resolver.get('wcd_settings:test:simple')

    assert entry is not None
    assert isinstance(entry, Simple)
    assert entry.title is None


@pytest.mark.django_db
def test_user_resolver_empty():
    registry = Registry()

    class Simple(SettingsDTO):
        title: Optional[str] = None

    registry.register(UserSettingsDescriptor(
        key='wcd_settings:test:simple',
        dto=Simple,
        schema=Simple.model_json_schema(),
    ))

    resolver = UserSettingsResolver(
        registry=registry, queryset=UserSettings.objects.all(),
    )
    entry: Optional[Simple] = resolver.get((1, 'wcd_settings:test:simple'))

    assert entry is not None
    assert isinstance(entry, Simple)
    assert entry.title is None


@pytest.mark.django_db
def test_user_resolver():
    registry = Registry()

    class Simple(SettingsDTO):
        title: Optional[str] = None


    user = User.objects.create_user(username='test', password='test')
    UserSettings.objects.create(
        key='wcd_settings:test:simple', config={"title": "test"},
        user_id=user.pk,
    )

    registry.register(UserSettingsDescriptor(
        key='wcd_settings:test:simple',
        dto=Simple,
        schema=Simple.model_json_schema(),
    ))

    resolver = UserSettingsResolver(
        registry=registry, queryset=UserSettings.objects.all(),
    )
    entry: Optional[Simple] = resolver.get((user.pk, 'wcd_settings:test:simple'))

    assert entry is not None
    assert isinstance(entry, Simple)
    assert entry.title == 'test'

    false_entry: Optional[Simple] = resolver.get((user.pk + 1, 'wcd_settings:test:simple'))

    assert false_entry is not None
    assert isinstance(false_entry, Simple)
    assert false_entry.title is None


@pytest.mark.django_db
def test_app_resolver(django_assert_num_queries):
    registry = Registry()

    class Simple(SettingsDTO):
        title: Optional[str] = None

    AppSettings.objects.create(
        key='wcd_settings:test:simple', config={"title": "test"},
    )

    registry.register(AppSettingsDescriptor(
        key='wcd_settings:test:simple',
        dto=Simple,
        schema=Simple.model_json_schema(),
    ))

    resolver = AppSettingsResolver(
        registry=registry, queryset=AppSettings.objects.all(),
    )

    with django_assert_num_queries(1):
        entry: Optional[Simple] = resolver.get('wcd_settings:test:simple')

    assert entry is not None
    assert isinstance(entry, Simple)
    assert entry.title == 'test'

    with django_assert_num_queries(0):
        entry: Optional[Simple] = resolver.get('wcd_settings:test:simple')

    assert entry.title == 'test'
