from typing import List

import strawberry
import strawberry_django
from .filters import RiskAssignmentFilter
from .models import Risk, RiskRelation, RiskAssignment


@strawberry_django.type(
    model=Risk,
    fields="__all__",
)
class RiskType:
    pass


@strawberry_django.type(
    model=RiskRelation,
    fields="__all__",
)
class RiskRelationType:
    pass


@strawberry_django.type(
    model=RiskAssignment,
    fields="__all__",
    filters=RiskAssignmentFilter,
)
class RiskAssingmentType:
    pass


@strawberry.type
class Query:
    @strawberry.field
    def risk(self, id: int) -> RiskType:
        return Risk.objects.get(pk=id)

    risk_list: List[RiskType] = strawberry_django.field()

    @strawberry.field
    def relation(self, id: int) -> RiskRelationType:
        return RiskRelation.objects.get(pk=id)

    relation_list: List[RiskRelationType] = strawberry_django.field()

    @strawberry.field
    def risk_assignment(self, id: int) -> RiskAssingmentType:
        return RiskAssingment.objects.get(pk=id)

    risk_assignment_list: List[RiskAssingmentType] = strawberry_django.field()


schema = [Query]
