from django.urls import reverse


__all__ = 'admin_change_url', 'admin_add_url', 'admin_changelist_url',


def admin_change_url(obj):
    """
    Return admin change url for given object
    """
    app_label = obj._meta.app_label
    model_name = obj._meta.model.__name__.lower()
    return reverse(f'admin:{app_label}_{model_name}_change', args=(obj.pk,))


def admin_add_url(obj):
    """
    Return admin change url for given object
    """
    app_label = obj._meta.app_label
    model_name = obj._meta.model.__name__.lower()
    return reverse(f'admin:{app_label}_{model_name}_add', args=(obj.pk,))


def admin_changelist_url(model):
    """
    Return admin change list url fir given model
    """
    app_label = model._meta.app_label
    model_name = model.__name__.lower()
    return reverse(f'admin:{app_label}_{model_name}_changelist')
