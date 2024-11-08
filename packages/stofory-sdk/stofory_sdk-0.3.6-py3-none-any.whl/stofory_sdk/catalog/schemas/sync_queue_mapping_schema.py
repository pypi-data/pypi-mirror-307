from datetime import datetime
from typing import Annotated

from litestar.params import Parameter
from msgspec import Struct, Meta

from stofory_sdk.catalog.models.enums import SyncTaskType, SyncTaskPriority


class SyncTaskCreateRequest(Struct, forbid_unknown_fields=True):
    priority: Annotated[SyncTaskPriority, Parameter(title="Priority", description="The priority of the sync task.")]
    consumer_prefix: Annotated[str, Parameter(title="Consumer Prefix", description="The prefix of the consumer."), Meta(min_length=1)]
    table_name: Annotated[str, Parameter(title="Table Name", description="The name of the table."), Meta(min_length=1)]
    operation: Annotated[SyncTaskType, Parameter(title="Operation", description="The operation of the sync task.")]


class SyncTaskUpdateRequest(Struct, forbid_unknown_fields=True):
    priority: Annotated[SyncTaskPriority, Parameter(title="Priority", description="The priority of the sync task.")]
    consumer_prefix: Annotated[str, Parameter(title="Consumer Prefix", description="The prefix of the consumer."), Meta(min_length=1)]
    table_name: Annotated[str, Parameter(title="Table Name", description="The name of the table."), Meta(min_length=1)]
    operation: Annotated[SyncTaskType, Parameter(title="Operation", description="The operation of the sync task.")]


class SyncTaskResponse(Struct):
    priority: SyncTaskPriority
    consumer_prefix: str
    table_name: str
    operation: SyncTaskType

    created_at: datetime
    updated_at: datetime
