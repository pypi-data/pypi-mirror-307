# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/classes/50_DomoDataset_Stream.ipynb.

# %% ../../nbs/classes/50_DomoDataset_Stream.ipynb 3
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Union, Any
from enum import Enum

import httpx
from sqlglot import parse_one, exp


import domolibrary.client.DomoAuth as dmda
import domolibrary.client.DomoError as dmde

import domolibrary.routes.stream as stream_routes

# %% auto 0
__all__ = ['StreamConfig_Mapping_amazon_s3_assumerole', 'StreamConfig_Mapping_snowflake_unload_v2',
           'StreamConfig_Mapping_snowflake_federated', 'StreamConfig_Mapping_snowflake', 'StreamConfig_Mapping_default',
           'StreamConfig_Mapping', 'StreamConfig_Mappings', 'StreamConfig', 'Dataset_Stream_GET_Error', 'DomoStream']

# %% ../../nbs/classes/50_DomoDataset_Stream.ipynb 8
@dataclass
class StreamConfig_Mapping:
    data_provider_type: str
    sql: str = None
    warehouse: str = None
    database_name: str = None
    s3_bucket_category: str = None

    is_default: bool = False

    def search_keys_by_value(
        self, value_to_search: str,
    ) -> Union[StreamConfigMapping, None]:
        
        if self.is_default:
            if value_to_search in ["enteredCustomQuery", "query", "customQuery"]:
                return 'sql'
        
        return next(
            (key for key, value in asdict(self).items() if value == value_to_search),
            None,
        )


StreamConfig_Mapping_amazon_s3_assumerole = StreamConfig_Mapping(
    data_provider_type="amazon_s3_assumerole", s3_bucket_category="filesDiscovery"
)

StreamConfig_Mapping_snowflake_unload_v2 = StreamConfig_Mapping(
    data_provider_type="snowflake_unload_v2",
    sql="query",
    warehouse="warehouseName",
    database_name="databaseName",
)

StreamConfig_Mapping_snowflake_federated = StreamConfig_Mapping(
    data_provider_type="snowflake_federated", sql=None
)

StreamConfig_Mapping_snowflake = StreamConfig_Mapping(
    data_provider_type="snowflake",
    sql="query",
    warehouse="warehouseName",
    database_name="databaseName",
    s3_bucket_category=None,
)

StreamConfig_Mapping_default = StreamConfig_Mapping(
    data_provider_type="default",
    is_default = True
)

class StreamConfig_Mappings(Enum):
    amazon_s3_assumerole = StreamConfig_Mapping_amazon_s3_assumerole
    snowflake_unload_v2 = StreamConfig_Mapping_snowflake_unload_v2
    snowflake_federated = StreamConfig_Mapping_snowflake_federated
    snowflake = StreamConfig_Mapping_snowflake

    default = StreamConfig_Mapping_default

    @classmethod
    def search(cls, value, debug_api : bool = False) -> Union[StreamConfig_Mappings, None] :
        """facilitates return of a deault mapping type"""
        
        try:
            return cls[value]
        
        except KeyError as e:
            if debug_api:
                print(f"{value} has not been added to enum config, must implement {e}")
            return cls.default

# %% ../../nbs/classes/50_DomoDataset_Stream.ipynb 10
@dataclass
class StreamConfig:
    stream_category: str
    name: str
    type: str
    value: str
    value_clean: str = None
    parent: DomoStream = (
        None  ## pass to allow updating parent objecct with extracted values of interest
    )

    def __post_init__(self):

        # self.value_clean = self.value.replace("\n", " ")
        # sc.value_clean = re.sub(" +", " ", sc.value_clean)

        if self.stream_category == "sql":
            self.process_sql()

    def process_sql(self):

        self.parent.configuration_query = self.value

        try:
            for table in parse_one(self.value).find_all(exp.Table):
                self.parent.configuration_tables.append(table.name.lower())
                self.parent.configuration_tables = sorted(
                    list(set(self.parent.configuration_tables))
                )

        except Exception as e:
            # suppress errors when parsing SQL query
            pass

        return self.parent.configuration_query

    @classmethod
    def from_json(
        cls, obj: dict, data_provider_type: str, parent_stream: DomoStream = None
    ):

        config_name = obj["name"]

        mapping_enum = StreamConfig_Mappings.search(
            data_provider_type.lower().replace("-", "_")
        )
        stream_category = "default"

        if mapping_enum:
            stream_category = mapping_enum.value.search_keys_by_value(config_name)

            if parent_stream:
                parent_stream.has_mapping = True

        return cls(
            stream_category=stream_category,
            name=config_name,
            type=obj["type"],
            value=obj["value"],
            parent=parent_stream,
        )

    def to_json(self):
        return {"field": self.stream_category, "key": self.name, "value": self.value}

