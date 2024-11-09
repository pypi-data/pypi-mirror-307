from typing import *


__all__ = 'StatefulFormAdminMixin',


class StatefulFormAdminMixin:
    add_form = None
    add_fieldsets = None
    add_inlines = None
    change_form = None

    def get_add_form(self, request, **kwargs):
        return self.add_form

    def get_change_form(self, request, obj, **kwargs):
        return self.change_form

    def get_form(self, request, obj=None, **kwargs):
        form = None

        if obj is None and self.add_form is not None:
            form = self.get_add_form(request, **kwargs)

        if obj is not None:
            form = self.get_change_form(request, obj, **kwargs)

        if form is not None:
            kwargs['form'] = form

        return super().get_form(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        self.inlines = self.__class__.inlines

        if obj is None and self.add_inlines is not None:
            self.inlines = self.add_inlines

        if obj is None and self.add_fieldsets is not None:
            return self.add_fieldsets

        return super().get_fieldsets(request, obj)
