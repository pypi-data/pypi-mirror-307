# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from global_vo_grpc_service.protos import image_api_pb2 as global__vo__grpc__service_dot_protos_dot_image__api__pb2


class ImageApiStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.FindOrCreateImage = channel.unary_unary(
                '/ImageApi/FindOrCreateImage',
                request_serializer=global__vo__grpc__service_dot_protos_dot_image__api__pb2.FindOrCreateImageRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_image__api__pb2.FindOrCreateImageResponse.FromString,
                )
        self.GetImageById = channel.unary_unary(
                '/ImageApi/GetImageById',
                request_serializer=global__vo__grpc__service_dot_protos_dot_image__api__pb2.GetImageByIdRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_image__api__pb2.GetImageByIdResponse.FromString,
                )


class ImageApiServicer(object):
    """Missing associated documentation comment in .proto file."""

    def FindOrCreateImage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetImageById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ImageApiServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'FindOrCreateImage': grpc.unary_unary_rpc_method_handler(
                    servicer.FindOrCreateImage,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_image__api__pb2.FindOrCreateImageRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_image__api__pb2.FindOrCreateImageResponse.SerializeToString,
            ),
            'GetImageById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetImageById,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_image__api__pb2.GetImageByIdRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_image__api__pb2.GetImageByIdResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ImageApi', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ImageApi(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def FindOrCreateImage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ImageApi/FindOrCreateImage',
            global__vo__grpc__service_dot_protos_dot_image__api__pb2.FindOrCreateImageRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_image__api__pb2.FindOrCreateImageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetImageById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ImageApi/GetImageById',
            global__vo__grpc__service_dot_protos_dot_image__api__pb2.GetImageByIdRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_image__api__pb2.GetImageByIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
