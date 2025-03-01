# -*- coding: utf-8 -*-
# Generated by https://github.com/i2y/connecpy/protoc-gen-connecpy.  DO NOT EDIT!
# source: mtmai/mtmpb/ag.proto

from typing import Any, Protocol, Union

import httpx

from connecpy.async_client import AsyncConnecpyClient
from connecpy.base import Endpoint
from connecpy.server import ConnecpyServer
from connecpy.client import ConnecpyClient
from connecpy.context import ClientContext, ServiceContext

import mtmai.mtmpb.ag_pb2 as _pb2

from google.protobuf import symbol_database

_sym_db = symbol_database.Default()


class AgService(Protocol):
    async def Greet(self, req: _pb2.GreetRequest, ctx: ServiceContext) -> _pb2.GreetResponse: ...
    async def Greet2(self, req: _pb2.GreetRequest, ctx: ServiceContext) -> _pb2.GreetResponse: ...
    async def ComponentList(self, req: _pb2.ComponentListReq, ctx: ServiceContext) -> _pb2.ComponentListRes: ...
    async def GetComponent(self, req: _pb2.GetComponentReq, ctx: ServiceContext) -> _pb2.Component: ...
    async def ListChatMessage(self, req: _pb2.ChatMessageListReq, ctx: ServiceContext) -> _pb2.ChatMessageList: ...


class AgServiceServer(ConnecpyServer):
    def __init__(self, *, service: AgService, server_path_prefix=""):
        super().__init__()
        self._prefix = f"{server_path_prefix}/mtmai.mtmpb.AgService"
        self._endpoints = {
            "Greet": Endpoint[_pb2.GreetRequest, _pb2.GreetResponse](
                service_name="AgService",
                name="Greet",
                function=getattr(service, "Greet"),
                input=_pb2.GreetRequest,
                output=_pb2.GreetResponse,
                allowed_methods=("POST",),
            ),
            "Greet2": Endpoint[_pb2.GreetRequest, _pb2.GreetResponse](
                service_name="AgService",
                name="Greet2",
                function=getattr(service, "Greet2"),
                input=_pb2.GreetRequest,
                output=_pb2.GreetResponse,
                allowed_methods=("POST",),
            ),
            "ComponentList": Endpoint[_pb2.ComponentListReq, _pb2.ComponentListRes](
                service_name="AgService",
                name="ComponentList",
                function=getattr(service, "ComponentList"),
                input=_pb2.ComponentListReq,
                output=_pb2.ComponentListRes,
                allowed_methods=("POST",),
            ),
            "GetComponent": Endpoint[_pb2.GetComponentReq, _pb2.Component](
                service_name="AgService",
                name="GetComponent",
                function=getattr(service, "GetComponent"),
                input=_pb2.GetComponentReq,
                output=_pb2.Component,
                allowed_methods=("POST",),
            ),
            "ListChatMessage": Endpoint[_pb2.ChatMessageListReq, _pb2.ChatMessageList](
                service_name="AgService",
                name="ListChatMessage",
                function=getattr(service, "ListChatMessage"),
                input=_pb2.ChatMessageListReq,
                output=_pb2.ChatMessageList,
                allowed_methods=("POST",),
            ),
        }

    def serviceName(self):
        return "mtmai.mtmpb.AgService"


class AgServiceSync(Protocol):
    def Greet(self, req: _pb2.GreetRequest, ctx: ServiceContext) -> _pb2.GreetResponse: ...
    def Greet2(self, req: _pb2.GreetRequest, ctx: ServiceContext) -> _pb2.GreetResponse: ...
    def ComponentList(self, req: _pb2.ComponentListReq, ctx: ServiceContext) -> _pb2.ComponentListRes: ...
    def GetComponent(self, req: _pb2.GetComponentReq, ctx: ServiceContext) -> _pb2.Component: ...
    def ListChatMessage(self, req: _pb2.ChatMessageListReq, ctx: ServiceContext) -> _pb2.ChatMessageList: ...


class AgServiceServerSync(ConnecpyServer):
    def __init__(self, *, service: AgServiceSync, server_path_prefix=""):
        super().__init__()
        self._prefix = f"{server_path_prefix}/mtmai.mtmpb.AgService"
        self._endpoints = {
            "Greet": Endpoint[_pb2.GreetRequest, _pb2.GreetResponse](
                service_name="AgService",
                name="Greet",
                function=getattr(service, "Greet"),
                input=_pb2.GreetRequest,
                output=_pb2.GreetResponse,
                allowed_methods=("POST",),
            ),
            "Greet2": Endpoint[_pb2.GreetRequest, _pb2.GreetResponse](
                service_name="AgService",
                name="Greet2",
                function=getattr(service, "Greet2"),
                input=_pb2.GreetRequest,
                output=_pb2.GreetResponse,
                allowed_methods=("POST",),
            ),
            "ComponentList": Endpoint[_pb2.ComponentListReq, _pb2.ComponentListRes](
                service_name="AgService",
                name="ComponentList",
                function=getattr(service, "ComponentList"),
                input=_pb2.ComponentListReq,
                output=_pb2.ComponentListRes,
                allowed_methods=("POST",),
            ),
            "GetComponent": Endpoint[_pb2.GetComponentReq, _pb2.Component](
                service_name="AgService",
                name="GetComponent",
                function=getattr(service, "GetComponent"),
                input=_pb2.GetComponentReq,
                output=_pb2.Component,
                allowed_methods=("POST",),
            ),
            "ListChatMessage": Endpoint[_pb2.ChatMessageListReq, _pb2.ChatMessageList](
                service_name="AgService",
                name="ListChatMessage",
                function=getattr(service, "ListChatMessage"),
                input=_pb2.ChatMessageListReq,
                output=_pb2.ChatMessageList,
                allowed_methods=("POST",),
            ),
        }

    def serviceName(self):
        return "mtmai.mtmpb.AgService"


