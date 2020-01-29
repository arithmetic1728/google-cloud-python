# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/cloud/automl_v1/proto/data_items.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.cloud.automl_v1.proto import (
    geometry_pb2 as google_dot_cloud_dot_automl__v1_dot_proto_dot_geometry__pb2,
)
from google.cloud.automl_v1.proto import (
    io_pb2 as google_dot_cloud_dot_automl__v1_dot_proto_dot_io__pb2,
)
from google.cloud.automl_v1.proto import (
    text_segment_pb2 as google_dot_cloud_dot_automl__v1_dot_proto_dot_text__segment__pb2,
)
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
    name="google/cloud/automl_v1/proto/data_items.proto",
    package="google.cloud.automl.v1",
    syntax="proto3",
    serialized_options=_b(
        "\n\032com.google.cloud.automl.v1P\001Z<google.golang.org/genproto/googleapis/cloud/automl/v1;automl\252\002\026Google.Cloud.AutoML.V1\312\002\026Google\\Cloud\\AutoMl\\V1\352\002\031Google::Cloud::AutoML::V1"
    ),
    serialized_pb=_b(
        '\n-google/cloud/automl_v1/proto/data_items.proto\x12\x16google.cloud.automl.v1\x1a\x1cgoogle/api/annotations.proto\x1a+google/cloud/automl_v1/proto/geometry.proto\x1a%google/cloud/automl_v1/proto/io.proto\x1a/google/cloud/automl_v1/proto/text_segment.proto\x1a\x19google/protobuf/any.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1cgoogle/protobuf/struct.proto"=\n\x05Image\x12\x15\n\x0bimage_bytes\x18\x01 \x01(\x0cH\x00\x12\x15\n\rthumbnail_uri\x18\x04 \x01(\tB\x06\n\x04\x64\x61ta"F\n\x0bTextSnippet\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\t\x12\x11\n\tmime_type\x18\x02 \x01(\t\x12\x13\n\x0b\x63ontent_uri\x18\x04 \x01(\t"\xea\x01\n\x12\x44ocumentDimensions\x12N\n\x04unit\x18\x01 \x01(\x0e\x32@.google.cloud.automl.v1.DocumentDimensions.DocumentDimensionUnit\x12\r\n\x05width\x18\x02 \x01(\x02\x12\x0e\n\x06height\x18\x03 \x01(\x02"e\n\x15\x44ocumentDimensionUnit\x12\'\n#DOCUMENT_DIMENSION_UNIT_UNSPECIFIED\x10\x00\x12\x08\n\x04INCH\x10\x01\x12\x0e\n\nCENTIMETER\x10\x02\x12\t\n\x05POINT\x10\x03"\xd6\x05\n\x08\x44ocument\x12\x41\n\x0cinput_config\x18\x01 \x01(\x0b\x32+.google.cloud.automl.v1.DocumentInputConfig\x12:\n\rdocument_text\x18\x02 \x01(\x0b\x32#.google.cloud.automl.v1.TextSnippet\x12\x37\n\x06layout\x18\x03 \x03(\x0b\x32\'.google.cloud.automl.v1.Document.Layout\x12G\n\x13\x64ocument_dimensions\x18\x04 \x01(\x0b\x32*.google.cloud.automl.v1.DocumentDimensions\x12\x12\n\npage_count\x18\x05 \x01(\x05\x1a\xb4\x03\n\x06Layout\x12\x39\n\x0ctext_segment\x18\x01 \x01(\x0b\x32#.google.cloud.automl.v1.TextSegment\x12\x13\n\x0bpage_number\x18\x02 \x01(\x05\x12;\n\rbounding_poly\x18\x03 \x01(\x0b\x32$.google.cloud.automl.v1.BoundingPoly\x12R\n\x11text_segment_type\x18\x04 \x01(\x0e\x32\x37.google.cloud.automl.v1.Document.Layout.TextSegmentType"\xc8\x01\n\x0fTextSegmentType\x12!\n\x1dTEXT_SEGMENT_TYPE_UNSPECIFIED\x10\x00\x12\t\n\x05TOKEN\x10\x01\x12\r\n\tPARAGRAPH\x10\x02\x12\x0e\n\nFORM_FIELD\x10\x03\x12\x13\n\x0f\x46ORM_FIELD_NAME\x10\x04\x12\x17\n\x13\x46ORM_FIELD_CONTENTS\x10\x05\x12\t\n\x05TABLE\x10\x06\x12\x10\n\x0cTABLE_HEADER\x10\x07\x12\r\n\tTABLE_ROW\x10\x08\x12\x0e\n\nTABLE_CELL\x10\t"\xbe\x01\n\x0e\x45xamplePayload\x12.\n\x05image\x18\x01 \x01(\x0b\x32\x1d.google.cloud.automl.v1.ImageH\x00\x12;\n\x0ctext_snippet\x18\x02 \x01(\x0b\x32#.google.cloud.automl.v1.TextSnippetH\x00\x12\x34\n\x08\x64ocument\x18\x04 \x01(\x0b\x32 .google.cloud.automl.v1.DocumentH\x00\x42\t\n\x07payloadB\xaa\x01\n\x1a\x63om.google.cloud.automl.v1P\x01Z<google.golang.org/genproto/googleapis/cloud/automl/v1;automl\xaa\x02\x16Google.Cloud.AutoML.V1\xca\x02\x16Google\\Cloud\\AutoMl\\V1\xea\x02\x19Google::Cloud::AutoML::V1b\x06proto3'
    ),
    dependencies=[
        google_dot_api_dot_annotations__pb2.DESCRIPTOR,
        google_dot_cloud_dot_automl__v1_dot_proto_dot_geometry__pb2.DESCRIPTOR,
        google_dot_cloud_dot_automl__v1_dot_proto_dot_io__pb2.DESCRIPTOR,
        google_dot_cloud_dot_automl__v1_dot_proto_dot_text__segment__pb2.DESCRIPTOR,
        google_dot_protobuf_dot_any__pb2.DESCRIPTOR,
        google_dot_protobuf_dot_duration__pb2.DESCRIPTOR,
        google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,
    ],
)


