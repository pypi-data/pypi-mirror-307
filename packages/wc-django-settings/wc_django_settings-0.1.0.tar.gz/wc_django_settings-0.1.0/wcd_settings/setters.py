from typing import *
from functools import partial
from django.db import models
from django.utils.translation import pgettext_lazy, pgettext
from pydantic import ValidationError
from collections import defaultdict

from wcd_settings.resolvers import (
    SettingsResolver, UserSettingsResolver, AppSettingsResolver,
)
from wcd_settings.registries import SettingsDTO
from wcd_settings.models import AppSettings, UserSettings


__all__ = (
    'SettingsSetAction', 'AppSettingsSetAction', 'UserSettingsSetAction',
    'SettingsSetter',
    'app_instance_factory', 'user_instance_factory',
    'AppSettingsSetter', 'UserSettingsSetter',
    'make_app_setter', 'make_user_setter',
)

PathType = List[Union[str, int]]


class SettingsSetAction(SettingsDTO):
    key: Hashable
    path: PathType
    value: Any


class AppSettingsSetAction(SettingsSetAction):
    key: str


class UserSettingsSetAction(SettingsSetAction):
    key: Tuple[int, str]


A = TypeVar('A', bound=SettingsSetAction)
M = TypeVar('M', bound=models.Model)
R = TypeVar('R', bound=SettingsResolver)


class SettingsSetter(Generic[A, R, M]):
    def __init__(
        self,
        resolver: R,
        instance_factory: Callable[[Hashable, SettingsDTO], M],
    ):
        self.resolver = resolver
        self.instance_factory = instance_factory

    def find_groups(self, dtos: List[A]):
        grouped = defaultdict(list)

        for dto in dtos:
            grouped[dto.key].append(dto)

        resolver = self.resolver
        resolver.collect(grouped.keys())

        return [
            (key, resolver.get(key), resolver.get_db_instance(key), dtos)
            for key, dtos in grouped.items()
        ]

    def apply(
        self,
        instance: M,
        settings: SettingsDTO,
        dtos: List[A],
    ) -> Tuple[M, List[Tuple[A, Exception]]]:
        if len(dtos) == 0:
            return instance, []

        result = settings.model_copy()
        failures = []

        for dto in dtos:
            # TODO:
            # assert len(dto.path) < 2, 'Path with more that one parameter is not yet fully supported.'

            try:
                if len(dto.path) == 0:
                    result = dto.value
                    continue
                else:
                    current = result

                    for key in dto.path[:-1]:
                        current = getattr(current, key)
                        # TODO:
                        assert current is not None, (
                            'Autocreation on settings path is not supported.'
                        )

                    setattr(current, dto.path[-1], dto.value)

            except ValidationError as e:
                failures.append((dto, e))
            except AssertionError as e:
                failures.append((dto, e))

        instance.config = result.model_dump()

        return instance, failures

    def commit(
        self,
        to_create: List[Tuple[M, bool]],
        to_update: List[Tuple[M, bool]],
        partial: bool = False,
    ):
        creatables = [i for i, f in to_create if partial or f]
        updatables = [i for i, f in to_update if partial or f]

        if len(creatables) > 0:
            model = creatables[0].__class__
            model.objects.bulk_create(creatables)

        if len(updatables) > 0:
            model = updatables[0].__class__
            model.objects.bulk_update(updatables, ['config'])

        ready = creatables + updatables

        for i in ready:
            self.resolver.inject(i)

        return ready

    def set(self, dtos: List[A]):
        groups = self.find_groups(dtos)
        failures: Dict[Hashable, List[Tuple[PathType, Exception]]] = defaultdict(list)
        to_create = []
        to_update = []

        for key, settings, instance, gdtos in groups:
            if settings is None:
                failures[key] = [
                    ([], KeyError(pgettext(
                        'wcd_settings:error', 'No settings found for {key}'
                    ).format(key=key)))
                ]
                continue

            change_group = to_update

            if instance is None:
                instance = self.instance_factory(key, settings)
                change_group = to_create

            instance, i_failures = self.apply(instance, settings, gdtos)
            fully = len(i_failures) == 0

            for dto, e in i_failures:
                failures[key].append((dto.path, e))

            change_group.append((instance, fully))

        return partial(self.commit, to_create, to_update), failures

    def save(self, key: Hashable, dto: SettingsDTO):
        results, failures = self.set([SettingsSetAction(key=key, path=[], value=dto)])

        if len(failures) > 0:
            raise failures[key][0][1]

        return results()[0]


def app_instance_factory(key: str, settings: SettingsDTO):
    return AppSettings(key=key)


def user_instance_factory(key: Tuple[int, str], settings: SettingsDTO):
    uid, settings_key = key
    return UserSettings(key=settings_key, user_id=uid)


AppSettingsSetter = SettingsSetter[AppSettingsSetAction, AppSettingsResolver, AppSettings]
UserSettingsSetter = SettingsSetter[UserSettingsSetAction, UserSettingsResolver, UserSettings]

def make_app_setter(resolver: AppSettingsResolver) -> AppSettingsSetter:
    return SettingsSetter(resolver, instance_factory=app_instance_factory)


def make_user_setter(resolver: UserSettingsResolver) -> UserSettingsSetter:
    return SettingsSetter(resolver, instance_factory=user_instance_factory)
