# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from mtmai.mtmpb import events_pb2 as mtmai_dot_mtmpb_dot_events__pb2


class EventsServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Push = channel.unary_unary(
                '/mtmai.mtmpb.EventsService/Push',
                request_serializer=mtmai_dot_mtmpb_dot_events__pb2.PushEventRequest.SerializeToString,
                response_deserializer=mtmai_dot_mtmpb_dot_events__pb2.Event.FromString,
                _registered_method=True)
        self.BulkPush = channel.unary_unary(
                '/mtmai.mtmpb.EventsService/BulkPush',
                request_serializer=mtmai_dot_mtmpb_dot_events__pb2.BulkPushEventRequest.SerializeToString,
                response_deserializer=mtmai_dot_mtmpb_dot_events__pb2.Events.FromString,
                _registered_method=True)
        self.ReplaySingleEvent = channel.unary_unary(
                '/mtmai.mtmpb.EventsService/ReplaySingleEvent',
                request_serializer=mtmai_dot_mtmpb_dot_events__pb2.ReplayEventRequest.SerializeToString,
                response_deserializer=mtmai_dot_mtmpb_dot_events__pb2.Event.FromString,
                _registered_method=True)
        self.PutLog = channel.unary_unary(
                '/mtmai.mtmpb.EventsService/PutLog',
                request_serializer=mtmai_dot_mtmpb_dot_events__pb2.PutLogRequest.SerializeToString,
                response_deserializer=mtmai_dot_mtmpb_dot_events__pb2.PutLogResponse.FromString,
                _registered_method=True)
        self.PutStreamEvent = channel.unary_unary(
                '/mtmai.mtmpb.EventsService/PutStreamEvent',
                request_serializer=mtmai_dot_mtmpb_dot_events__pb2.PutStreamEventRequest.SerializeToString,
                response_deserializer=mtmai_dot_mtmpb_dot_events__pb2.PutStreamEventResponse.FromString,
                _registered_method=True)


class EventsServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Push(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BulkPush(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReplaySingleEvent(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PutLog(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PutStreamEvent(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_EventsServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Push': grpc.unary_unary_rpc_method_handler(
                    servicer.Push,
                    request_deserializer=mtmai_dot_mtmpb_dot_events__pb2.PushEventRequest.FromString,
                    response_serializer=mtmai_dot_mtmpb_dot_events__pb2.Event.SerializeToString,
            ),
            'BulkPush': grpc.unary_unary_rpc_method_handler(
                    servicer.BulkPush,
                    request_deserializer=mtmai_dot_mtmpb_dot_events__pb2.BulkPushEventRequest.FromString,
                    response_serializer=mtmai_dot_mtmpb_dot_events__pb2.Events.SerializeToString,
            ),
            'ReplaySingleEvent': grpc.unary_unary_rpc_method_handler(
                    servicer.ReplaySingleEvent,
                    request_deserializer=mtmai_dot_mtmpb_dot_events__pb2.ReplayEventRequest.FromString,
                    response_serializer=mtmai_dot_mtmpb_dot_events__pb2.Event.SerializeToString,
            ),
            'PutLog': grpc.unary_unary_rpc_method_handler(
                    servicer.PutLog,
                    request_deserializer=mtmai_dot_mtmpb_dot_events__pb2.PutLogRequest.FromString,
                    response_serializer=mtmai_dot_mtmpb_dot_events__pb2.PutLogResponse.SerializeToString,
            ),
            'PutStreamEvent': grpc.unary_unary_rpc_method_handler(
                    servicer.PutStreamEvent,
                    request_deserializer=mtmai_dot_mtmpb_dot_events__pb2.PutStreamEventRequest.FromString,
                    response_serializer=mtmai_dot_mtmpb_dot_events__pb2.PutStreamEventResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mtmai.mtmpb.EventsService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('mtmai.mtmpb.EventsService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class EventsService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Push(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/mtmai.mtmpb.EventsService/Push',
            mtmai_dot_mtmpb_dot_events__pb2.PushEventRequest.SerializeToString,
            mtmai_dot_mtmpb_dot_events__pb2.Event.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def BulkPush(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/mtmai.mtmpb.EventsService/BulkPush',
            mtmai_dot_mtmpb_dot_events__pb2.BulkPushEventRequest.SerializeToString,
            mtmai_dot_mtmpb_dot_events__pb2.Events.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ReplaySingleEvent(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/mtmai.mtmpb.EventsService/ReplaySingleEvent',
            mtmai_dot_mtmpb_dot_events__pb2.ReplayEventRequest.SerializeToString,
            mtmai_dot_mtmpb_dot_events__pb2.Event.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def PutLog(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/mtmai.mtmpb.EventsService/PutLog',
            mtmai_dot_mtmpb_dot_events__pb2.PutLogRequest.SerializeToString,
            mtmai_dot_mtmpb_dot_events__pb2.PutLogResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def PutStreamEvent(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/mtmai.mtmpb.EventsService/PutStreamEvent',
            mtmai_dot_mtmpb_dot_events__pb2.PutStreamEventRequest.SerializeToString,
            mtmai_dot_mtmpb_dot_events__pb2.PutStreamEventResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