_DOCUMENTDIMENSIONS_DOCUMENTDIMENSIONUNIT = _descriptor.EnumDescriptor(
    name="DocumentDimensionUnit",
    full_name="google.cloud.automl.v1.DocumentDimensions.DocumentDimensionUnit",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="DOCUMENT_DIMENSION_UNIT_UNSPECIFIED",
            index=0,
            number=0,
            serialized_options=None,
            type=None,
        ),
        _descriptor.EnumValueDescriptor(
            name="INCH", index=1, number=1, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="CENTIMETER", index=2, number=2, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="POINT", index=3, number=3, serialized_options=None, type=None
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=594,
    serialized_end=695,
)
_sym_db.RegisterEnumDescriptor(_DOCUMENTDIMENSIONS_DOCUMENTDIMENSIONUNIT)

_DOCUMENT_LAYOUT_TEXTSEGMENTTYPE = _descriptor.EnumDescriptor(
    name="TextSegmentType",
    full_name="google.cloud.automl.v1.Document.Layout.TextSegmentType",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="TEXT_SEGMENT_TYPE_UNSPECIFIED",
            index=0,
            number=0,
            serialized_options=None,
            type=None,
        ),
        _descriptor.EnumValueDescriptor(
            name="TOKEN", index=1, number=1, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PARAGRAPH", index=2, number=2, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="FORM_FIELD", index=3, number=3, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="FORM_FIELD_NAME",
            index=4,
            number=4,
            serialized_options=None,
            type=None,
        ),
        _descriptor.EnumValueDescriptor(
            name="FORM_FIELD_CONTENTS",
            index=5,
            number=5,
            serialized_options=None,
            type=None,
        ),
        _descriptor.EnumValueDescriptor(
            name="TABLE", index=6, number=6, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="TABLE_HEADER", index=7, number=7, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="TABLE_ROW", index=8, number=8, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="TABLE_CELL", index=9, number=9, serialized_options=None, type=None
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=1224,
    serialized_end=1424,
)
_sym_db.RegisterEnumDescriptor(_DOCUMENT_LAYOUT_TEXTSEGMENTTYPE)


