# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: onos/provisioner/aspects.proto, onos/provisioner/config.proto
# plugin: python-betterproto
from dataclasses import dataclass
from datetime import datetime
from typing import AsyncIterator, Dict, List, Optional

import betterproto
import grpclib


@dataclass(eq=False, repr=False)
class DeviceConfig(betterproto.Message):
    """
    DeviceConfig is a topology entity aspect used to specify what pipeline and
    chassis config a device should have applied to it
    """

    pipeline_config_id: str = betterproto.string_field(1)
    chassis_config_id: str = betterproto.string_field(2)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class PipelineConfigState(betterproto.Message):
    """
    PipelineConfigState is a topology entity aspect used to indicate what
    pipeline config a device has presently applied to it
    """

    config_id: str = betterproto.string_field(1)
    cookie: int = betterproto.uint64_field(2)
    updated: datetime = betterproto.message_field(3)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class ChassisConfigState(betterproto.Message):
    """
    ChassisConfigState is a topology entity aspect used to indicate what
    chassis config a device has presently applied to it
    """

    config_id: str = betterproto.string_field(1)
    updated: datetime = betterproto.message_field(2)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class ConfigRecord(betterproto.Message):
    """
    DeviceConfig is a topology entity aspect used to specify what pipeline and
    chassis config a device should have applied to it
    """

    config_id: str = betterproto.string_field(1)
    kind: str = betterproto.string_field(3)
    artifacts: List[str] = betterproto.string_field(4)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class Config(betterproto.Message):
    """
    PipelineConfigState is a topology entity aspect used to indicate what
    pipeline config a device has presently applied to it
    """

    record: "ConfigRecord" = betterproto.message_field(1)
    artifacts: Dict[str, bytes] = betterproto.map_field(
        4, betterproto.TYPE_STRING, betterproto.TYPE_BYTES
    )

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class AddConfigRequest(betterproto.Message):
    """
    ChassisConfigState is a topology entity aspect used to indicate what
    chassis config a device has presently applied to it
    """

    config: "Config" = betterproto.message_field(1)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class AddConfigResponse(betterproto.Message):
    pass

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class DeleteConfigRequest(betterproto.Message):
    config_id: str = betterproto.string_field(1)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class DeleteConfigResponse(betterproto.Message):
    pass

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class GetConfigRequest(betterproto.Message):
    config_id: str = betterproto.string_field(1)
    include_artifacts: bool = betterproto.bool_field(2)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class GetConfigResponse(betterproto.Message):
    config: "Config" = betterproto.message_field(1)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class ListConfigsRequest(betterproto.Message):
    kind: str = betterproto.string_field(1)
    include_artifacts: bool = betterproto.bool_field(2)
    watch: bool = betterproto.bool_field(3)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class ListConfigsResponse(betterproto.Message):
    config: "Config" = betterproto.message_field(1)

    def __post_init__(self) -> None:
        super().__post_init__()


class ProvisionerServiceStub(betterproto.ServiceStub):
    async def add(self, *, config: "Config" = None) -> "AddConfigResponse":

        request = AddConfigRequest()
        if config is not None:
            request.config = config

        return await self._unary_unary(
            "/onos.provisioner.ProvisionerService/Add", request, AddConfigResponse
        )

    async def delete(self, *, config_id: str = "") -> "DeleteConfigResponse":

        request = DeleteConfigRequest()
        request.config_id = config_id

        return await self._unary_unary(
            "/onos.provisioner.ProvisionerService/Delete", request, DeleteConfigResponse
        )

    async def get(
        self, *, config_id: str = "", include_artifacts: bool = False
    ) -> "GetConfigResponse":

        request = GetConfigRequest()
        request.config_id = config_id
        request.include_artifacts = include_artifacts

        return await self._unary_unary(
            "/onos.provisioner.ProvisionerService/Get", request, GetConfigResponse
        )

    async def list(
        self, *, kind: str = "", include_artifacts: bool = False, watch: bool = False
    ) -> AsyncIterator["ListConfigsResponse"]:

        request = ListConfigsRequest()
        request.kind = kind
        request.include_artifacts = include_artifacts
        request.watch = watch

        async for response in self._unary_stream(
            "/onos.provisioner.ProvisionerService/List",
            request,
            ListConfigsResponse,
        ):
            yield response