class AgServiceClient(ConnecpyClient):
    def Greet(
        self,
        *,
        request: _pb2.GreetRequest,
        ctx: ClientContext,
        server_path_prefix: str = "",
        **kwargs,
    ) -> _pb2.GreetResponse:
        method = "POST"
        return self._make_request(
            url=f"{server_path_prefix}/mtmai.mtmpb.AgService/Greet",
            ctx=ctx,
            request=request,
            response_obj=_pb2.GreetResponse,
            method=method,
            **kwargs,
        )

    def Greet2(
        self,
        *,
        request: _pb2.GreetRequest,
        ctx: ClientContext,
        server_path_prefix: str = "",
        **kwargs,
    ) -> _pb2.GreetResponse:
        method = "POST"
        return self._make_request(
            url=f"{server_path_prefix}/mtmai.mtmpb.AgService/Greet2",
            ctx=ctx,
            request=request,
            response_obj=_pb2.GreetResponse,
            method=method,
            **kwargs,
        )

    def ComponentList(
        self,
        *,
        request: _pb2.ComponentListReq,
        ctx: ClientContext,
        server_path_prefix: str = "",
        **kwargs,
    ) -> _pb2.ComponentListRes:
        method = "POST"
        return self._make_request(
            url=f"{server_path_prefix}/mtmai.mtmpb.AgService/ComponentList",
            ctx=ctx,
            request=request,
            response_obj=_pb2.ComponentListRes,
            method=method,
            **kwargs,
        )

    def GetComponent(
        self,
        *,
        request: _pb2.GetComponentReq,
        ctx: ClientContext,
        server_path_prefix: str = "",
        **kwargs,
    ) -> _pb2.Component:
        method = "POST"
        return self._make_request(
            url=f"{server_path_prefix}/mtmai.mtmpb.AgService/GetComponent",
            ctx=ctx,
            request=request,
            response_obj=_pb2.Component,
            method=method,
            **kwargs,
        )

    def ListChatMessage(
        self,
        *,
        request: _pb2.ChatMessageListReq,
        ctx: ClientContext,
        server_path_prefix: str = "",
        **kwargs,
    ) -> _pb2.ChatMessageList:
        method = "POST"
        return self._make_request(
            url=f"{server_path_prefix}/mtmai.mtmpb.AgService/ListChatMessage",
            ctx=ctx,
            request=request,
            response_obj=_pb2.ChatMessageList,
            method=method,
            **kwargs,
        )


class AsyncAgServiceClient(AsyncConnecpyClient):
    async def Greet(
        self,
        *,
        request: _pb2.GreetRequest,
        ctx: ClientContext,
        server_path_prefix: str = "",
        session: Union[httpx.AsyncClient, None] = None,
        **kwargs,
    ) -> _pb2.GreetResponse:
        method = "POST"
        return await self._make_request(
            url=f"{server_path_prefix}/mtmai.mtmpb.AgService/Greet",
            ctx=ctx,
            request=request,
            response_obj=_pb2.GreetResponse,
            method=method,
            session=session,
            **kwargs,
        )

    async def Greet2(
        self,
        *,
        request: _pb2.GreetRequest,
        ctx: ClientContext,
        server_path_prefix: str = "",
        session: Union[httpx.AsyncClient, None] = None,
        **kwargs,
    ) -> _pb2.GreetResponse:
        method = "POST"
        return await self._make_request(
            url=f"{server_path_prefix}/mtmai.mtmpb.AgService/Greet2",
            ctx=ctx,
            request=request,
            response_obj=_pb2.GreetResponse,
            method=method,
            session=session,
            **kwargs,
        )

    async def ComponentList(
        self,
        *,
        request: _pb2.ComponentListReq,
        ctx: ClientContext,
        server_path_prefix: str = "",
        session: Union[httpx.AsyncClient, None] = None,
        **kwargs,
    ) -> _pb2.ComponentListRes:
        method = "POST"
        return await self._make_request(
            url=f"{server_path_prefix}/mtmai.mtmpb.AgService/ComponentList",
            ctx=ctx,
            request=request,
            response_obj=_pb2.ComponentListRes,
            method=method,
            session=session,
            **kwargs,
        )

    async def GetComponent(
        self,
        *,
        request: _pb2.GetComponentReq,
        ctx: ClientContext,
        server_path_prefix: str = "",
        session: Union[httpx.AsyncClient, None] = None,
        **kwargs,
    ) -> _pb2.Component:
        method = "POST"
        return await self._make_request(
            url=f"{server_path_prefix}/mtmai.mtmpb.AgService/GetComponent",
            ctx=ctx,
            request=request,
            response_obj=_pb2.Component,
            method=method,
            session=session,
            **kwargs,
        )

    async def ListChatMessage(
        self,
        *,
        request: _pb2.ChatMessageListReq,
        ctx: ClientContext,
        server_path_prefix: str = "",
        session: Union[httpx.AsyncClient, None] = None,
        **kwargs,
    ) -> _pb2.ChatMessageList:
        method = "POST"
        return await self._make_request(
            url=f"{server_path_prefix}/mtmai.mtmpb.AgService/ListChatMessage",
            ctx=ctx,
            request=request,
            response_obj=_pb2.ChatMessageList,
            method=method,
            session=session,
            **kwargs,
        )
