from dataclasses import dataclass

from django.db.models import QuerySet
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


@dataclass
class ModelSearchSelectOptions:

    queryset: QuerySet
    template: str = 'ui/widgets/model_search_select_options.html'

    def get_context(self):
        return {'options': self.queryset}

    def __str__(self):
        return mark_safe(render_to_string(self.template, self.get_context()))
