import logging
from datetime import datetime, date, timedelta
from django.utils.translation import gettext_lazy as _
from django import template
from django.db.models import Manager
from django.forms import Form, ModelForm
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from accrete.contrib.ui import TableField, TableFieldType

_logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag(name='combine_templates')
def combine_templates(template_name, request=None):
    html = ''
    for app in settings.INSTALLED_APPS:
        try:
            html += render_to_string(
                f'{app.split(".")[-1]}/{template_name}', request=request
            )
        except template.TemplateDoesNotExist:
            continue
    return mark_safe(html)


@register.filter(name='field_attr')
def get_attr_from_field(obj: object, field: TableField):

    def return_save(attr):
        if isinstance(attr, Manager):
            return attr.related_model
        if attr is None:
            return None
        if isinstance(attr, str):
            return attr
        return attr

    f_name = field.name
    if field.field_type == TableFieldType.CHOICE_DISPLAY:
        f_name = f'get_{f_name}_display'

    try:
        attribute = getattr(obj, f_name, False)
    except (AttributeError,):
        _logger.warning(f'Object {obj} has no attribute {f_name}')
        attribute = None
    return return_save(attribute)


@register.filter(name='get_attr')
def get_attr_from_string(param: object, value: str):

    def return_save(attr):
        if isinstance(attr, Manager) and hasattr(attr, 'related_model'):
            return attr.related_model
        if attr is None:
            return None
        if isinstance(attr, str):
            return attr
        return attr

    try:
        attribute = getattr(param, value, False)
    except (AttributeError,):
        _logger.warning(f'Object {param} has no attribute {value}')
        attribute = None
    return return_save(attribute)


@register.filter(name='related_obj_url')
def related_obj_url(param: object, value: str):
    attr = getattr(param, value, False)
    if attr and hasattr(attr, 'get_absolute_url'):
        return attr.get_absolute_url()
    return '#'


@register.filter(name='message_class')
def message_class(param):
    if param.level == 25:
        return 'is-success'
    if param.level == 30:
        return 'is-warning'
    if param.level == 40:
        return 'is-danger'


@register.filter(name='non_field_error_code')
def non_field_error_code(form: [Form|ModelForm], code: str) -> bool:
    if not form:
        return False
    for error in form.non_field_errors().as_data():
        if error.code and error.code == code:
            return True
    return False


@register.filter(name='extract_non_field_error')
def extract_non_field_error(form: [Form|ModelForm], code: str) -> str:
    if not form:
        return ''
    errors = []
    for error in form.non_field_errors().as_data():
        if error.code and error.code == code:
            errors.append(str(error.message))
    return mark_safe('<br>'.join(errors))


@register.filter(name='timedelta_cast')
def timedelta_cast(td: timedelta, code: str) -> str | None:
    if not isinstance(td, timedelta):
        return None
    codes = ['days', 'hours', 'minutes', 'seconds', 'microseconds']
    if code not in codes:
        return None
    return str(getattr(td, code))


@register.filter(name='weekday')
def datetime_to_weekday(dt: datetime|date, default=None) -> str:
    if dt is None:
        return default
    mapping = {
        1: _('Mon'),
        2: _('Tue'),
        3: _('Wed'),
        4: _('Thu'),
        5: _('Fri'),
        6: _('Sat'),
        7: _('Sun')
    }
    return mapping[dt.isoweekday()]
