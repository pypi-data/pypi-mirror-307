from typing import *

from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse as HttpResponse
from django.views import View
from django.http import HttpRequest, JsonResponse

from wcd_settings.setters import SettingsSetter
from wcd_settings import shortcuts


__all__ = (
    'BaseView', 'DetailView',
    'AppSettingsAll', 'UserSettingsAll',
    'app_settings_all_view', 'user_settings_all_view', 'make_urlpatterns',
)


class BaseView(View):
    def render_to_response(self, context):
        return JsonResponse(context)


class DetailView(BaseView):
    include: Optional[List[str]] = None
    exclude: Optional[List[str]] = None

    def all_keys(self, settings: SettingsSetter, request: HttpRequest):
        keys = settings.resolver.registry.keys()
        include = self.include if self.include is not None else keys
        exclude = self.exclude if self.exclude is not None else []
        return [k for k in keys if k in include and k not in exclude]

    def settings(self, request: HttpRequest):
        return {}

    def get(self, request: HttpRequest):
        return self.render_to_response(self.settings(request))


class AppSettingsAll(DetailView):
    def settings(self, request: HttpRequest):
        settings = shortcuts.app_settings(request)
        all_keys = self.all_keys(settings, request)
        resolver = settings.resolver
        resolver.prepare(all_keys)

        return {
            key: dto.model_dump(mode='json')
            for key, dto in ((k, resolver.get(k)) for k in all_keys)
            if dto is not None
        }


class UserSettingsAll(DetailView):
    guest_user_id: int = 0

    def settings(self, request: HttpRequest):
        user_id = request.user.pk if request.user.is_authenticated else self.guest_user_id
        settings = shortcuts.user_settings(request)
        all_keys = [(user_id, k) for k in self.all_keys(settings, request)]
        resolver = settings.resolver
        resolver.prepare(all_keys)

        return {
            key: dto.model_dump(mode='json')
            for (_, key), dto in ((k, resolver.get(k)) for k in all_keys)
            if dto is not None
        }


app_settings_all_view = AppSettingsAll.as_view()
user_settings_all_view = UserSettingsAll.as_view()


def make_urlpatterns(
    app_settings_all=app_settings_all_view,
    user_settings_all=user_settings_all_view,
):
    return [
        path('app/', include(([
            path('all/', csrf_exempt(app_settings_all), name='all'),
        ], 'app'))),
        path('own/', include(([
            path('all/', csrf_exempt(user_settings_all), name='all'),
        ], 'own'))),
    ]
