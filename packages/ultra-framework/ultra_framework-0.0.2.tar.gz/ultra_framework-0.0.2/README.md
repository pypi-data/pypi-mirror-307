# UltraFramework

## Description
Framework for FastAPI inspired by Java Spring.

* It exposes a base entity class SQLEntity that can be derived in order to define custom entities.
* It exposes a base repository class CRUDRepository[M]  that can be derived in order to define custom repositories. The following public methods are available:
  * save(): None
  * find_all(): None
  * delete(): None

Example:

```python
from sqlalchemy.orm import mapped_column, Mapped
from ultra_framework.entities.sql_entity import SQLEntity
from ultra_framework.repositories.crud_repository import CRUDRepository


class UserEntity(SQLEntity):
  __tablename__ = "users"
  __table_args__ = {"schema": "myschema"}

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str]


class UserRepository(CRUDRepository[UserEntity]):
  entity_class = UserEntity

  @CRUDRepository.auto_implement_one([lambda idx: UserEntity.id == idx])
  def find_by_id(self, idx: int) -> UserEntity: ...
```
