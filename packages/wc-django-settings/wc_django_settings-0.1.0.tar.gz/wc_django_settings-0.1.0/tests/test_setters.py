from typing import *
import pytest
import logging
from django.contrib.auth.models import User
from wcd_settings.registries import (
    SettingsDTO, UserSettingsDescriptor, AppSettingsDescriptor, Registry,
)
from wcd_settings.resolvers import AppSettingsResolver, UserSettingsResolver
from wcd_settings.models import AppSettings, UserSettings
from wcd_settings.setters import SettingsSetter, SettingsSetAction


@pytest.mark.django_db
def test_app_save(django_assert_num_queries):
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

    with django_assert_num_queries(0):
        resolver = AppSettingsResolver(
            registry=registry, queryset=AppSettings.objects.all(),
        )
        setter = SettingsSetter(resolver, lambda key, dto: AppSettings(key=key))

    with django_assert_num_queries(1):
        entry: Optional[Simple] = resolver.get('wcd_settings:test:simple')

    assert entry is not None
    entry = entry.model_copy()
    entry.title = 'test2'

    with django_assert_num_queries(2):
        setter.save('wcd_settings:test:simple', entry)

    with django_assert_num_queries(0):
        entry2: Optional[Simple] = resolver.get('wcd_settings:test:simple')

    assert id(entry) != id(entry2)
    assert entry2.title == 'test2'

    resolver.clear()

    with django_assert_num_queries(1):
        entry: Optional[Simple] = resolver.get('wcd_settings:test:simple')

    assert isinstance(entry, Simple)
    assert entry.title == 'test2'



@pytest.mark.django_db
def test_user_save(django_assert_num_queries):
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

    with django_assert_num_queries(0):
        resolver = UserSettingsResolver(
            registry=registry, queryset=UserSettings.objects.all(),
        )
        setter = SettingsSetter(
            resolver,
            lambda key, dto: UserSettings(key=key[1], user_id=key[0]),
        )

    with django_assert_num_queries(1):
        entry: Optional[Simple] = resolver.get((user.pk, 'wcd_settings:test:simple'))

    assert entry is not None
    entry = entry.model_copy()
    entry.title = 'test2'

    with django_assert_num_queries(2):
        setter.save((user.pk, 'wcd_settings:test:simple'), entry)

    with django_assert_num_queries(0):
        entry2: Optional[Simple] = resolver.get((user.pk, 'wcd_settings:test:simple'))

    assert id(entry) != id(entry2)
    assert entry2.title == 'test2'

    resolver.clear()

    with django_assert_num_queries(1):
        entry: Optional[Simple] = resolver.get((user.pk, 'wcd_settings:test:simple'))

    assert isinstance(entry, Simple)
    assert entry.title == 'test2'

    user2 = User.objects.create_user(username='test2', password='test')

    entry = entry.model_copy()
    entry.title = 'test3'

    with django_assert_num_queries(2) as q:
        setter.save((user2.pk, 'wcd_settings:test:simple'), entry)

    resolver.clear()

    with django_assert_num_queries(1):
        uentry: Optional[Simple] = resolver.get((user.pk, 'wcd_settings:test:simple'))

    assert uentry.title == 'test2'

    with django_assert_num_queries(1):
        u2entry: Optional[Simple] = resolver.get((user2.pk, 'wcd_settings:test:simple'))

    assert u2entry.title == 'test3'

    resolver.clear()

    with django_assert_num_queries(1):
        resolver.prepare([
            (user.pk, 'wcd_settings:test:simple'),
            (user2.pk, 'wcd_settings:test:simple'),
        ])

    with django_assert_num_queries(0):
        uentry: Optional[Simple] = resolver.get((user.pk, 'wcd_settings:test:simple'))

    assert uentry.title == 'test2'

    with django_assert_num_queries(0):
        u2entry: Optional[Simple] = resolver.get((user2.pk, 'wcd_settings:test:simple'))

    assert u2entry.title == 'test3'
