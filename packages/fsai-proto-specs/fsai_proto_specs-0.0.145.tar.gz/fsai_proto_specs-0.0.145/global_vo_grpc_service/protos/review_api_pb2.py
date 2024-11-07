# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: global_vo_grpc_service/protos/review_api.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from global_vo_grpc_service.protos import utils_pb2 as global__vo__grpc__service_dot_protos_dot_utils__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.global_vo_grpc_service/protos/review_api.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a)global_vo_grpc_service/protos/utils.proto\"\x97\x02\n\x06Review\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x12\n\nmission_id\x18\x02 \x01(\x05\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x12\x12\n\ncreated_by\x18\x05 \x01(\x05\x12\x12\n\nupdated_by\x18\x06 \x01(\x05\x12\x12\n\ndeleted_by\x18\x07 \x01(\x05\x12.\n\ncreated_at\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nupdated_at\x18\t \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\ndeleted_at\x18\n \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"J\n\x19\x43\x61\x63heLastUserQueryRequest\x12\x19\n\x11\x65s_query_json_str\x18\x01 \x01(\t\x12\x12\n\nmission_id\x18\x02 \x01(\x05\">\n\x1a\x43\x61\x63heLastUserQueryResponse\x12 \n\x0b\x63hange_type\x18\x01 \x01(\x0e\x32\x0b.ChangeType\"\'\n\x0bHeightRange\x12\x0b\n\x03min\x18\x01 \x01(\x02\x12\x0b\n\x03max\x18\x02 \x01(\x02\"&\n\nScoreRange\x12\x0b\n\x03min\x18\x01 \x01(\x02\x12\x0b\n\x03max\x18\x02 \x01(\x02\"\xaa\x01\n\x0c\x46ilterValues\x12\x14\n\x0c\x63\x61tegory_ids\x18\x01 \x03(\x05\x12\"\n\x0cheight_range\x18\x02 \x01(\x0b\x32\x0c.HeightRange\x12\x0e\n\x06states\x18\x03 \x03(\t\x12 \n\x0bscore_range\x18\x04 \x01(\x0b\x32\x0b.ScoreRange\x12\x16\n\x0e\x63reated_by_ids\x18\x05 \x03(\x05\x12\x16\n\x0eupdated_by_ids\x18\x06 \x03(\x05\"\xa6\x01\n\x13\x43reateReviewRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x15\n\rtotal_batches\x18\x03 \x01(\x05\x12\x12\n\nmission_id\x18\x04 \x01(\x05\x12\x1b\n\x13sample_size_percent\x18\x05 \x01(\x05\x12$\n\rfilter_values\x18\x06 \x01(\x0b\x32\r.FilterValues\"K\n\x14\x43reateReviewResponse\x12 \n\x0b\x63hange_type\x18\x01 \x01(\x0e\x32\x0b.ChangeType\x12\x11\n\treview_id\x18\x02 \x01(\x05\"#\n\x15\x46indReviewByIdRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"S\n\x16\x46indReviewByIdResponse\x12 \n\x0b\x63hange_type\x18\x01 \x01(\x0e\x32\x0b.ChangeType\x12\x17\n\x06review\x18\x02 \x01(\x0b\x32\x07.Review\"#\n\x12ListReviewsRequest\x12\r\n\x05query\x18\x01 \x01(\t\"Q\n\x13ListReviewsResponse\x12 \n\x0b\x63hange_type\x18\x01 \x01(\x0e\x32\x0b.ChangeType\x12\x18\n\x07reviews\x18\x02 \x03(\x0b\x32\x07.Review\".\n\x18GetReviewProgressRequest\x12\x12\n\nreview_ids\x18\x01 \x03(\x05\"\xda\x01\n\x19GetReviewProgressResponse\x12\x45\n\x0freview_progress\x18\x01 \x03(\x0b\x32,.GetReviewProgressResponse.GetReviewProgress\x1av\n\x11GetReviewProgress\x12\x11\n\treview_id\x18\x01 \x01(\x05\x12\x14\n\x0ctotal_images\x18\x02 \x01(\x05\x12\x1c\n\x14\x61nnotation_completed\x18\x03 \x01(\x05\x12\x1a\n\x12\x61nnotation_skipped\x18\x04 \x01(\x05\x32\xe0\x02\n\tReviewApi\x12M\n\x12\x43\x61\x63heLastUserQuery\x12\x1a.CacheLastUserQueryRequest\x1a\x1b.CacheLastUserQueryResponse\x12;\n\x0c\x43reateReview\x12\x14.CreateReviewRequest\x1a\x15.CreateReviewResponse\x12\x41\n\x0e\x46indReviewById\x12\x16.FindReviewByIdRequest\x1a\x17.FindReviewByIdResponse\x12\x38\n\x0bListReviews\x12\x13.ListReviewsRequest\x1a\x14.ListReviewsResponse\x12J\n\x11GetReviewProgress\x12\x19.GetReviewProgressRequest\x1a\x1a.GetReviewProgressResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'global_vo_grpc_service.protos.review_api_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REVIEW._serialized_start=127
  _REVIEW._serialized_end=406
  _CACHELASTUSERQUERYREQUEST._serialized_start=408
  _CACHELASTUSERQUERYREQUEST._serialized_end=482
  _CACHELASTUSERQUERYRESPONSE._serialized_start=484
  _CACHELASTUSERQUERYRESPONSE._serialized_end=546
  _HEIGHTRANGE._serialized_start=548
  _HEIGHTRANGE._serialized_end=587
  _SCORERANGE._serialized_start=589
  _SCORERANGE._serialized_end=627
  _FILTERVALUES._serialized_start=630
  _FILTERVALUES._serialized_end=800
  _CREATEREVIEWREQUEST._serialized_start=803
  _CREATEREVIEWREQUEST._serialized_end=969
  _CREATEREVIEWRESPONSE._serialized_start=971
  _CREATEREVIEWRESPONSE._serialized_end=1046
  _FINDREVIEWBYIDREQUEST._serialized_start=1048
  _FINDREVIEWBYIDREQUEST._serialized_end=1083
  _FINDREVIEWBYIDRESPONSE._serialized_start=1085
  _FINDREVIEWBYIDRESPONSE._serialized_end=1168
  _LISTREVIEWSREQUEST._serialized_start=1170
  _LISTREVIEWSREQUEST._serialized_end=1205
  _LISTREVIEWSRESPONSE._serialized_start=1207
  _LISTREVIEWSRESPONSE._serialized_end=1288
  _GETREVIEWPROGRESSREQUEST._serialized_start=1290
  _GETREVIEWPROGRESSREQUEST._serialized_end=1336
  _GETREVIEWPROGRESSRESPONSE._serialized_start=1339
  _GETREVIEWPROGRESSRESPONSE._serialized_end=1557
  _GETREVIEWPROGRESSRESPONSE_GETREVIEWPROGRESS._serialized_start=1439
  _GETREVIEWPROGRESSRESPONSE_GETREVIEWPROGRESS._serialized_end=1557
  _REVIEWAPI._serialized_start=1560
  _REVIEWAPI._serialized_end=1912
# @@protoc_insertion_point(module_scope)
