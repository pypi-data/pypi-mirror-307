# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: kerfed/protos/common/v1/scene.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from kerfed.protos.common.v1 import fileblob_pb2 as kerfed_dot_protos_dot_common_dot_v1_dot_fileblob__pb2
from kerfed.protos.common.v1 import outcome_pb2 as kerfed_dot_protos_dot_common_dot_v1_dot_outcome__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#kerfed/protos/common/v1/scene.proto\x12\x17kerfed.protos.common.v1\x1a&kerfed/protos/common/v1/fileblob.proto\x1a%kerfed/protos/common/v1/outcome.proto\"\x94\x01\n\x0fGeometrySummary\x12\x17\n\x07geom_id\x18\x01 \x01(\tR\x06geomId\x12\x17\n\x07node_id\x18\x02 \x03(\tR\x06nodeId\x12\x12\n\x04name\x18\x03 \x01(\tR\x04name\x12;\n\x07preview\x18\x04 \x01(\x0b\x32!.kerfed.protos.common.v1.FileBlobR\x07preview\"\xda\x02\n\x05Scene\x12;\n\x07neutral\x18\x01 \x01(\x0b\x32!.kerfed.protos.common.v1.FileBlobR\x07neutral\x12=\n\x08original\x18\x02 \x01(\x0b\x32!.kerfed.protos.common.v1.FileBlobR\x08original\x12\x12\n\x04name\x18\x03 \x01(\tR\x04name\x12H\n\ngeometries\x18\x04 \x03(\x0b\x32(.kerfed.protos.common.v1.GeometrySummaryR\ngeometries\x12;\n\x07preview\x18\x05 \x01(\x0b\x32!.kerfed.protos.common.v1.FileBlobR\x07preview\x12:\n\x07outcome\x18\x06 \x01(\x0b\x32 .kerfed.protos.common.v1.OutcomeR\x07outcomeB\xe3\x01\n\x1b\x63om.kerfed.protos.common.v1B\nSceneProtoP\x01Z9github.com/kerfed/protos/kerfed/protos/common/v1;commonv1\xa2\x02\x03KPC\xaa\x02\x17Kerfed.Protos.Common.V1\xca\x02\x17Kerfed\\Protos\\Common\\V1\xe2\x02#Kerfed\\Protos\\Common\\V1\\GPBMetadata\xea\x02\x1aKerfed::Protos::Common::V1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'kerfed.protos.common.v1.scene_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\033com.kerfed.protos.common.v1B\nSceneProtoP\001Z9github.com/kerfed/protos/kerfed/protos/common/v1;commonv1\242\002\003KPC\252\002\027Kerfed.Protos.Common.V1\312\002\027Kerfed\\Protos\\Common\\V1\342\002#Kerfed\\Protos\\Common\\V1\\GPBMetadata\352\002\032Kerfed::Protos::Common::V1'
  _globals['_GEOMETRYSUMMARY']._serialized_start=144
  _globals['_GEOMETRYSUMMARY']._serialized_end=292
  _globals['_SCENE']._serialized_start=295
  _globals['_SCENE']._serialized_end=641
# @@protoc_insertion_point(module_scope)
