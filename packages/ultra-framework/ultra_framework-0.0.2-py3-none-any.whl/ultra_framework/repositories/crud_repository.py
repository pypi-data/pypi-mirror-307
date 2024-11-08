from typing import Iterable, List, Union, Callable, Type, Self, Any, Tuple

from sqlalchemy import ColumnElement, LambdaElement
from sqlalchemy.orm import Query
from sqlalchemy.sql.elements import SQLCoreOperations
from sqlalchemy.sql.roles import ExpressionElementRole, TypedColumnsClauseRole

from ultra_framework.entities.sql_entity import SQLEntity
from ultra_framework.mixins.session_mixin import SessionMixin

type Criterion[T] = Union[
    ColumnElement[T],
    SQLCoreOperations[T],
    ExpressionElementRole[T],
    TypedColumnsClauseRole[T],
    Callable[[], ColumnElement[T] | LambdaElement]
]
type AutoImplementableOne[T] = Callable[[...], T]
type AutoImplementableMany[T] = Callable[[...], Iterable[T]]


class CRUDRepository[M: SQLEntity](SessionMixin):

    entity_class: Type[M]

    def save(self, entity: M) -> None:
        self.session.add(entity)

    def find_all(self, limit: int | None = None, offset: int | None = None) -> Iterable[M]:
        query = self.session.query(self.entity_class)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        return query.all()

    def delete(self, entity: M) -> None:
        self.session.delete(entity)

    def __filter_by_conditions(self, conditions: List[Criterion[bool]],
                               limit: int | None = None, offset: int | None = None) -> Query[M]:
        query = self.session.query(self.entity_class).filter(*conditions)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        return query

    @staticmethod
    def auto_implement_many(condition_calls: List[Callable[[Any], Criterion[bool]]]
                       ) -> Callable[[AutoImplementableMany[M]], AutoImplementableMany[M]]:

        def outer(fn: AutoImplementableMany[M]) -> AutoImplementableMany[M]:

            def inner(*args, **kwargs) -> Iterable[M]:
                self: Self = args[0]
                params = args[1:]
                conditions = CRUDRepository.__handle_params(fn.__name__, params, condition_calls)

                if len(params) == len(condition_calls) + 2:
                    limit, offset = params[-2:]
                else:
                    limit = kwargs["limit"]
                    offset = kwargs["offset"]

                return self.__filter_by_conditions(conditions, limit, offset).all()

            return inner

        return outer

    @staticmethod
    def auto_implement_one(condition_calls: List[Callable[[Any], Criterion[bool]]]
                            ) -> Callable[[AutoImplementableOne[M]], AutoImplementableOne[M]]:

        def outer(fn: AutoImplementableOne[M]) -> AutoImplementableOne[M]:

            def inner(*args) -> M:
                self: Self = args[0]
                params = args[1:]
                conditions = CRUDRepository.__handle_params(fn.__name__, params, condition_calls)
                return self.__filter_by_conditions(conditions).one()

            return inner

        return outer

    @staticmethod
    def __handle_params(fn_name: str,
                        params: Tuple[Any, ...],
                        condition_calls: List[Callable[[Any], Criterion[bool]]]) -> List[Criterion[bool]]:
        conditions: List[Criterion[bool]] = []
        if len(params) < len(condition_calls):
            raise RuntimeError(f"number of arguments of method '{fn_name}' are less than number of conditions")
        for param, condition_call in zip(params, condition_calls):
            conditions.append(condition_call(param))
        return conditions
