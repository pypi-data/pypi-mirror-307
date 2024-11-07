# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/classes/50_DomoAccessToken.ipynb.

# %% auto 0
__all__ = ['DomoAccessToken', 'get_access_tokens']

# %% ../../nbs/classes/50_DomoAccessToken.ipynb 3
import httpx
import datetime as dt
from nbdev.showdoc import patch_to
import asyncio

from dataclasses import dataclass, field

import domolibrary.client.DomoAuth as dmda
import domolibrary.utils.chunk_execution as ce

import domolibrary.routes.access_token as access_token_routes

# %% ../../nbs/classes/50_DomoAccessToken.ipynb 7
@dataclass
class DomoAccessToken:
    id: int
    name: str
    owner: None
    expiration_date: dt.datetime
    token: str = field(repr=False)

    auth: dmda.DomoAuth = field(repr=False)

    def __eq__(self, other):
        if not isinstance(other, DomoAccessToken):
            return False

        return self.id == other.id

    @classmethod
    async def _from_json(cls, obj, auth):
        import domolibrary.classes.DomoUser as dmu

        owner = await dmu.DomoUser.get_by_id(user_id=obj["ownerId"], auth=auth)

        return cls(
            id=obj["id"],
            name=obj["name"],
            owner=owner,
            expiration_date=obj["expires"],
            auth=auth,
            token=obj.get("token"),
        )

# %% ../../nbs/classes/50_DomoAccessToken.ipynb 8
async def get_access_tokens(
    auth: dmda.DomoAuth = None,
    return_raw: bool = False,
    debug_api: bool = False,
    debug_num_stacks_to_drop=2,
    session: httpx.AsyncClient = None,
    parent_class=None,
):
    res = await access_token_routes.get_access_tokens(
        auth=auth,
        session=session,
        debug_api=debug_api,
        parent_class=parent_class,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    return await ce.gather_with_concurrency(
        *[DomoAccessToken._from_json(obj=obj, auth=auth) for obj in res.response], n=10
    )

# %% ../../nbs/classes/50_DomoAccessToken.ipynb 10
@patch_to(DomoAccessToken, cls_method=True)
async def generate(
    cls: DomoAccessToken,
    duration_in_days: int,
    token_name: str,
    auth: dmda.DomoAuth,
    owner,  # DomoUser
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop: int = 2,
    return_raw: bool = False,
    parent_class: str = None,
):

    res = await access_token_routes.generate_access_token(
        user_id=owner.id,
        token_name=token_name,
        duration_in_days=duration_in_days,
        auth=auth,
        debug_api=debug_api,
        session=session,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class or cls.__name__,
    )

    if return_raw:
        return res

    return await cls._from_json(obj=res.response, auth=auth)

# %% ../../nbs/classes/50_DomoAccessToken.ipynb 11
@patch_to(DomoAccessToken)
async def revoke(
    self,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop: int = 2,
):
    return await access_token_routes.revoke_access_token(
        auth=self.auth,
        access_token_id=self.id,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=self.__class__.__name__,
        session=session,
    )

# %% ../../nbs/classes/50_DomoAccessToken.ipynb 13
@patch_to(DomoAccessToken)
async def regenerate(
    self,
    session: httpx.AsyncClient = None,
    duration_in_days: int = 90,
    debug_api: bool = False,
    return_raw: bool = False,
    debug_num_stacks_to_drop: int = 2,
):

    await self.revoke()

    await asyncio.sleep(3)

    cls = await self.generate(
        duration_in_days=duration_in_days,
        token_name=self.name,
        auth=self.auth,
        owner=self.owner,
        debug_api=debug_api,
        session=session,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        return_raw=return_raw,
        parent_class=self.__class__.__name__,
    )

    self.token = cls.token
    self.expiration_date = cls.expiration_date

    return self
