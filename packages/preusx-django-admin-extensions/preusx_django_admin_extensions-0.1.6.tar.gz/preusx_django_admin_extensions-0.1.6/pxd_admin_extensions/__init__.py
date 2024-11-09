__version__ = '0.1.6'

from .annotations import *
from .multidb import *
from .form_types import *
from .changelist_template_names import *
from .stateful_form import *
from .field_overrider import *
from .form_entities_instance_injector import *
from .form_init_runners import *
from .decorators import *
from .extended_template import *
from .model_save import *

from .urls import *
from .formatters import *
from .filters import *

VERSION = tuple(__version__.split('.'))