_IMAGE = _descriptor.Descriptor(
    name="Image",
    full_name="google.cloud.automl.v1.Image",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="image_bytes",
            full_name="google.cloud.automl.v1.Image.image_bytes",
            index=0,
            number=1,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="thumbnail_uri",
            full_name="google.cloud.automl.v1.Image.thumbnail_uri",
            index=1,
            number=4,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[
        _descriptor.OneofDescriptor(
            name="data",
            full_name="google.cloud.automl.v1.Image.data",
            index=0,
            containing_type=None,
            fields=[],
        )
    ],
    serialized_start=325,
    serialized_end=386,
)


_TEXTSNIPPET = _descriptor.Descriptor(
    name="TextSnippet",
    full_name="google.cloud.automl.v1.TextSnippet",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="content",
            full_name="google.cloud.automl.v1.TextSnippet.content",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="mime_type",
            full_name="google.cloud.automl.v1.TextSnippet.mime_type",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="content_uri",
            full_name="google.cloud.automl.v1.TextSnippet.content_uri",
            index=2,
            number=4,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=388,
    serialized_end=458,
)


_DOCUMENTDIMENSIONS = _descriptor.Descriptor(
    name="DocumentDimensions",
    full_name="google.cloud.automl.v1.DocumentDimensions",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="unit",
            full_name="google.cloud.automl.v1.DocumentDimensions.unit",
            index=0,
            number=1,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="width",
            full_name="google.cloud.automl.v1.DocumentDimensions.width",
            index=1,
            number=2,
            type=2,
            cpp_type=6,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="height",
            full_name="google.cloud.automl.v1.DocumentDimensions.height",
            index=2,
            number=3,
            type=2,
            cpp_type=6,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[_DOCUMENTDIMENSIONS_DOCUMENTDIMENSIONUNIT],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=461,
    serialized_end=695,
)


_DOCUMENT_LAYOUT = _descriptor.Descriptor(
    name="Layout",
    full_name="google.cloud.automl.v1.Document.Layout",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="text_segment",
            full_name="google.cloud.automl.v1.Document.Layout.text_segment",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="page_number",
            full_name="google.cloud.automl.v1.Document.Layout.page_number",
            index=1,
            number=2,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="bounding_poly",
            full_name="google.cloud.automl.v1.Document.Layout.bounding_poly",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="text_segment_type",
            full_name="google.cloud.automl.v1.Document.Layout.text_segment_type",
            index=3,
            number=4,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[_DOCUMENT_LAYOUT_TEXTSEGMENTTYPE],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=988,
    serialized_end=1424,
)

_DOCUMENT = _descriptor.Descriptor(
    name="Document",
    full_name="google.cloud.automl.v1.Document",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="input_config",
            full_name="google.cloud.automl.v1.Document.input_config",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="document_text",
            full_name="google.cloud.automl.v1.Document.document_text",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="layout",
            full_name="google.cloud.automl.v1.Document.layout",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="document_dimensions",
            full_name="google.cloud.automl.v1.Document.document_dimensions",
            index=3,
            number=4,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="page_count",
            full_name="google.cloud.automl.v1.Document.page_count",
            index=4,
            number=5,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[_DOCUMENT_LAYOUT],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=698,
    serialized_end=1424,
)


_EXAMPLEPAYLOAD = _descriptor.Descriptor(
    name="ExamplePayload",
    full_name="google.cloud.automl.v1.ExamplePayload",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="image",
            full_name="google.cloud.automl.v1.ExamplePayload.image",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="text_snippet",
            full_name="google.cloud.automl.v1.ExamplePayload.text_snippet",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="document",
            full_name="google.cloud.automl.v1.ExamplePayload.document",
            index=2,
            number=4,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[
        _descriptor.OneofDescriptor(
            name="payload",
            full_name="google.cloud.automl.v1.ExamplePayload.payload",
            index=0,
            containing_type=None,
            fields=[],
        )
    ],
    serialized_start=1427,
    serialized_end=1617,
)

