# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: wandb/proto/wandb_server.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from wandb.proto import wandb_base_pb2 as wandb_dot_proto_dot_wandb__base__pb2
from wandb.proto import wandb_internal_pb2 as wandb_dot_proto_dot_wandb__internal__pb2
from wandb.proto import wandb_settings_pb2 as wandb_dot_proto_dot_wandb__settings__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1ewandb/proto/wandb_server.proto\x12\x0ewandb_internal\x1a\x1cwandb/proto/wandb_base.proto\x1a wandb/proto/wandb_internal.proto\x1a wandb/proto/wandb_settings.proto\"k\n\x19ServerAuthenticateRequest\x12\x0f\n\x07\x61pi_key\x18\x01 \x01(\t\x12\x10\n\x08\x62\x61se_url\x18\x02 \x01(\t\x12+\n\x05_info\x18\xc8\x01 \x01(\x0b\x32\x1b.wandb_internal._RecordInfo\"w\n\x1aServerAuthenticateResponse\x12\x16\n\x0e\x64\x65\x66\x61ult_entity\x18\x01 \x01(\t\x12\x14\n\x0c\x65rror_status\x18\x02 \x01(\t\x12+\n\x05_info\x18\xc8\x01 \x01(\x0b\x32\x1b.wandb_internal._RecordInfo\"D\n\x15ServerShutdownRequest\x12+\n\x05_info\x18\xc8\x01 \x01(\x0b\x32\x1b.wandb_internal._RecordInfo\"\x18\n\x16ServerShutdownResponse\"B\n\x13ServerStatusRequest\x12+\n\x05_info\x18\xc8\x01 \x01(\x0b\x32\x1b.wandb_internal._RecordInfo\"\x16\n\x14ServerStatusResponse\"r\n\x17ServerInformInitRequest\x12*\n\x08settings\x18\x01 \x01(\x0b\x32\x18.wandb_internal.Settings\x12+\n\x05_info\x18\xc8\x01 \x01(\x0b\x32\x1b.wandb_internal._RecordInfo\"\x1a\n\x18ServerInformInitResponse\"s\n\x18ServerInformStartRequest\x12*\n\x08settings\x18\x01 \x01(\x0b\x32\x18.wandb_internal.Settings\x12+\n\x05_info\x18\xc8\x01 \x01(\x0b\x32\x1b.wandb_internal._RecordInfo\"\x1b\n\x19ServerInformStartResponse\"H\n\x19ServerInformFinishRequest\x12+\n\x05_info\x18\xc8\x01 \x01(\x0b\x32\x1b.wandb_internal._RecordInfo\"\x1c\n\x1aServerInformFinishResponse\"H\n\x19ServerInformAttachRequest\x12+\n\x05_info\x18\xc8\x01 \x01(\x0b\x32\x1b.wandb_internal._RecordInfo\"u\n\x1aServerInformAttachResponse\x12*\n\x08settings\x18\x01 \x01(\x0b\x32\x18.wandb_internal.Settings\x12+\n\x05_info\x18\xc8\x01 \x01(\x0b\x32\x1b.wandb_internal._RecordInfo\"H\n\x19ServerInformDetachRequest\x12+\n\x05_info\x18\xc8\x01 \x01(\x0b\x32\x1b.wandb_internal._RecordInfo\"\x1c\n\x1aServerInformDetachResponse\"]\n\x1bServerInformTeardownRequest\x12\x11\n\texit_code\x18\x01 \x01(\x05\x12+\n\x05_info\x18\xc8\x01 \x01(\x0b\x32\x1b.wandb_internal._RecordInfo\"\x1e\n\x1cServerInformTeardownResponse\"\xe7\x04\n\rServerRequest\x12\x30\n\x0erecord_publish\x18\x01 \x01(\x0b\x32\x16.wandb_internal.RecordH\x00\x12\x34\n\x12record_communicate\x18\x02 \x01(\x0b\x32\x16.wandb_internal.RecordH\x00\x12>\n\x0binform_init\x18\x03 \x01(\x0b\x32\'.wandb_internal.ServerInformInitRequestH\x00\x12\x42\n\rinform_finish\x18\x04 \x01(\x0b\x32).wandb_internal.ServerInformFinishRequestH\x00\x12\x42\n\rinform_attach\x18\x05 \x01(\x0b\x32).wandb_internal.ServerInformAttachRequestH\x00\x12\x42\n\rinform_detach\x18\x06 \x01(\x0b\x32).wandb_internal.ServerInformDetachRequestH\x00\x12\x46\n\x0finform_teardown\x18\x07 \x01(\x0b\x32+.wandb_internal.ServerInformTeardownRequestH\x00\x12@\n\x0cinform_start\x18\x08 \x01(\x0b\x32(.wandb_internal.ServerInformStartRequestH\x00\x12\x41\n\x0c\x61uthenticate\x18\t \x01(\x0b\x32).wandb_internal.ServerAuthenticateRequestH\x00\x42\x15\n\x13server_request_type\"\xfd\x04\n\x0eServerResponse\x12\x34\n\x12result_communicate\x18\x02 \x01(\x0b\x32\x16.wandb_internal.ResultH\x00\x12H\n\x14inform_init_response\x18\x03 \x01(\x0b\x32(.wandb_internal.ServerInformInitResponseH\x00\x12L\n\x16inform_finish_response\x18\x04 \x01(\x0b\x32*.wandb_internal.ServerInformFinishResponseH\x00\x12L\n\x16inform_attach_response\x18\x05 \x01(\x0b\x32*.wandb_internal.ServerInformAttachResponseH\x00\x12L\n\x16inform_detach_response\x18\x06 \x01(\x0b\x32*.wandb_internal.ServerInformDetachResponseH\x00\x12P\n\x18inform_teardown_response\x18\x07 \x01(\x0b\x32,.wandb_internal.ServerInformTeardownResponseH\x00\x12J\n\x15inform_start_response\x18\x08 \x01(\x0b\x32).wandb_internal.ServerInformStartResponseH\x00\x12K\n\x15\x61uthenticate_response\x18\t \x01(\x0b\x32*.wandb_internal.ServerAuthenticateResponseH\x00\x42\x16\n\x14server_response_typeB\x1bZ\x19\x63ore/pkg/service_go_protob\x06proto3')



