from typing import *


__all__ = 'FormInitRunnersAdminMixin',


class InitRunnableFormMixin:
    _admin_instance = None
    _form_init_kwargs = {}

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.__form_init_run__()

    def __form_init_run__(self):
        admin = self._admin_instance
        kwargs = {**self._form_init_kwargs}

        for init_runner in admin.get_form_init_runners():
            init_runner(admin, self, kwargs=kwargs)


class FormInitRunnersAdminMixin:
    form_init_runners: Iterable[Callable] = ()

    def get_form_init_runners(self):
        return [*self.form_init_runners, self.init_form_runner]

    def init_form_runner(self, admin, form, kwargs={}):
        pass

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj=obj, change=change, **kwargs)
        kwargs['form'] = form

        return self.make_init_runnable_form(
            request, obj=obj, change=change, **kwargs
        )

    def make_init_runnable_form(
        self, request, form, obj=None, change=False, **kwargs
    ):
        Form = type(f'{form.__name__}InitRunnable', (InitRunnableFormMixin, form,), {
            '_admin_instance': self,
            '_form_init_kwargs': {'request': request, 'obj': obj, **kwargs},
        })

        return Form