_IMAGE.oneofs_by_name["data"].fields.append(_IMAGE.fields_by_name["image_bytes"])
_IMAGE.fields_by_name["image_bytes"].containing_oneof = _IMAGE.oneofs_by_name["data"]
_DOCUMENTDIMENSIONS.fields_by_name[
    "unit"
].enum_type = _DOCUMENTDIMENSIONS_DOCUMENTDIMENSIONUNIT
_DOCUMENTDIMENSIONS_DOCUMENTDIMENSIONUNIT.containing_type = _DOCUMENTDIMENSIONS
_DOCUMENT_LAYOUT.fields_by_name[
    "text_segment"
].message_type = (
    google_dot_cloud_dot_automl__v1_dot_proto_dot_text__segment__pb2._TEXTSEGMENT
)
_DOCUMENT_LAYOUT.fields_by_name[
    "bounding_poly"
].message_type = (
    google_dot_cloud_dot_automl__v1_dot_proto_dot_geometry__pb2._BOUNDINGPOLY
)
_DOCUMENT_LAYOUT.fields_by_name[
    "text_segment_type"
].enum_type = _DOCUMENT_LAYOUT_TEXTSEGMENTTYPE
_DOCUMENT_LAYOUT.containing_type = _DOCUMENT
_DOCUMENT_LAYOUT_TEXTSEGMENTTYPE.containing_type = _DOCUMENT_LAYOUT
_DOCUMENT.fields_by_name[
    "input_config"
].message_type = (
    google_dot_cloud_dot_automl__v1_dot_proto_dot_io__pb2._DOCUMENTINPUTCONFIG
)
_DOCUMENT.fields_by_name["document_text"].message_type = _TEXTSNIPPET
_DOCUMENT.fields_by_name["layout"].message_type = _DOCUMENT_LAYOUT
_DOCUMENT.fields_by_name["document_dimensions"].message_type = _DOCUMENTDIMENSIONS
_EXAMPLEPAYLOAD.fields_by_name["image"].message_type = _IMAGE
_EXAMPLEPAYLOAD.fields_by_name["text_snippet"].message_type = _TEXTSNIPPET
_EXAMPLEPAYLOAD.fields_by_name["document"].message_type = _DOCUMENT
_EXAMPLEPAYLOAD.oneofs_by_name["payload"].fields.append(
    _EXAMPLEPAYLOAD.fields_by_name["image"]
)
_EXAMPLEPAYLOAD.fields_by_name[
    "image"
].containing_oneof = _EXAMPLEPAYLOAD.oneofs_by_name["payload"]
_EXAMPLEPAYLOAD.oneofs_by_name["payload"].fields.append(
    _EXAMPLEPAYLOAD.fields_by_name["text_snippet"]
)
_EXAMPLEPAYLOAD.fields_by_name[
    "text_snippet"
].containing_oneof = _EXAMPLEPAYLOAD.oneofs_by_name["payload"]
_EXAMPLEPAYLOAD.oneofs_by_name["payload"].fields.append(
    _EXAMPLEPAYLOAD.fields_by_name["document"]
)
_EXAMPLEPAYLOAD.fields_by_name[
    "document"
].containing_oneof = _EXAMPLEPAYLOAD.oneofs_by_name["payload"]
DESCRIPTOR.message_types_by_name["Image"] = _IMAGE
DESCRIPTOR.message_types_by_name["TextSnippet"] = _TEXTSNIPPET
DESCRIPTOR.message_types_by_name["DocumentDimensions"] = _DOCUMENTDIMENSIONS
DESCRIPTOR.message_types_by_name["Document"] = _DOCUMENT
DESCRIPTOR.message_types_by_name["ExamplePayload"] = _EXAMPLEPAYLOAD
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Image = _reflection.GeneratedProtocolMessageType(
    "Image",
    (_message.Message,),
    dict(
        DESCRIPTOR=_IMAGE,
        __module__="google.cloud.automl_v1.proto.data_items_pb2",
        __doc__="""A representation of an image. Only images up to 30MB in
  size are supported.
  
  
  Attributes:
      data:
          Input only. The data representing the image.
      image_bytes:
          Image content represented as a stream of bytes. Note: As with
          all ``bytes`` fields, protobuffers use a pure binary
          representation, whereas JSON representations use base64.
      thumbnail_uri:
          Output only. HTTP URI to the thumbnail image.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.automl.v1.Image)
    ),
)
_sym_db.RegisterMessage(Image)

TextSnippet = _reflection.GeneratedProtocolMessageType(
    "TextSnippet",
    (_message.Message,),
    dict(
        DESCRIPTOR=_TEXTSNIPPET,
        __module__="google.cloud.automl_v1.proto.data_items_pb2",
        __doc__="""A representation of a text snippet.
  
  
  Attributes:
      content:
          Required. The content of the text snippet as a string. Up to
          250000 characters long.
      mime_type:
          Optional. The format of
          [content][google.cloud.automl.v1.TextSnippet.content].
          Currently the only two allowed values are "text/html" and
          "text/plain". If left blank, the format is automatically
          determined from the type of the uploaded
          [content][google.cloud.automl.v1.TextSnippet.content].
      content_uri:
          Output only. HTTP URI where you can download the content.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.automl.v1.TextSnippet)
    ),
)
_sym_db.RegisterMessage(TextSnippet)