_SERVERAUTHENTICATEREQUEST = DESCRIPTOR.message_types_by_name['ServerAuthenticateRequest']
_SERVERAUTHENTICATERESPONSE = DESCRIPTOR.message_types_by_name['ServerAuthenticateResponse']
_SERVERSHUTDOWNREQUEST = DESCRIPTOR.message_types_by_name['ServerShutdownRequest']
_SERVERSHUTDOWNRESPONSE = DESCRIPTOR.message_types_by_name['ServerShutdownResponse']
_SERVERSTATUSREQUEST = DESCRIPTOR.message_types_by_name['ServerStatusRequest']
_SERVERSTATUSRESPONSE = DESCRIPTOR.message_types_by_name['ServerStatusResponse']
_SERVERINFORMINITREQUEST = DESCRIPTOR.message_types_by_name['ServerInformInitRequest']
_SERVERINFORMINITRESPONSE = DESCRIPTOR.message_types_by_name['ServerInformInitResponse']
_SERVERINFORMSTARTREQUEST = DESCRIPTOR.message_types_by_name['ServerInformStartRequest']
_SERVERINFORMSTARTRESPONSE = DESCRIPTOR.message_types_by_name['ServerInformStartResponse']
_SERVERINFORMFINISHREQUEST = DESCRIPTOR.message_types_by_name['ServerInformFinishRequest']
_SERVERINFORMFINISHRESPONSE = DESCRIPTOR.message_types_by_name['ServerInformFinishResponse']
_SERVERINFORMATTACHREQUEST = DESCRIPTOR.message_types_by_name['ServerInformAttachRequest']
_SERVERINFORMATTACHRESPONSE = DESCRIPTOR.message_types_by_name['ServerInformAttachResponse']
_SERVERINFORMDETACHREQUEST = DESCRIPTOR.message_types_by_name['ServerInformDetachRequest']
_SERVERINFORMDETACHRESPONSE = DESCRIPTOR.message_types_by_name['ServerInformDetachResponse']
_SERVERINFORMTEARDOWNREQUEST = DESCRIPTOR.message_types_by_name['ServerInformTeardownRequest']
_SERVERINFORMTEARDOWNRESPONSE = DESCRIPTOR.message_types_by_name['ServerInformTeardownResponse']
_SERVERREQUEST = DESCRIPTOR.message_types_by_name['ServerRequest']
_SERVERRESPONSE = DESCRIPTOR.message_types_by_name['ServerResponse']
ServerAuthenticateRequest = _reflection.GeneratedProtocolMessageType('ServerAuthenticateRequest', (_message.Message,), {
  'DESCRIPTOR' : _SERVERAUTHENTICATEREQUEST,
  '__module__' : 'wandb.proto.wandb_server_pb2'
  # @@protoc_insertion_point(class_scope:wandb_internal.ServerAuthenticateRequest)
  })
