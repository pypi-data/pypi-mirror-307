from typing import *
import json

from django.utils.html import mark_safe
from django.utils.translation import pgettext_lazy


__all__ = (
    'make_json_data_field',
    'render_html_table',
    'prettify_json',
)


def make_json_data_field(
    field: str,
    verbose_name: str = pgettext_lazy('admin_utils', 'Json data')
):
    def json_data(self, obj):
        return mark_safe(prettify_json(getattr(obj, field, {})))
    json_data.short_description = verbose_name

    return json_data


def render_html_table(data: List[Tuple]) -> str:
    html = '<table style="border: 1px solid #ecf2f6;"><tbody>'
    for line in data:
        html += '<tr><td>'
        html += '</td><td>'.join(line)
        html += '</td></tr>'
    html += '</tbody></table>'
    return html


def prettify_json(data: Dict) -> str:
    return ''.join([
        '<span style="white-space: pre-wrap; font-family: monospace">',
            json.dumps(data, ensure_ascii=False, indent=4, default=str),
        '</span>',
    ])
