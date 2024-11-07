# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/routes/instance_config.ipynb.

# %% auto 0
__all__ = ['ToggleSocialUsers_Error', 'get_is_invite_social_users_enabled', 'ToggleUserInvite_Error',
           'toggle_is_user_invite_enabled', 'get_is_user_invite_notifications_enabled', 'get_allowlist',
           'Allowlist_UnableToUpdate', 'set_allowlist', 'set_authorized_domains', 'GetDomains_NotFound',
           'get_authorized_domains', 'InstanceConfig_Error', 'get_is_weekly_digest_enabled',
           'toggle_is_weekly_digest_enabled', 'GetAppDomains_NotFound', 'get_authorized_custom_app_domains',
           'set_authorized_custom_app_domains']

# %% ../../nbs/routes/instance_config.ipynb 2
import httpx

from typing import List

import domolibrary.client.get_data as gd
import domolibrary.client.ResponseGetData as rgd
import domolibrary.client.DomoAuth as dmda
import domolibrary.client.DomoError as de

from domolibrary.utils.convert import convert_string_to_bool

import domolibrary.routes.user as user_routes

# %% ../../nbs/routes/instance_config.ipynb 5
class ToggleSocialUsers_Error(de.DomoError):
    def __init__(self, status, domo_instance, message="failure to toggle social users"):
        super().__init__(status=status, domo_instance=domo_instance, message=message)


@gd.route_function
async def get_is_invite_social_users_enabled(
    auth: dmda.DomoAuth,
    customer_id: str,
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    parent_class=None,
    return_raw: bool = False,
    debug_num_stacks_to_drop=1,
) -> rgd.ResponseGetData:

    # must pass the customer as the short form API endpoint (without customer_id) does not support a GET request
    # url = f"https://{auth.domo_instance}.domo.com/api/content/v3/customers/features/free-invite"

    url = f"https://{auth.domo_instance}.domo.com/api/content/v3/customers/{customer_id}/features/free-invite"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        session=session,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise ToggleSocialUsers_Error(
            status=res.status, message=res.response, domo_instance=auth.domo_instance
        )

    if return_raw:
        return res

    res.response = {"name": "free-invite", "is_enabled": res.response["enabled"]}

    return res

# %% ../../nbs/routes/instance_config.ipynb 7
class ToggleUserInvite_Error(de.DomoError):
    def __init__(
        self, status, domo_instance, message="failure to toggle user invite enabled"
    ):
        super().__init__(status=status, domo_instance=domo_instance, message=message)


@gd.route_function
async def toggle_is_user_invite_enabled(
    auth: dmda.DomoFullAuth,
    is_enabled: bool,
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    return_raw: bool = False,
    parent_class=None,
    debug_num_stacks_to_drop=1,
) -> rgd.ResponseGetData:
    """
    Admin > Company Settings > Notifications
    """

    url = f"https://{auth.domo_instance}.domo.com/api/customer/v1/properties/user.invite.email.enabled"

    body = {"value": is_enabled}

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=body,
        session=session,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise ToggleUserInvite_Error(
            status=res.status, message=res.response, domo_instance=auth.domo_instance
        )

    if return_raw:
        return res

    res.response = {"feature": "user.invite.email.enabled", "is_enabled": is_enabled}

    return res

# %% ../../nbs/routes/instance_config.ipynb 9
@gd.route_function
async def get_is_user_invite_notifications_enabled(
    auth: dmda.DomoFullAuth,
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    parent_class=None,
    debug_num_stacks_to_drop=1,
    return_raw: bool = False,
) -> rgd.ResponseGetData:


    url = f"https://{auth.domo_instance}.domo.com/api/customer/v1/properties/user.invite.email.enabled"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        session=session,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise ToggleSocialUsers_Error(
            status=res.status, message=res.response, domo_instance=auth.domo_instance
        )

    if return_raw:
        return res

    res.response = {
        "name": "user.invite.email.enabled",
        "is_enabled": convert_string_to_bool(res.response["value"]),
    }

    return res

# %% ../../nbs/routes/instance_config.ipynb 11
@gd.route_function
async def get_allowlist(
    auth: dmda.DomoAuth,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
    debug_api: bool = False,
    parent_class=None,
    debug_num_stacks_to_drop=1,
) -> rgd.ResponseGetData:


    url = f"https://{auth.domo_instance}.domo.com/admin/companysettings/whitelist"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        headers={"accept": "*/*"},
        session=session,
        debug_api=debug_api,
        is_follow_redirects=True,
        return_raw=return_raw,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    return res

# %% ../../nbs/routes/instance_config.ipynb 14
class Allowlist_UnableToUpdate(de.DomoError):
    def __init__(
        self,
        status: int,
        reason: str,
        domo_instance: str,
        function_name: str = "update_allowlist",
    ):
        super().__init__(
            function_name=function_name,
            status=status,
            message=f"unable to update allowlist: {reason}",
            domo_instance=domo_instance,
        )