DocumentDimensions = _reflection.GeneratedProtocolMessageType(
    "DocumentDimensions",
    (_message.Message,),
    dict(
        DESCRIPTOR=_DOCUMENTDIMENSIONS,
        __module__="google.cloud.automl_v1.proto.data_items_pb2",
        __doc__="""Message that describes dimension of a document.
  
  
  Attributes:
      unit:
          Unit of the dimension.
      width:
          Width value of the document, works together with the unit.
      height:
          Height value of the document, works together with the unit.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.automl.v1.DocumentDimensions)
    ),
)
_sym_db.RegisterMessage(DocumentDimensions)

Document = _reflection.GeneratedProtocolMessageType(
    "Document",
    (_message.Message,),
    dict(
        Layout=_reflection.GeneratedProtocolMessageType(
            "Layout",
            (_message.Message,),
            dict(
                DESCRIPTOR=_DOCUMENT_LAYOUT,
                __module__="google.cloud.automl_v1.proto.data_items_pb2",
                __doc__="""Describes the layout information of a
    [text\_segment][google.cloud.automl.v1.Document.Layout.text\_segment] in
    the document.
    
    
    Attributes:
        text_segment:
            Text Segment that represents a segment in [document\_text][goo
            gle.cloud.automl.v1.Document.document\_text].
        page_number:
            Page number of the [text\_segment][google.cloud.automl.v1.Docu
            ment.Layout.text\_segment] in the original document, starts
            from 1.
        bounding_poly:
            The position of the [text\_segment][google.cloud.automl.v1.Doc
            ument.Layout.text\_segment] in the page. Contains exactly 4  [
            normalized\_vertices][google.cloud.automl.v1.BoundingPoly.norm
            alized\_vertices] and they are connected by edges in the order
            provided, which will represent a rectangle parallel to the
            frame. The
            [NormalizedVertex-s][google.cloud.automl.v1.NormalizedVertex]
            are relative to the page. Coordinates are based on top-left as
            point (0,0).
        text_segment_type:
            The type of the [text\_segment][google.cloud.automl.v1.Documen
            t.Layout.text\_segment] in document.
    """,
                # @@protoc_insertion_point(class_scope:google.cloud.automl.v1.Document.Layout)
            ),
        ),
        DESCRIPTOR=_DOCUMENT,
        __module__="google.cloud.automl_v1.proto.data_items_pb2",
        __doc__="""A structured text document e.g. a PDF.
  
  
  Attributes:
      input_config:
          An input config specifying the content of the document.
      document_text:
          The plain text version of this document.
      layout:
          Describes the layout of the document. Sorted by
          [page\_number][].
      document_dimensions:
          The dimensions of the page in the document.
      page_count:
          Number of pages in the document.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.automl.v1.Document)
    ),
)
_sym_db.RegisterMessage(Document)
_sym_db.RegisterMessage(Document.Layout)

ExamplePayload = _reflection.GeneratedProtocolMessageType(
    "ExamplePayload",
    (_message.Message,),
    dict(
        DESCRIPTOR=_EXAMPLEPAYLOAD,
        __module__="google.cloud.automl_v1.proto.data_items_pb2",
        __doc__="""Example data used for training or prediction.
  
  
  Attributes:
      payload:
          Required. The example data.
      image:
          Example image.
      text_snippet:
          Example text.
      document:
          Example document.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.automl.v1.ExamplePayload)
    ),
)
_sym_db.RegisterMessage(ExamplePayload)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
