from typing import *
import logging
from pydantic import BaseModel, ValidationError, ConfigDict
from pydantic.alias_generators import to_camel
from wcd_settings.utils.descriptor_registry import (
    DescriptorRegistry, Descriptor,
)


__all__ = (
    'SettingsDTO',
    'AppSettingsDescriptor', 'UserSettingsDescriptor',
    'Registry',
    'app_settings_registry', 'user_settings_registry',
)

logger = logging.getLogger(__name__)


class SettingsDTO(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        extra='allow',
    )


class SettingsDescriptor(Descriptor):
    dto: Type[SettingsDTO]
    schema: dict


class AppSettingsDescriptor(SettingsDescriptor):
    pass


class UserSettingsDescriptor(SettingsDescriptor):
    pass


class Registry(DescriptorRegistry):
    def check(self, descriptor: SettingsDescriptor):
        try:
            super().check(descriptor)
        except AssertionError as e:
            logger.warning(e, exc_info=True)

        try:
            descriptor.dto()
        except ValidationError as e:
            logger.warning(
                f'Model for {descriptor.key} can\'t be initialized empty. \n',
                exc_info=True,
            )


app_settings_registry = Registry()
user_settings_registry = Registry()
