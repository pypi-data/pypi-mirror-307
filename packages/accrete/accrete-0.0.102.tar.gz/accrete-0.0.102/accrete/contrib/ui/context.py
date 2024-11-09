import logging
import json
from urllib.parse import quote_plus
from uuid import uuid4
from dataclasses import dataclass, field
from functools import partial
from typing import Type, TypedDict
from django.utils.translation import gettext_lazy as _t
from django.db import models
from django.db.models import Model, QuerySet
from django.core.paginator import Paginator
from django.core import paginator, exceptions
from django.forms import Form, ModelForm
from accrete.annotation import Annotation
from accrete.utils.views import cast_param
from .elements import (
    ClientAction, BreadCrumb, TableField, TableFieldType, TableFieldAlignment,
    ClientActionGroup
)
from .filter import Filter
from accrete.utils import filter_from_querystring

_logger = logging.getLogger(__name__)

DEFAULT_PAGINATE_BY = 40


class DetailPagination(TypedDict):
    previous_object_url: str
    next_object_url: str
    current_object_idx: int
    total_objects: int


@dataclass(kw_only=True)
class BaseContext:

    extra: dict = field(default_factory=dict)

    def __post_init__(self):
        for key, value in self.extra.items():
            setattr(self, key, value)

    def dict(self):
        return {
            attr: getattr(self, attr, None) for attr
            in filter(lambda x: not x.startswith('_'), self.__dict__)
        }


@dataclass(kw_only=True)
class Context(BaseContext):

    title: str = ''
    breadcrumbs: list[BreadCrumb] = field(default_factory=list)
    actions: list[ClientAction | ClientActionGroup] = field(default_factory=list)


@dataclass
class TableContext(Context):

    object_label: str
    fields: list[TableField]
    list_page: paginator.Page
    pagination_param_str: str
    endless_scroll: bool
    filter: Filter
    object_param_str: str = field(default='', kw_only=True)
    field_selection: bool = True


def table_context_factory(model: Type[Model], params: dict, queryset=None, **kwargs) -> TableContext:
    if queryset is None:
        queryset = filter_from_querystring(model, params)
    page = list_page(
        queryset,
        cast_param(params, 'paginate_by', int, 40),
        cast_param(params, 'page', int, 1)
    )
    try:
        has_name_field = (
            model._meta.get_field('name').get_internal_type() == 'CharField'
        )
    except exceptions.FieldDoesNotExist:
        has_name_field = False

    ctx = partial(TableContext, **dict(
        title=str(model._meta.verbose_name_plural),
        object_label=str(model._meta.verbose_name),
        object_param_str=url_param_str(
            params,
            ['q', 'paginate_by', 'page', 'fields']
        ),
        fields=get_table_fields(
            cast_param(params, 'fields', json.loads, []), model
        ),
        list_page=page,
        pagination_param_str=url_param_str(
            params, ['q', 'paginate_by', 'fields']
        ),
        endless_scroll=True,
        filter=Filter(
            model,
            default_filter_term='name__icontains' if has_name_field else ''
        )
    ))
    return ctx(**kwargs)


@dataclass
class ListContext(Context):

    object_label: str
    object_param_str: str
    list_page: paginator.Page
    pagination_param_str: str
    filter: Filter = None
    endless_scroll: bool = True
    column_width: int = 12
    column_width_widescreen: int = None
    column_width_desktop: int = None
    column_height: int = 150
    column_height_unit: str = 'px'
    field_selection: bool = False

    def __post_init__(self):
        super().__post_init__()
        if self.column_width not in range(1, 13):
            _logger.warning(
                'ListContext parameter column_width should be in range 1 - 12'
            )
        if self.column_width_widescreen is None:
            self.column_width_widescreen = self.column_width
        if self.column_width_desktop is None:
            self.column_width_desktop = self.column_width


def list_context_factory(model: Type[Model], params: dict, queryset=None, paginate_by=None, **kwargs) -> ListContext:
    if queryset is None:
        queryset = filter_from_querystring(model, params)
    page = list_page(
        queryset,
        cast_param(params, 'paginate_by', int, paginate_by or 20),
        cast_param(params, 'page', int, 1)
    )
    try:
        has_name_field = (
            model._meta.get_field('name').get_internal_type() == 'CharField'
        )
    except exceptions.FieldDoesNotExist:
        has_name_field = False

    ctx = partial(ListContext, **dict(
        title=str(model._meta.verbose_name_plural),
        object_label=str(model._meta.verbose_name),
        object_param_str=url_param_str(
            params,
            ['q', 'paginate_by', 'page']
        ),
        list_page=page,
        pagination_param_str=url_param_str(
            params, ['q', 'paginate_by']
        ),
        endless_scroll=True,
        filter=Filter(
            model,
            default_filter_term='name__icontains' if has_name_field else ''
        ),
        column_width=4,
        column_height=150
    ))
    return ctx(**kwargs)


