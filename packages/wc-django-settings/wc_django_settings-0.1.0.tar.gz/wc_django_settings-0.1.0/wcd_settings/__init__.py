__version__ = '0.1.0'

from django.utils.module_loading import autodiscover_modules

VERSION = tuple(__version__.split('.'))

default_app_config = 'wcd_settings.apps.SettingsConfig'


def autodiscover():
    autodiscover_modules('conf')
    autodiscover_modules('settings')