# %% ../../nbs/routes/instance_config.ipynb 15
@gd.route_function
async def set_allowlist(
    auth: dmda.DomoAuth,
    ip_address_ls: list[str],
    debug_api: bool = False,
    return_raw: bool = False,
    session: httpx.AsyncClient = None,
    parent_class=None,
    debug_num_stacks_to_drop=1,
) -> rgd.ResponseGetData:
    """companysettings/whitelist API only allows users to SET the allowlist does not allow INSERT or UPDATE"""

    url = f"https://{auth.domo_instance}.domo.com/admin/companysettings/whitelist"

    body = {"addresses": ip_address_ls}

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=body,
        debug_api=debug_api,
        is_follow_redirects=True,
        return_raw=return_raw,
        session=session,
        headers={"accept": "text/plain"},
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )
    if not res.is_success:
        raise Allowlist_UnableToUpdate(
            status=res.status, reason=res.response, domo_instance=auth.domo_instance
        )

    if res.is_success:
        res.response = f"allow list updated from {res.response}"

    return res

# %% ../../nbs/routes/instance_config.ipynb 17
@gd.route_function
async def set_authorized_domains(
    auth: dmda.DomoAuth,
    authorized_domain_ls: List[str],
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    parent_class=None,
    debug_num_stacks_to_drop=1,
):

    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/customer-states/authorized-domains"

    body = {"name": "authorized-domains", "value": ",".join(authorized_domain_ls)}

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=body,
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    return res

# %% ../../nbs/routes/instance_config.ipynb 18
class GetDomains_NotFound(de.DomoError):
    def __init__(self, status, message, domo_instance):
        super().__init__(status=status, message=message, domo_instance=domo_instance)


@gd.route_function
async def get_authorized_domains(
    auth: dmda.DomoAuth,
    return_raw: bool = False,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    parent_class=None,
    debug_num_stacks_to_drop=1,
):


    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/customer-states/authorized-domains"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    # domo raises a 404 error even if the success is valid but there are no approved domains
    if res.status == 404 and res.response == "Not Found":
        res_test = await user_routes.get_all_users(auth=auth)

        if not res_test.is_success:
            raise GetDomains_NotFound(
                domo_instance=auth.domo_instance,
                status=res.status,
                message=res.response,
            )

        if res_test.is_success:
            res.status = 200
            res.is_success = True
            res.response = []

        return res

    res.response = [domain.strip() for domain in res.response.get("value").split(",")]
    return res

# %% ../../nbs/routes/instance_config.ipynb 20
class InstanceConfig_Error(de.DomoError):
    def __init__(self, status, message, domo_instance):
        super().__init__(status=status, message=message, domo_instance=domo_instance)


@gd.route_function
async def get_is_weekly_digest_enabled(
    auth: dmda.DomoAuth,
    return_raw: bool = False,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    parent_class=None,
    debug_num_stacks_to_drop=1,
):
    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/customer-states/come-back-to-domo-all-users"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    if res.status == 404 and res.response == "Not Found":
        raise InstanceConfig_Error(
            domo_instance=auth.domo_instance,
            status=res.status,
            message=res.response,
        )

    res.response = {
        "is_enabled": convert_string_to_bool(res.response["value"]),
        "feature": "come-back-to-domo-all-users",
    }

    return res

# %% ../../nbs/routes/instance_config.ipynb 22
@gd.route_function
async def toggle_is_weekly_digest_enabled(
    auth: dmda.DomoAuth,
    return_raw: bool = False,
    debug_api: bool = False,
    is_enabled: bool = True,
    session: httpx.AsyncClient = None,
    parent_class=None,
    debug_num_stacks_to_drop=1,
):
    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/customer-states/come-back-to-domo-all-users"

    body = {"name": "come-back-to-domo-all-users", "value": is_enabled}
    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=body,
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    if not res.is_success:
        return res

    return await get_is_weekly_digest_enabled(auth=auth)

# %% ../../nbs/routes/instance_config.ipynb 24
class GetAppDomains_NotFound(de.DomoError):
    def __init__(self, status, message, domo_instance):
        super().__init__(status=status, message=message, domo_instance=domo_instance)


@gd.route_function
async def get_authorized_custom_app_domains(
    auth: dmda.DomoAuth,
    return_raw: bool = False,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    parent_class=None,
    debug_num_stacks_to_drop=1,
):
    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/customer-states/authorized-app-domains"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    # domo raises a 404 error even if the success is valid but there are no approved domains
    if res.status == 404 and res.response == "Not Found":
        res_test = await user_routes.get_all_users(auth=auth)

        if not res_test.is_success:
            raise GetAppDomains_NotFound(
                domo_instance=auth.domo_instance,
                status=res.status,
                message=res.response,
            )

        if res_test.is_success:
            res.status = 200
            res.is_success = True
            res.response = []

        return res

    res.response = [domain.strip() for domain in res.response.get("value").split(",")]
    return res

# %% ../../nbs/routes/instance_config.ipynb 26
@gd.route_function
async def set_authorized_custom_app_domains(
    auth: dmda.DomoAuth,
    authorized_custom_app_domain_ls: List[str],
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    parent_class=None,
    debug_num_stacks_to_drop=1,
):
    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/customer-states/authorized-app-domains"

    body = {
        "name": "authorized-app-domains",
        "value": ",".join(authorized_custom_app_domain_ls),
    }

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=body,
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    return res