# %% ../../nbs/classes/50_DomoDataset_Stream.ipynb 13
class Dataset_Stream_GET_Error(dmde.ClassError):
    def __init__(self, cls_instance, message):

        super().__init__(cls_instance=cls_instance, message=message, cls_name_attr="id")


@dataclass
class DomoStream:
    auth: dmda.DomoAuth = field(repr=False)
    id: str
    dataset_id: str

    parent: Any = field(repr=False, default=None)

    transport_description: str = None
    transport_version: int = None
    update_method: str = None
    data_provider_name: str = None
    data_provider_key: str = None
    account_id: str = None
    account_display_name: str = None
    account_userid: str = None

    has_mapping: bool = False
    configuration: List[StreamConfig] = field(default_factory=list)
    configuration_tables: List[str] = field(default_factory=list)
    configuration_query: str = None

    @classmethod
    def _from_parent(cls, parent):
        st = cls(
            auth=parent.auth, 
            id=parent.stream_id, 
            dataset_id=parent.id, 
            parent=parent
        )

        return st

    @classmethod
    def _from_json(cls, auth, obj):

        data_provider = obj.get("dataProvider", {})
        transport = obj.get("transport", {})
        datasource = obj.get("dataSource", {})

        account = obj.get("account", {})

        sd = cls(
            auth=auth,
            id=obj["id"],
            transport_description=transport["description"],
            transport_version=transport["version"],
            update_method=obj.get("updateMethod"),
            data_provider_name=data_provider["name"],
            data_provider_key=data_provider["key"],
            dataset_id=datasource["id"],
        )

        if account:
            sd.account_id = account.get("id")
            sd.account_display_name = account.get("displayName")
            sd.account_userid = account.get("userId")

        sd.configuration = [
            StreamConfig.from_json(
                obj=c_obj, data_provider_type=data_provider.get("key"), parent_stream=sd
            )
            for c_obj in obj["configuration"]
        ]

        return sd

    def generate_config_rpt(self):
        res = {}

        for config in self.configuration:
            if config.stream_category != "default" and config.stream_category:
                obj = config.to_json()
                res.update({obj["field"]: obj["value"]})

        return res

    @classmethod
    async def get_stream_by_id(
        cls,
        auth: dmda.DomoAuth,
        stream_id: str,
        debug_num_stacks_to_drop=2,
        debug_api: bool = False,
        return_raw: bool = False,
        parent : Any = None,
        session: Optional[httpx.AsyncClient] = None,
    ):

        res = await stream_routes.get_stream_by_id(
            auth=auth,
            stream_id=stream_id,
            session=session,
            parent_class=cls.__name__,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            debug_api=debug_api,
        )

        if return_raw:
            return res

        st = cls._from_json(auth=auth, obj=res.response)
        st.parent = parent
        return st

    async def get(self):
        if not (self.parent and self.parent.stream_id):
            raise Dataset_Stream_GET_Error(
                cls_instance=self,
                message=f"dataset {self.parent} has no stream_id",
            )

        self.parent.Stream = await self.get_stream_by_id(
            auth=self.parent.auth, 
            stream_id=self.parent.stream_id,
            parent = self.parent
        )

        return self.parent.Stream

    @classmethod
    async def create_stream(
        cls,
        cnfg_body,
        auth: dmda.DomoAuth = None,
        session: Optional[httpx.AsyncClient] = None,
        debug_api: bool = False,
    ):
        return await stream_routes.create_stream(
            auth=auth, body=cnfg_body, session=session, debug_api=debug_api
        )

    @classmethod
    async def update_stream(
        cls,
        cnfg_body,
        stream_id,
        auth: dmda.DomoAuth = None,
        session: Optional[httpx.AsyncClient] = None,
        debug_api: bool = False,
    ):

        return await stream_routes.update_stream(
            auth=auth,
            stream_id=stream_id,
            body=cnfg_body,
            session=session,
            debug_api=debug_api,
        )
