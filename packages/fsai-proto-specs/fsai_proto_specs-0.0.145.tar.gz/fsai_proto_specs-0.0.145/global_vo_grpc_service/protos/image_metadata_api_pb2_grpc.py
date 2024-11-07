# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from global_vo_grpc_service.protos import image_metadata_api_pb2 as global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class ImageMetadataApiStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListAllImageMetadataConfigs = channel.unary_unary(
                '/ImageMetadataApi/ListAllImageMetadataConfigs',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.ListAllImageMetadataConfigsResponse.FromString,
                )
        self.GetImageMetadataByImageId = channel.unary_unary(
                '/ImageMetadataApi/GetImageMetadataByImageId',
                request_serializer=global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.GetImageMetadataByImageIdRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.GetImageMetadataByImageIdResponse.FromString,
                )
        self.CreateImageMetadata = channel.unary_unary(
                '/ImageMetadataApi/CreateImageMetadata',
                request_serializer=global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.CreateImageMetadataRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.CreateImageMetadataResponse.FromString,
                )
        self.UpdateImageMetadata = channel.unary_unary(
                '/ImageMetadataApi/UpdateImageMetadata',
                request_serializer=global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.UpdateImageMetadataRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.UpdateImageMetadataResponse.FromString,
                )
        self.DeleteImageMetadata = channel.unary_unary(
                '/ImageMetadataApi/DeleteImageMetadata',
                request_serializer=global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.DeleteImageMetadataRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.DeleteImageMetadataResponse.FromString,
                )


class ImageMetadataApiServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ListAllImageMetadataConfigs(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetImageMetadataByImageId(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateImageMetadata(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateImageMetadata(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteImageMetadata(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ImageMetadataApiServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ListAllImageMetadataConfigs': grpc.unary_unary_rpc_method_handler(
                    servicer.ListAllImageMetadataConfigs,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.ListAllImageMetadataConfigsResponse.SerializeToString,
            ),
            'GetImageMetadataByImageId': grpc.unary_unary_rpc_method_handler(
                    servicer.GetImageMetadataByImageId,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.GetImageMetadataByImageIdRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.GetImageMetadataByImageIdResponse.SerializeToString,
            ),
            'CreateImageMetadata': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateImageMetadata,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.CreateImageMetadataRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.CreateImageMetadataResponse.SerializeToString,
            ),
            'UpdateImageMetadata': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateImageMetadata,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.UpdateImageMetadataRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.UpdateImageMetadataResponse.SerializeToString,
            ),
            'DeleteImageMetadata': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteImageMetadata,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.DeleteImageMetadataRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.DeleteImageMetadataResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ImageMetadataApi', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ImageMetadataApi(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ListAllImageMetadataConfigs(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ImageMetadataApi/ListAllImageMetadataConfigs',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.ListAllImageMetadataConfigsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetImageMetadataByImageId(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ImageMetadataApi/GetImageMetadataByImageId',
            global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.GetImageMetadataByImageIdRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.GetImageMetadataByImageIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateImageMetadata(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ImageMetadataApi/CreateImageMetadata',
            global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.CreateImageMetadataRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.CreateImageMetadataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateImageMetadata(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ImageMetadataApi/UpdateImageMetadata',
            global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.UpdateImageMetadataRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.UpdateImageMetadataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteImageMetadata(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ImageMetadataApi/DeleteImageMetadata',
            global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.DeleteImageMetadataRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_image__metadata__api__pb2.DeleteImageMetadataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
