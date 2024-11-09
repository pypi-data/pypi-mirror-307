from typing import *
from typing import Sequence, Tuple
from pydantic import BaseModel, ValidationError
from django.db.models import QuerySet
from wcd_settings.registries import Registry, SettingsDescriptor
from wcd_settings.models import SettingsBase, AppSettings, UserSettings
from wcd_settings.registries import app_settings_registry, user_settings_registry


__all__ = (
    'SettingsResolver', 'AppSettingsResolver', 'UserSettingsResolver',
    'make_app_resolver', 'make_user_resolver',
)

K = TypeVar('K')
M = TypeVar('M', bound=BaseModel)


class SettingsResolver(Generic[K, M]):
    registry: Registry
    queryset: Optional[QuerySet] = None
    storage: Dict[K, M]
    db_instances: Dict[K, SettingsBase]

    def __init__(
        self,
        registry: Optional[Registry] = None,
        queryset: Optional[QuerySet] = None,
    ):
        registry = (
            registry
            if registry is not None else
            getattr(self, 'registry', None)
        )

        assert registry is not None, (
            '`registry` must be specified on a resolver or passed on init.'
        )

        self.registry = registry
        self.queryset = queryset
        self.clear()

    def get_queryset(self) -> QuerySet:
        result = self.queryset

        assert result is not None, (
            '`queryset` must be specified on a resolver or '
            '`get_queryset` method must be re-implemented.'
        )

        return result

    def filter_queryset(self, queryset: QuerySet, keys: Sequence[K]) -> QuerySet:
        return queryset.filter(key__in=keys)

    def get_descriptor(self, key: Union[str, K]) -> Optional[SettingsDescriptor]:
        return self.registry.get(key)

    def make_key(self, instance: SettingsBase) -> K:
        return instance.key

    def make_dto(self, key: Union[str, K], config: dict) -> Optional[M]:
        descriptor = self.get_descriptor(key)

        if descriptor is None:
            return None

        try:
            return descriptor.dto.model_validate(config)
        except ValidationError:
            try:
                return descriptor.dto()
            except ValidationError as e:
                return None

    def to_item(self, instance: SettingsBase) -> Optional[Tuple[K, M]]:
        model = self.make_dto(instance.key, instance.config)

        if model is None:
            return None

        return self.make_key(instance), model

    def inject(self, instance: SettingsBase):
        item = self.to_item(instance)

        if item is None:
            return

        key, model = item
        self.db_instances[key] = instance
        self.storage[key] = model

    def know(self, keys: Sequence[K]):
        self.known.update(keys)

    def is_known(self, key: K) -> bool:
        return key in self.known

    def collect(self, keys: Sequence[K]):
        queryset = self.filter_queryset(self.get_queryset(), keys)
        self.know(keys)

        for instance in queryset:
            self.inject(instance)

    def prepare(self, keys: Sequence[K]):
        keys = [k for k in keys if not self.is_known(k)]

        if len(keys) == 0:
            return

        self.collect(keys)

    def clear(self):
        self.known = set()
        self.storage = {}
        self.db_instances = {}

    def get(self, key: K) -> Optional[M]:
        self.prepare([key])

        if key not in self.storage:
            return self.make_dto(key, {})

        return self.storage[key]

    def get_db_instance(self, key: K) -> Optional[SettingsBase]:
        self.prepare([key])

        return self.db_instances.get(key)


class AppSettingsResolver(SettingsResolver[str, BaseModel]):
    def clear(self):
        super().clear()

        self.is_prepared = False

    def filter_queryset(self, queryset: QuerySet, keys: Sequence[K]) -> QuerySet:
        return queryset.all()

    def is_known(self, key: str) -> bool:
        return self.is_prepared

    def prepare(self, keys: Sequence[K]):
        super().prepare(keys)
        self.is_prepared = True


class UserSettingsResolver(SettingsResolver[Tuple[Hashable, str], BaseModel]):
    def get_descriptor(self, key: Union[str, Tuple[Hashable, str]]) -> Optional[SettingsDescriptor]:
        if isinstance(key, (tuple, list)):
            _, key = key

        return super().get_descriptor(key)

    def make_key(self, instance: UserSettings) -> Tuple[Hashable, str]:
        return instance.user_id, instance.key

    def filter_queryset(self, queryset: QuerySet, keys: Sequence[Tuple[Hashable, str]]) -> QuerySet:
        uids = {uid for uid, _ in keys} - {None, 0}

        if len(uids) == 0:
            return queryset.none()

        return queryset.filter(user_id__in=uids)

    def is_known(self, key: Tuple[Hashable, str]) -> bool:
        uid, _ = key
        return uid in self.known

    def know(self, keys: Sequence[Tuple[Hashable, str]]):
        self.known.update(uid for uid, _ in keys)


def make_app_resolver(registry: Optional[Registry] = None) -> AppSettingsResolver:
    return AppSettingsResolver(
        registry=registry if registry is not None else app_settings_registry,
        queryset=AppSettings.objects.all(),
    )


def make_user_resolver(registry: Optional[Registry] = None) -> UserSettingsResolver:
    return UserSettingsResolver(
        registry=registry if registry is not None else user_settings_registry,
        queryset=UserSettings.objects.all(),
    )
