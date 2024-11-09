from typing import *


__all__ = 'FieldOverriderAdminMixin',


class FieldOverriderAdminMixin:
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        name = db_field.name

        if name in self.formfield_overrides:
            kwargs = {**self.formfield_overrides[name], **kwargs}

        attmethod = getattr(self, f'formfield_for_dbfield_{name}', None)
        super_method = super().formfield_for_dbfield

        if attmethod is not None:
            return attmethod(
                db_field, request, super_method=super_method, kwargs=kwargs,
            )

        return super_method(db_field, request, **kwargs)
