# WebCase Settings

Global and User settings per package registry.

## Installation

```sh
pip install wc-django-settings
```

In `settings.py`:

```python
INSTALLED_APPS += [
  'wcd_settings',
]

MIDDLEWARE += [
  'wcd_settings.middleware.settings_middleware',
]
```