_sym_db.RegisterMessage(ServerAuthenticateRequest)

ServerAuthenticateResponse = _reflection.GeneratedProtocolMessageType('ServerAuthenticateResponse', (_message.Message,), {
  'DESCRIPTOR' : _SERVERAUTHENTICATERESPONSE,
  '__module__' : 'wandb.proto.wandb_server_pb2'
  # @@protoc_insertion_point(class_scope:wandb_internal.ServerAuthenticateResponse)
  })
_sym_db.RegisterMessage(ServerAuthenticateResponse)

ServerShutdownRequest = _reflection.GeneratedProtocolMessageType('ServerShutdownRequest', (_message.Message,), {
  'DESCRIPTOR' : _SERVERSHUTDOWNREQUEST,
  '__module__' : 'wandb.proto.wandb_server_pb2'
  # @@protoc_insertion_point(class_scope:wandb_internal.ServerShutdownRequest)
  })
_sym_db.RegisterMessage(ServerShutdownRequest)

ServerShutdownResponse = _reflection.GeneratedProtocolMessageType('ServerShutdownResponse', (_message.Message,), {
  'DESCRIPTOR' : _SERVERSHUTDOWNRESPONSE,
  '__module__' : 'wandb.proto.wandb_server_pb2'
  # @@protoc_insertion_point(class_scope:wandb_internal.ServerShutdownResponse)
  })
_sym_db.RegisterMessage(ServerShutdownResponse)

ServerStatusRequest = _reflection.GeneratedProtocolMessageType('ServerStatusRequest', (_message.Message,), {
  'DESCRIPTOR' : _SERVERSTATUSREQUEST,
  '__module__' : 'wandb.proto.wandb_server_pb2'
  # @@protoc_insertion_point(class_scope:wandb_internal.ServerStatusRequest)
  })
_sym_db.RegisterMessage(ServerStatusRequest)

ServerStatusResponse = _reflection.GeneratedProtocolMessageType('ServerStatusResponse', (_message.Message,), {
  'DESCRIPTOR' : _SERVERSTATUSRESPONSE,
  '__module__' : 'wandb.proto.wandb_server_pb2'
  # @@protoc_insertion_point(class_scope:wandb_internal.ServerStatusResponse)
  })
_sym_db.RegisterMessage(ServerStatusResponse)

ServerInformInitRequest = _reflection.GeneratedProtocolMessageType('ServerInformInitRequest', (_message.Message,), {
  'DESCRIPTOR' : _SERVERINFORMINITREQUEST,
  '__module__' : 'wandb.proto.wandb_server_pb2'
  # @@protoc_insertion_point(class_scope:wandb_internal.ServerInformInitRequest)
  })
_sym_db.RegisterMessage(ServerInformInitRequest)

ServerInformInitResponse = _reflection.GeneratedProtocolMessageType('ServerInformInitResponse', (_message.Message,), {
  'DESCRIPTOR' : _SERVERINFORMINITRESPONSE,
  '__module__' : 'wandb.proto.wandb_server_pb2'
  # @@protoc_insertion_point(class_scope:wandb_internal.ServerInformInitResponse)
  })
_sym_db.RegisterMessage(ServerInformInitResponse)

