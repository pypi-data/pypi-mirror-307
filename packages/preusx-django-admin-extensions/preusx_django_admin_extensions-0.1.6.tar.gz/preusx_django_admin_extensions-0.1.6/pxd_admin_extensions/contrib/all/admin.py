from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from admin_numeric_filter.admin import NumericFilterModelAdmin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django_better_admin_arrayfield.forms.fields import DynamicArrayField

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


__all__ = 'AllAdmin',


class AllAdmin(
    DynamicArrayMixin,
    ListAnnotatorAdminMixin,
    NumericFilterModelAdmin,
    FormTypeAdminMixin,
    ModelAllSavedAdminMixin,
    ChangeListCustomTemplateNameAdminMixin,
    FormEntitiesInstanceInjectionAdminMixin,
    FormInitRunnersAdminMixin,
    FieldOverriderAdminMixin,
    StatefulFormAdminMixin,
    ExtendedTemplateAdmin,
    MultiDBModelAdmin,
    admin.ModelAdmin
):
    """All the admin features in one place.
    """
    empty_value_display = '-----'

    formfield_overrides = {
        ArrayField: {'form_class': DynamicArrayField},
    }
