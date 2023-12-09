from typing import Sequence

from sqlalchemy import select

from db_models.db_models import Permission
from shop_be.services.base import BaseService


class PermissionService(BaseService[Permission]):
    MODEL = Permission

    async def get_or_create(self, names: list[str]) -> Sequence['Permission']:
        names = set(name.lower() for name in names)
        query = select(self.MODEL).where(self.MODEL.name.in_(names))
        exist_permissions = await self.fetch_all(query)
        exist_names = set(perm.name for perm in exist_permissions)
        new_names = names - exist_names

        if not new_names:
            return exist_permissions

        for name in new_names:
            permission = self.MODEL(
                name=name,
                guard_name='api',
                pivot={},
            )
            self.session.add(permission)
            exist_permissions.append(permission)
        await self.session.commit()
        return exist_permissions