ServerInformStartRequest = _reflection.GeneratedProtocolMessageType('ServerInformStartRequest', (_message.Message,), {
  'DESCRIPTOR' : _SERVERINFORMSTARTREQUEST,
  '__module__' : 'wandb.proto.wandb_server_pb2'
  # @@protoc_insertion_point(class_scope:wandb_internal.ServerInformStartRequest)
  })
_sym_db.RegisterMessage(ServerInformStartRequest)

ServerInformStartResponse = _reflection.GeneratedProtocolMessageType('ServerInformStartResponse', (_message.Message,), {
  'DESCRIPTOR' : _SERVERINFORMSTARTRESPONSE,
  '__module__' : 'wandb.proto.wandb_server_pb2'
  # @@protoc_insertion_point(class_scope:wandb_internal.ServerInformStartResponse)
  })
_sym_db.RegisterMessage(ServerInformStartResponse)

ServerInformFinishRequest = _reflection.GeneratedProtocolMessageType('ServerInformFinishRequest', (_message.Message,), {
  'DESCRIPTOR' : _SERVERINFORMFINISHREQUEST,
  '__module__' : 'wandb.proto.wandb_server_pb2'
  # @@protoc_insertion_point(class_scope:wandb_internal.ServerInformFinishRequest)
  })
_sym_db.RegisterMessage(ServerInformFinishRequest)

ServerInformFinishResponse = _reflection.GeneratedProtocolMessageType('ServerInformFinishResponse', (_message.Message,), {
  'DESCRIPTOR' : _SERVERINFORMFINISHRESPONSE,
  '__module__' : 'wandb.proto.wandb_server_pb2'
  # @@protoc_insertion_point(class_scope:wandb_internal.ServerInformFinishResponse)
  })
_sym_db.RegisterMessage(ServerInformFinishResponse)

ServerInformAttachRequest = _reflection.GeneratedProtocolMessageType('ServerInformAttachRequest', (_message.Message,), {
  'DESCRIPTOR' : _SERVERINFORMATTACHREQUEST,
  '__module__' : 'wandb.proto.wandb_server_pb2'
  # @@protoc_insertion_point(class_scope:wandb_internal.ServerInformAttachRequest)
  })
_sym_db.RegisterMessage(ServerInformAttachRequest)

ServerInformAttachResponse = _reflection.GeneratedProtocolMessageType('ServerInformAttachResponse', (_message.Message,), {
  'DESCRIPTOR' : _SERVERINFORMATTACHRESPONSE,
  '__module__' : 'wandb.proto.wandb_server_pb2'
  # @@protoc_insertion_point(class_scope:wandb_internal.ServerInformAttachResponse)
  })
_sym_db.RegisterMessage(ServerInformAttachResponse)

ServerInformDetachRequest = _reflection.GeneratedProtocolMessageType('ServerInformDetachRequest', (_message.Message,), {
  'DESCRIPTOR' : _SERVERINFORMDETACHREQUEST,
  '__module__' : 'wandb.proto.wandb_server_pb2'
  # @@protoc_insertion_point(class_scope:wandb_internal.ServerInformDetachRequest)
  })
_sym_db.RegisterMessage(ServerInformDetachRequest)

ServerInformDetachResponse = _reflection.GeneratedProtocolMessageType('ServerInformDetachResponse', (_message.Message,), {
  'DESCRIPTOR' : _SERVERINFORMDETACHRESPONSE,
  '__module__' : 'wandb.proto.wandb_server_pb2'
  # @@protoc_insertion_point(class_scope:wandb_internal.ServerInformDetachResponse)
  })
_sym_db.RegisterMessage(ServerInformDetachResponse)

ServerInformTeardownRequest = _reflection.GeneratedProtocolMessageType('ServerInformTeardownRequest', (_message.Message,), {
  'DESCRIPTOR' : _SERVERINFORMTEARDOWNREQUEST,
  '__module__' : 'wandb.proto.wandb_server_pb2'
  # @@protoc_insertion_point(class_scope:wandb_internal.ServerInformTeardownRequest)
  })
_sym_db.RegisterMessage(ServerInformTeardownRequest)