@dataclass
class DetailContext(Context):

    object: Model
    detail_page: DetailPagination = None
    pagination_param_str: str = ''


@dataclass
class FormContext(Context):

    form: Form | ModelForm
    form_id: str = 'form'
    form_method: str = 'post'
    form_action: str = ''


@dataclass
class ModalFormContext(BaseContext):

    title: str
    form: Form | ModelForm
    form_id: str = 'form'
    blocking: bool = True


@dataclass
class ModalContext(BaseContext):

    title: str
    blocking: bool = False
    modal_id: str = None

    def __post_init__(self):
        super().__post_init__()
        if not self.modal_id:
            self.modal_id = f'modal{str(uuid4())[:8]}'


def url_param_dict(get_params: dict) -> dict:
    return {
        key: f'&{key}={quote_plus(value)}'
        for key, value in get_params.items()
    }


def url_param_str(params: dict, extract: list[str] = None) -> str:
    """
    Return a URL Querystring from the given params dict.
    If extract is supplied, only specified keys will be used.
    """
    if extract:
        params = extract_url_params(params, extract)
    param_str = (
        "".join(str(value) for value in url_param_dict(params).values())
        .replace('&&', '&')
        .replace('?&', '?')
        .strip('?&')
    )
    return f'?{param_str}'


def extract_url_params(params: dict, keys: list[str]) -> dict:
    return {key: params[key] for key in keys if key in params}


def exclude_params(params: dict, keys: list[str]) -> dict:
    return {key: val for key, val in params.items() if key not in keys}


def list_page(
        queryset: QuerySet, paginate_by: int, page_number: int
) -> paginator.Page:
    pages = Paginator(queryset, per_page=paginate_by)
    return pages.page(
        page_number <= pages.num_pages and page_number or pages.num_pages
    )


def detail_page(queryset: QuerySet, obj: Model) -> dict:
    if not hasattr(obj, 'get_absolute_url'):
        _logger.warning(
            'Detail pagination disabled for models without the '
            'get_absolute_url attribute. Set paginate_by to 0 to '
            'deactivate pagination.'
        )
        return {}
    if obj not in queryset:
        url = obj.get_absolute_url()
        return {
            'previous_object_url': url,
            'next_object_url': url,
            'current_object_idx': 1,
            'total_objects': 1
        }

    idx = (*queryset,).index(obj)
    previous_object_url = (
        queryset[idx - 1] if idx - 1 >= 0 else queryset.last()
    ).get_absolute_url()
    next_object_url = (
        queryset[idx + 1] if idx + 1 <= queryset.count() - 1 else queryset.first()
    ).get_absolute_url()
    return {
        'previous_object_url': previous_object_url,
        'next_object_url': next_object_url,
        'current_object_idx': idx + 1,
        'total_objects': queryset.count()
    }


def form_actions(discard_url: str, form_id: str = 'form') -> list[ClientAction]:
    return [
        ClientAction(
            name=_t('Save'),
            submit=True,
            class_list=['is-success'],
            form_id=form_id,
        ),
        ClientAction(
            name=_t('Discard'),
            url=discard_url
        )
    ]


def get_table_fields(
        fields: list[str],
        model: type[Model],
        field_definition: dict[str | TableField] = None
) -> list[TableField]:

    def get_alignment(field_attr) -> TableFieldAlignment:
        number_field_types = (
            models.DecimalField, models.IntegerField, models.FloatField
        )
        if (
            isinstance(field_attr, number_field_types)
            or (
                isinstance(field_attr, Annotation)
                and field_attr.field in number_field_types
            )
        ):
            return TableFieldAlignment.RIGHT
        return TableFieldAlignment.LEFT

    def get_field_definition(f_name: str) -> TableField:
        if definition := field_definition.get(f_name):
            return definition
        try:
            return model.table_field_definition[f_name]
        except (AttributeError, KeyError):
            attr = getattr(model, f_name)
            if not isinstance(attr, Annotation) and hasattr(attr, 'field'):
                attr = attr.field
        is_relation = (
            hasattr(attr, 'related_model')
            and hasattr(attr.related_model, 'get_absolute_url')
        )
        field_type = TableFieldType.NONE
        if getattr(attr, 'choices', False):
            field_type = TableFieldType.CHOICE_DISPLAY
        return TableField(
            label=attr.verbose_name,
            name=f_name,
            field_type=field_type,
            alignment=get_alignment(attr),
            is_relation=is_relation
        )

    if field_definition is None:
        field_definition = {}
    table_fields = []
    for field_name in fields:
        try:
            table_fields.append(get_field_definition(field_name))
        except AttributeError as e:
            _logger.error(e)
            pass
    return table_fields
