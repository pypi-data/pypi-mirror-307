import strawberry_django
from .filtersets import RiskAssignmentFilterSet
from .models import RiskAssignment

from netbox.graphql.filter_mixins import autotype_decorator, BaseFilterMixin

__all__ = (
    'RiskAssignmentFilter',
)


@strawberry_django.filter(RiskAssignment, lookups=True)
@autotype_decorator(RiskAssignmentFilterSet)
class RiskAssignmentFilter(BaseFilterMixin):
    pass