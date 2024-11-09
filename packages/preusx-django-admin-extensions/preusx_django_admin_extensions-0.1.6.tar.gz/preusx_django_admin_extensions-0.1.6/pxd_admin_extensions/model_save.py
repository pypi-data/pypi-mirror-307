from typing import *
from django.forms import BaseModelFormSet, ModelForm
from django.http import HttpRequest


__all__ = 'ModelAllSavedAdminMixin',


class ModelAllSavedAdminMixin:
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        request._saved_admin_params = request, obj, form, change

    def save_related(
        self,
        request: HttpRequest,
        form: ModelForm,
        formsets: BaseModelFormSet,
        change: bool,
    ) -> None:
        super().save_related(request, form, formsets, change)
        saved = getattr(request, '_saved_admin_params', None)

        if saved is not None:
            _, obj, _, _ = saved
            self.on_model_all_saved(request, obj, form, formsets, change)

    def on_model_all_saved(
        self,
        request: HttpRequest,
        obj,
        form: ModelForm,
        formsets: BaseModelFormSet,
        change: bool,
    ) -> None:
        pass
