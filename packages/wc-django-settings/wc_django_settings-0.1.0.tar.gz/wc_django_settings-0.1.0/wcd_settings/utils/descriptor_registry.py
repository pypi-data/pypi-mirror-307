from typing import List, Optional, Sequence, Tuple, Union
from django.utils.module_loading import import_string
from collections import OrderedDict
# from rest_framework import serializers
from django import forms
from django_jsonform.widgets import JSONFormWidget


__all__ = (
    'registry_choices',
    'Descriptor', 'DescriptorRegistry', 'DescriptorDisplayDRFField',
    'registry_schema_field_override_init_runner',
)


def registry_choices(import_path: str):
    def resolver():
        # HACK!
        # Getting around a circular dependency error...
        try:
            registry = import_string(import_path)
        except ImportError as e:
            return []

        return registry.choices()

    return resolver


class Descriptor:
    key: str
    verbose_name: str

    def __init__(
        self,
        key: str,
        verbose_name: Optional[str] = None,
        **kwargs,
    ):
        self.key = key
        self.verbose_name = (
            verbose_name if verbose_name is not None else key.title()
        )
        self.__inject_parameters__(kwargs)

    def __inject_parameters__(self, parameters: dict):
        for key, value in parameters.items():
            setattr(self, key, value)


class DescriptorRegistry(OrderedDict):
    def check(self, descriptor: Descriptor):
        assert not self.registered(descriptor.key), f'{descriptor.key} already registered.'

    def register(self, descriptor: Descriptor):
        self.check(descriptor)

        self[descriptor.key] = descriptor

        return descriptor

    def registered(self, name: str) -> bool:
        return name in self

    def choices(self) -> List[Tuple[str, str]]:
        return [
            (key, descriptor.verbose_name)
            for key, descriptor in self.items()
        ]

    def multiregister(self, descriptors: Sequence[Union[str, Descriptor]]):
        for descriptor in descriptors:
            self.register(
                import_string(descriptor)
                if isinstance(descriptor, str) else
                descriptor
            )


# class DescriptorDisplayDRFField(serializers.CharField):
#     def __init__(self, registry: DescriptorRegistry, **kwargs):
#         self.registry = registry
#         super().__init__(**kwargs)

#     def to_representation(self, value):
#         descriptor: Descriptor = self.registry.get(value)

#         return {
#             'id': value,
#             'title': descriptor.verbose_name if descriptor is not None else value.title(),
#         }


def registry_schema_formfield_for_dbfield(
    admin, db_field, request, super_method, kwargs,
    schema_resolver=lambda x, **kw: None,
):
    kwargs = {**kwargs, 'widget': JSONFormWidget(
        schema=lambda i: schema_resolver(
            i, admin=admin, db_field=db_field, request=request,
        )
    )}
    return super_method(db_field, request, **kwargs)


def registry_schema_field_override_init_runner(
    admin, form,
    schema_resolver=lambda *a: (),
    kwargs={}, disable_schemaless=False,
):
    instance = getattr(form, 'instance', None)
    schemas = schema_resolver(instance, form, admin, kwargs)
    fields = form.fields

    for field_name, widget_kwargs in schemas:
        schema = widget_kwargs.get('schema', None)

        if field_name not in fields:
            continue

        field = fields[field_name]

        if schema:
            widget = JSONFormWidget(**widget_kwargs)
            widget.instance = instance

            if widget.get_schema():
                field.widget = widget

            continue

        if disable_schemaless:
            field.disabled = True
            field.widget = forms.HiddenInput()
