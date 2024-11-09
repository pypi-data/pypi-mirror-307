from django.apps import AppConfig
from django.utils.translation import pgettext_lazy


__all__ = 'SettingsConfig',


class SettingsConfig(AppConfig):
    name = 'wcd_settings'
    verbose_name = pgettext_lazy('wcd_settings', 'Settings')

    def ready(self) -> None:
        self.module.autodiscover()
