from typing import *
from functools import partial
from django.contrib import admin

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
from wcd_settings.utils.descriptor_registry import (
    DescriptorRegistry,
    registry_schema_field_override_init_runner,
)
from wcd_2factor.models import MethodConfig, UserConfig, ConfirmationState
from wcd_2factor.registries import method_config_registry
from wcd_2factor.services import default_setter


def config_schema_resolver(instance, form, admin, kwargs):
    schema = None
    path = admin.config_path

    if instance is not None and admin.config_registry is not None:
        descriptor = admin.config_registry.get(instance.method)

        if descriptor is not None:
            schema = descriptor

            for field in path:
                schema = getattr(schema, field, None)

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
    config_registry = method_config_registry
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
    ordering = '-created_at',
    readonly_fields = 'created_at', 'updated_at',


to_extend = (Admin,)

try:
    from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin


    to_extend = (TabbedDjangoJqueryTranslationAdmin, *to_extend)
except ImportError:
    pass


@admin.register(MethodConfig)
class MethodConfigAdmin(*to_extend):
    config_path = 'method',
    list_display = (
        '__str__', 'method',
        'is_active', 'is_default',
        'created_at', 'updated_at',
    )
    list_filter = 'method', 'is_active', 'is_default',
    date_hierarchy = 'updated_at'
    search_fields = 'config',
    fieldsets = (
        (None, {'fields': ('title', 'method',)}),
        (None, {'fields': (('is_active', 'is_default',),)}),
        (None, {'fields': ('config',)}),
        (None, {'fields': (('created_at', 'updated_at',),)}),
    )

    def on_model_all_saved(self, request, obj, form, formsets, change: bool) -> None:
        if obj.is_default:
            default_setter.set_method(method_config=obj)


@admin.register(UserConfig)
class UserConfigAdmin(Admin):
    config_path = 'method_config', 'method',
    list_display = (
        '__str__', 'status', 'method_config', 'user',
        'is_active', 'is_default',
        'created_at', 'updated_at',
    )
    date_hierarchy = 'updated_at'
    list_select_related = 'user', 'method_config',
    list_filter = 'user', 'method_config', 'status', 'is_active', 'is_default',
    autocomplete_fields = 'user', 'method_config',
    search_fields = 'config',
    fieldsets = (
        (None, {'fields': (('title', 'status',),)}),
        (None, {'fields': (('method_config', 'user',),)}),
        (None, {'fields': (('is_active', 'is_default',),)}),
        (None, {'fields': ('config',)}),
        (None, {'fields': (('created_at', 'updated_at',),)}),
    )

    def on_model_all_saved(self, request, obj, form, formsets, change: bool) -> None:
        if obj.is_default:
            default_setter.set_user(user_config=obj)


@admin.register(ConfirmationState)
class ConfirmationStateAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'status', 'method_config', 'user_config',
        'created_at', 'updated_at',
    )
    date_hierarchy = 'created_at'
    list_filter = 'method_config', 'user_config__user', 'status',
    search_fields = 'state',
    fieldsets = (
        (None, {'fields': ('status',)}),
        (None, {'fields': (('method_config', 'user_config',),)}),
        (None, {'fields': ('state',)}),
        (None, {'fields': (('created_at', 'updated_at',),)}),
    )
    ordering = '-created_at',
    readonly_fields = 'created_at', 'updated_at',