ServerInformTeardownResponse = _reflection.GeneratedProtocolMessageType('ServerInformTeardownResponse', (_message.Message,), {
  'DESCRIPTOR' : _SERVERINFORMTEARDOWNRESPONSE,
  '__module__' : 'wandb.proto.wandb_server_pb2'
  # @@protoc_insertion_point(class_scope:wandb_internal.ServerInformTeardownResponse)
  })
_sym_db.RegisterMessage(ServerInformTeardownResponse)

ServerRequest = _reflection.GeneratedProtocolMessageType('ServerRequest', (_message.Message,), {
  'DESCRIPTOR' : _SERVERREQUEST,
  '__module__' : 'wandb.proto.wandb_server_pb2'
  # @@protoc_insertion_point(class_scope:wandb_internal.ServerRequest)
  })
_sym_db.RegisterMessage(ServerRequest)

ServerResponse = _reflection.GeneratedProtocolMessageType('ServerResponse', (_message.Message,), {
  'DESCRIPTOR' : _SERVERRESPONSE,
  '__module__' : 'wandb.proto.wandb_server_pb2'
  # @@protoc_insertion_point(class_scope:wandb_internal.ServerResponse)
  })
_sym_db.RegisterMessage(ServerResponse)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\031core/pkg/service_go_proto'
  _SERVERAUTHENTICATEREQUEST._serialized_start=148
  _SERVERAUTHENTICATEREQUEST._serialized_end=255
  _SERVERAUTHENTICATERESPONSE._serialized_start=257
  _SERVERAUTHENTICATERESPONSE._serialized_end=376
  _SERVERSHUTDOWNREQUEST._serialized_start=378
  _SERVERSHUTDOWNREQUEST._serialized_end=446
  _SERVERSHUTDOWNRESPONSE._serialized_start=448
  _SERVERSHUTDOWNRESPONSE._serialized_end=472
  _SERVERSTATUSREQUEST._serialized_start=474
  _SERVERSTATUSREQUEST._serialized_end=540
  _SERVERSTATUSRESPONSE._serialized_start=542
  _SERVERSTATUSRESPONSE._serialized_end=564
  _SERVERINFORMINITREQUEST._serialized_start=566
  _SERVERINFORMINITREQUEST._serialized_end=680
  _SERVERINFORMINITRESPONSE._serialized_start=682
  _SERVERINFORMINITRESPONSE._serialized_end=708
  _SERVERINFORMSTARTREQUEST._serialized_start=710
  _SERVERINFORMSTARTREQUEST._serialized_end=825
  _SERVERINFORMSTARTRESPONSE._serialized_start=827
  _SERVERINFORMSTARTRESPONSE._serialized_end=854
  _SERVERINFORMFINISHREQUEST._serialized_start=856
  _SERVERINFORMFINISHREQUEST._serialized_end=928
  _SERVERINFORMFINISHRESPONSE._serialized_start=930
  _SERVERINFORMFINISHRESPONSE._serialized_end=958
  _SERVERINFORMATTACHREQUEST._serialized_start=960
  _SERVERINFORMATTACHREQUEST._serialized_end=1032
  _SERVERINFORMATTACHRESPONSE._serialized_start=1034
  _SERVERINFORMATTACHRESPONSE._serialized_end=1151
  _SERVERINFORMDETACHREQUEST._serialized_start=1153
  _SERVERINFORMDETACHREQUEST._serialized_end=1225
  _SERVERINFORMDETACHRESPONSE._serialized_start=1227
  _SERVERINFORMDETACHRESPONSE._serialized_end=1255
  _SERVERINFORMTEARDOWNREQUEST._serialized_start=1257
  _SERVERINFORMTEARDOWNREQUEST._serialized_end=1350
  _SERVERINFORMTEARDOWNRESPONSE._serialized_start=1352
  _SERVERINFORMTEARDOWNRESPONSE._serialized_end=1382
  _SERVERREQUEST._serialized_start=1385
  _SERVERREQUEST._serialized_end=2000
  _SERVERRESPONSE._serialized_start=2003
  _SERVERRESPONSE._serialized_end=2640
# @@protoc_insertion_point(module_scope)
