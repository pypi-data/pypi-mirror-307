from typing import *


__all__ = (
    'inject_instance_init_runner',
    'FormEntitiesInstanceInjectionAdminMixin',
)


def inject_instance_init_runner(admin, form, **kwargs):
    admin = form._admin_instance
    widget_keys = admin.inject_instance_widgets
    field_keys = admin.inject_instance_fields

    if widget_keys or field_keys:
        fields = form.fields
        instance = getattr(form, 'instance', None)

        for widget in widget_keys:
            if widget in fields:
                fields[widget].widget.instance = instance

        for field in field_keys:
            if field in fields:
                fields[field].instance = instance


class FormEntitiesInstanceInjectionAdminMixin:
    inject_instance_widgets = ()
    inject_instance_fields = ()
    form_init_runners: Iterable[Callable] = (inject_instance_init_runner,)
