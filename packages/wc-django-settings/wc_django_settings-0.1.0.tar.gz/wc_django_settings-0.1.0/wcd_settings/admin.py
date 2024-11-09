from typing import *
from functools import partial
from wcd_settings.models import AppSettings, UserSettings
from django.contrib import admin
from wcd_settings.utils.descriptor_registry import (
    DescriptorRegistry,
    registry_schema_field_override_init_runner,
)
from wcd_settings.registries import app_settings_registry, user_settings_registry
from pxd_admin_extensions import (
    MultiDBModelAdmin, ListAnnotatorAdminMixin, FormTypeAdminMixin,
    ModelAllSavedAdminMixin,
    ChangeListCustomTemplateNameAdminMixin,
    FormEntitiesInstanceInjectionAdminMixin,
    FormInitRunnersAdminMixin,
    FieldOverriderAdminMixin,
    StatefulFormAdminMixin,
    ExtendedTemplateAdmin,
)


def config_schema_resolver(instance, form, admin, kwargs):
    schema = None

    if instance is not None and admin.config_registry is not None:
        descriptor = admin.config_registry.get(instance.key)

        if descriptor is not None and descriptor.schema is not None:
            schema = descriptor.schema

    return [('config', {'schema': schema})]


class Admin(
    MultiDBModelAdmin, ListAnnotatorAdminMixin, FormTypeAdminMixin,
    ModelAllSavedAdminMixin,
    ChangeListCustomTemplateNameAdminMixin,
    FormEntitiesInstanceInjectionAdminMixin,
    FormInitRunnersAdminMixin,
    FieldOverriderAdminMixin,
    StatefulFormAdminMixin,
    ExtendedTemplateAdmin,
    admin.ModelAdmin,
):
    inject_instance_widgets = 'config',
    config_registry: Optional[DescriptorRegistry] = None
    form_init_runners = (
        *FormInitRunnersAdminMixin.form_init_runners,
        partial(
            registry_schema_field_override_init_runner,
            schema_resolver=config_schema_resolver,
            disable_schemaless=True,
        ),
    )
    readonly_fields = ('created_at', 'updated_at',)


@admin.register(AppSettings)
class AppSettingsAdmin(Admin):
    config_registry = app_settings_registry
    list_display = ('key', 'created_at', 'updated_at',)
    fieldsets = (
        (None, {'fields': ('key',)}),
        (None, {'fields': ('config',)}),
        (None, {'fields': (('created_at', 'updated_at',),)}),
    )


@admin.register(UserSettings)
class UserSettingsAdmin(Admin):
    config_registry = user_settings_registry
    list_display = ('key', 'user', 'created_at', 'updated_at',)
    date_hierarchy = 'updated_at'
    list_select_related = ('user',)
    list_filter = ('user',)
    autocomplete_fields = ('user',)
    fieldsets = (
        (None, {'fields': (('key', 'user',),)}),
        (None, {'fields': ('config',)}),
        (None, {'fields': (('created_at', 'updated_at',),)}),
    )
