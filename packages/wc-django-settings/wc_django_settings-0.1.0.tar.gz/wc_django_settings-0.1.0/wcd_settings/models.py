from typing import *
from django.conf import settings
from django.utils.translation import pgettext_lazy
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from wcd_settings.utils.dynamic_choices_field import DynamicChoicesField
from wcd_settings.utils.descriptor_registry import registry_choices


__all__ = 'SettingsBase', 'AppSettings', 'UserSettings'


class SettingsQuerySet(models.QuerySet):
    pass


class SettingsBase(models.Model):
    objects = SettingsQuerySet.as_manager()

    class Meta:
        verbose_name = pgettext_lazy('wcd_settings', 'Settings')
        verbose_name_plural = pgettext_lazy('wcd_settings', 'Settings')
        abstract = True

    key = DynamicChoicesField(
        verbose_name=pgettext_lazy('wcd_settings', 'Key'),
        choices=registry_choices(
            'wcd_settings.registries.app_settings_registry'
        ),
        max_length=128, blank=False, null=False,
    )
    config = models.JSONField(
        verbose_name=pgettext_lazy('wcd_settings', 'Config'),
        encoder=DjangoJSONEncoder, default=dict, blank=True, null=False,
    )

    created_at = models.DateTimeField(
        verbose_name=pgettext_lazy('wcd_settings', 'Created at'),
        auto_now_add=True, blank=False, null=False, db_index=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=pgettext_lazy('wcd_settings', 'Updated at'),
        auto_now=True, blank=False, null=False, db_index=True,
    )

    def __str__(self):
        return self.get_key_display()


class AppSettings(SettingsBase):
    class Meta:
        verbose_name = pgettext_lazy('wcd_settings', 'App settings')
        verbose_name_plural = pgettext_lazy('wcd_settings', 'Apps settings')

    key = DynamicChoicesField(
        verbose_name=pgettext_lazy('wcd_settings', 'Key'),
        choices=registry_choices(
            'wcd_settings.registries.app_settings_registry'
        ),
        max_length=128, blank=False, null=False, unique=True,
    )


class UserSettings(SettingsBase):
    class Meta:
        verbose_name = pgettext_lazy('wcd_settings', 'User settings')
        verbose_name_plural = pgettext_lazy('wcd_settings', 'Users settings')
        unique_together = (
            ('key', 'user'),
        )

    key = DynamicChoicesField(
        verbose_name=pgettext_lazy('wcd_settings', 'Key'),
        choices=registry_choices(
            'wcd_settings.registries.user_settings_registry'
        ),
        max_length=128, blank=False, null=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=pgettext_lazy('wcd_settings', 'User'),
        related_name='wcd_user_settings',
        on_delete=models.CASCADE, blank=False, null=False,
    )
