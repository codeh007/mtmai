# -*- coding: utf-8 -*-
# Generated by https://github.com/i2y/connecpy/protoc-gen-connecpy.  DO NOT EDIT!
# source: mtmai/mtmpb/user.proto

from typing import Any, Protocol, Union

import httpx

from connecpy.async_client import AsyncConnecpyClient
from connecpy.base import Endpoint
from connecpy.server import ConnecpyServer
from connecpy.client import ConnecpyClient
from connecpy.context import ClientContext, ServiceContext

import mtmai.mtmpb.user_pb2 as _pb2

from google.protobuf import symbol_database

_sym_db = symbol_database.Default()


class UserService(Protocol):
    async def ListMembers(self, req: _pb2.ListMemberReq, ctx: ServiceContext) -> _pb2.MemberList: ...


class UserServiceServer(ConnecpyServer):
    def __init__(self, *, service: UserService, server_path_prefix=""):
        super().__init__()
        self._prefix = f"{server_path_prefix}/mtmai.mtmpb.UserService"
        self._endpoints = {
            "ListMembers": Endpoint[_pb2.ListMemberReq, _pb2.MemberList](
                service_name="UserService",
                name="ListMembers",
                function=getattr(service, "ListMembers"),
                input=_pb2.ListMemberReq,
                output=_pb2.MemberList,
                allowed_methods=("POST",),
            ),
        }

    def serviceName(self):
        return "mtmai.mtmpb.UserService"


class UserServiceSync(Protocol):
    def ListMembers(self, req: _pb2.ListMemberReq, ctx: ServiceContext) -> _pb2.MemberList: ...


class UserServiceServerSync(ConnecpyServer):
    def __init__(self, *, service: UserServiceSync, server_path_prefix=""):
        super().__init__()
        self._prefix = f"{server_path_prefix}/mtmai.mtmpb.UserService"
        self._endpoints = {
            "ListMembers": Endpoint[_pb2.ListMemberReq, _pb2.MemberList](
                service_name="UserService",
                name="ListMembers",
                function=getattr(service, "ListMembers"),
                input=_pb2.ListMemberReq,
                output=_pb2.MemberList,
                allowed_methods=("POST",),
            ),
        }

    def serviceName(self):
        return "mtmai.mtmpb.UserService"


class UserServiceClient(ConnecpyClient):
    def ListMembers(
        self,
        *,
        request: _pb2.ListMemberReq,
        ctx: ClientContext,
        server_path_prefix: str = "",
        **kwargs,
    ) -> _pb2.MemberList:
        method = "POST"
        return self._make_request(
            url=f"{server_path_prefix}/mtmai.mtmpb.UserService/ListMembers",
            ctx=ctx,
            request=request,
            response_obj=_pb2.MemberList,
            method=method,
            **kwargs,
        )


class AsyncUserServiceClient(AsyncConnecpyClient):
    async def ListMembers(
        self,
        *,
        request: _pb2.ListMemberReq,
        ctx: ClientContext,
        server_path_prefix: str = "",
        session: Union[httpx.AsyncClient, None] = None,
        **kwargs,
    ) -> _pb2.MemberList:
        method = "POST"
        return await self._make_request(
            url=f"{server_path_prefix}/mtmai.mtmpb.UserService/ListMembers",
            ctx=ctx,
            request=request,
            response_obj=_pb2.MemberList,
            method=method,
            session=session,
            **kwargs,
        )
