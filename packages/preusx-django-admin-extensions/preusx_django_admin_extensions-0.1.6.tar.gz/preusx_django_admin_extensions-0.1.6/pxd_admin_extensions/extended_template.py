from django.contrib.admin import ModelAdmin


__all__ = 'ExtendedTemplateAdmin',


class ExtendedTemplateAdmin(ModelAdmin):
    change_form_template = 'admin/extended/change_form.html'
