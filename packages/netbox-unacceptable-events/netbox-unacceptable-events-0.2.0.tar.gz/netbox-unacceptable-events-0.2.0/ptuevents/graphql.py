from typing import Annotated, List

import strawberry
import strawberry_django
from .filters import PTUEventAssignmentFilter, PTAppSystemAssignmentFilter
from .models import PTUEvent, PTUEventRelation, PTUEventAssignment, PTAppSystem, PTAppSystemAssignment

from django.contrib.contenttypes.models import ContentType
from tenancy.models import Tenant


# PTContentTypeType (для ContentType, используемое в GenericForeignKey)
@strawberry_django.type(
    model=ContentType,
    fields="__all__",
)
class PTContentTypeType:
    pass

# PTTenantType (необходим для использования в PTAppSystemType)
@strawberry_django.type(
    model=Tenant,
    fields="__all__",
)
class PTTenantType:
    pass


# PTUEventType
@strawberry_django.type(
    model=PTUEvent,
    fields="__all__",
)
class PTUEventType:
    pass


# PTUEventRelationType
@strawberry_django.type(
    model=PTUEventRelation,
    fields="__all__",
)
class PTUEventRelationType:
    pass


# PTUEventAssignmentType с GenericForeignKey и внешними ключами
@strawberry_django.type(
    model=PTUEventAssignment,
    fields="__all__",
    filters=PTUEventAssignmentFilter,
)
class PTUEventAssignmentType:
    ptuevent: Annotated["PTUEventType", strawberry_django.field()]  # Внешний ключ на PTUEvent
    relation: Annotated["PTUEventRelationType", strawberry_django.field()]  # Внешний ключ на PTUEventRelation
    object_type: Annotated["PTContentTypeType", strawberry_django.field()]  # Внешний ключ на ContentType
    object: Annotated[str, strawberry_django.field()]  # Поле GenericForeignKey возвращается как строка или можно добавить логику


# PTAppSystemType с использованием PTTenantType
@strawberry_django.type(
    model=PTAppSystem,
    fields="__all__",
)
class PTAppSystemType:
    tenant: Annotated["PTTenantType", strawberry_django.field()]  # Внешний ключ на Tenant


# PTAppSystemAssignmentType с GenericForeignKey и внешними ключами
@strawberry_django.type(
    model=PTAppSystemAssignment,
    fields="__all__",
    filters=PTAppSystemAssignmentFilter,
)
class PTAppSystemAssignmentType:
    object_type: Annotated["PTContentTypeType", strawberry_django.field()]  # Внешний ключ на ContentType
    object: Annotated[str, strawberry_django.field()]  # Поле GenericForeignKey возвращается как строка или можно добавить логику
    app_system: Annotated["PTAppSystemType", strawberry_django.field()]  # Внешний ключ на PTAppSystem




@strawberry.type
class Query:
    # Получение одного PTUEvent по ID
    @strawberry.field
    def ptuevent(self, id: int) -> PTUEventType:
        return PTUEvent.objects.get(pk=id)

    # Получение списка PTUEvent
    ptuevent_list: List[PTUEventType] = strawberry_django.field()

    # Получение одного PTUEventRelation по ID
    @strawberry.field
    def relation(self, id: int) -> PTUEventRelationType:
        return PTUEventRelation.objects.get(pk=id)

    # Получение списка PTUEventRelation
    relation_list: List[PTUEventRelationType] = strawberry_django.field()

    # Получение одного PTUEventAssignment по ID
    @strawberry.field
    def ptuevent_assignment(self, id: int) -> PTUEventAssignmentType:
        return PTUEventAssignment.objects.get(pk=id)

    # Получение списка PTUEventAssignment
    ptuevent_assignment_list: List[PTUEventAssignmentType] = strawberry_django.field()

    # Получение одного PTAppSystem по ID
    @strawberry.field
    def ptapp_system(self, id: int) -> PTAppSystemType:
        return PTAppSystem.objects.get(pk=id)

    # Получение списка PTAppSystem
    ptapp_system_list: List[PTAppSystemType] = strawberry_django.field()

    # Получение одного PTAppSystemAssignment по ID
    @strawberry.field
    def ptapp_system_assignment(self, id: int) -> PTAppSystemAssignmentType:
        return PTAppSystemAssignment.objects.get(pk=id)

    # Получение списка PTAppSystemAssignment
    ptapp_system_assignment_list: List[PTAppSystemAssignmentType] = strawberry_django.field()


# Создание схемы
schema = [Query]