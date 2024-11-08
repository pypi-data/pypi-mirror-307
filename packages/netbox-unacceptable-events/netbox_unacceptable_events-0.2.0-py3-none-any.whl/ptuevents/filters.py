import strawberry_django
from .filtersets import PTUEventAssignmentFilterSet, PTAppSystemAssignmentFilterSet
from .models import PTUEventAssignment, PTAppSystemAssignment

from netbox.graphql.filter_mixins import autotype_decorator, BaseFilterMixin

__all__ = (
    'PTUEventAssignmentFilter',
    'PTAppSystemAssignmentFilter',
)


@strawberry_django.filter(PTUEventAssignment, lookups=True)
@autotype_decorator(PTUEventAssignmentFilterSet)
class PTUEventAssignmentFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(PTAppSystemAssignment, lookups=True)
@autotype_decorator(PTAppSystemAssignmentFilterSet)
class PTAppSystemAssignmentFilter(BaseFilterMixin):
    pass