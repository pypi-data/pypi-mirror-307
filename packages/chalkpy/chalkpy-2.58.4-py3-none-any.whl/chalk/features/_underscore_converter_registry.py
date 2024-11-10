from typing import Dict, Protocol, Type, TypeVar, Union, get_args

import pyarrow as pa

from chalk._gen.chalk.arrow.v1 import arrow_pb2 as arrow_pb
from chalk._gen.chalk.expression.v1 import expression_pb2 as expr_pb
from chalk.features import TPrimitive
from chalk.features._encoding.converter import PrimitiveFeatureConverter
from chalk.features.underscore import (
    DoubleUnderscore,
    Underscore,
    UnderscoreAttr,
    UnderscoreBinaryOp,
    UnderscoreBytesToString,
    UnderscoreCall,
    UnderscoreCast,
    UnderscoreCoalesce,
    UnderscoreCosineSimilarity,
    UnderscoreFunction,
    UnderscoreGetJSONValue,
    UnderscoreGunzip,
    UnderscoreIfThenElse,
    UnderscoreItem,
    UnderscoreMD5,
    UnderscoreRoot,
    UnderscoreSagemakerPredict,
    UnderscoreStringToBytes,
    UnderscoreTotalSeconds,
    UnderscoreUnaryOp,
    _,
)

T_contra = TypeVar("T_contra", bound=Underscore, contravariant=True)


class _UnderscoreConverter(Protocol[T_contra]):
    @staticmethod
    def to_proto(value: T_contra) -> expr_pb.LogicalExprNode:
        ...


# Stopgap until we make every underscore a UnderscoreFunction
UNDERSCORE_CONVERTER_REGISTRY: Dict[Type[Underscore], Type[_UnderscoreConverter]] = {}


def convert(value: Union[Underscore, TPrimitive, pa.DataType]) -> expr_pb.LogicalExprNode:
    if isinstance(value, Underscore):
        underscore_type = type(value)
        if underscore_type not in UNDERSCORE_CONVERTER_REGISTRY:
            raise NotImplementedError(f"No converter found for underscore type {underscore_type}")
        converter = UNDERSCORE_CONVERTER_REGISTRY[underscore_type]
        return converter.to_proto(value)
    elif isinstance(value, pa.DataType):
        return expr_pb.LogicalExprNode(
            literal_value=expr_pb.ExprLiteral(
                # HACK: Using this to store a dtype. This is not really a scalar value.
                value=arrow_pb.ScalarValue(null_value=PrimitiveFeatureConverter.convert_pa_dtype_to_proto_dtype(value))
            )
        )
    else:
        try:
            pa_dtype = pa.scalar(value).type
        except Exception as e:
            raise ValueError(f"Could not infer literal type for value `{value}`") from e
        converter = PrimitiveFeatureConverter(
            name="convert_underscore",
            is_nullable=False,
            pyarrow_dtype=pa_dtype,
        )
        return expr_pb.LogicalExprNode(
            literal_value=expr_pb.ExprLiteral(value=converter.from_primitive_to_protobuf(value))
        )


def _register(converter_cls: Type[_UnderscoreConverter]) -> None:
    """Automatically register a converter based on its generic type."""

    generic_type = get_args(converter_cls.__orig_bases__[0])[0]  # type: ignore
    if generic_type in UNDERSCORE_CONVERTER_REGISTRY:
        raise ValueError(f"Converter for {generic_type} is already registered.")
    UNDERSCORE_CONVERTER_REGISTRY[generic_type] = converter_cls


@_register
class _UnderscoreRootConverter(_UnderscoreConverter[UnderscoreRoot]):  # pyright: ignore[reportUnusedClass]
    @staticmethod
    def to_proto(value: UnderscoreRoot) -> expr_pb.LogicalExprNode:
        return expr_pb.LogicalExprNode(identifier=expr_pb.Identifier(name="_"))


@_register
class _DoubleUnderscoreConverter(_UnderscoreConverter[DoubleUnderscore]):  # pyright: ignore[reportUnusedClass]
    @staticmethod
    def to_proto(value: DoubleUnderscore) -> expr_pb.LogicalExprNode:
        return expr_pb.LogicalExprNode(identifier=expr_pb.Identifier(name="__"))


@_register
class _UnderscoreAttrConverter(_UnderscoreConverter[UnderscoreAttr]):  # pyright: ignore[reportUnusedClass]
    @staticmethod
    def to_proto(value: UnderscoreAttr) -> expr_pb.LogicalExprNode:
        return expr_pb.LogicalExprNode(
            get_attribute=expr_pb.ExprGetAttribute(
                parent=convert(value._chalk__parent),  # pyright: ignore[reportPrivateUsage]
                attribute=expr_pb.Identifier(name=value._chalk__attr),  # pyright: ignore[reportPrivateUsage]
            )
        )


@_register
class _UnderscoreItemConverter(_UnderscoreConverter[UnderscoreItem]):  # pyright: ignore[reportUnusedClass]
    @staticmethod
    def to_proto(value: UnderscoreItem) -> expr_pb.LogicalExprNode:
        raw_key = value._chalk__key  # pyright: ignore[reportPrivateUsage]
        converted_keys: list[expr_pb.LogicalExprNode] = []
        if isinstance(raw_key, tuple):
            converted_keys.extend([convert(k) for k in raw_key])
        else:
            converted_keys.append(convert(raw_key))

        return expr_pb.LogicalExprNode(
            get_subscript=expr_pb.ExprGetSubscript(
                parent=convert(value._chalk__parent),  # pyright: ignore[reportPrivateUsage]
                subscript=converted_keys,
            )
        )


@_register
class _UnderscoreCallConverter(_UnderscoreConverter[UnderscoreCall]):  # pyright: ignore[reportUnusedClass]
    @staticmethod
    def to_proto(value: UnderscoreCall) -> expr_pb.LogicalExprNode:
        args = [convert(arg) for arg in value._chalk__args]  # pyright: ignore[reportPrivateUsage]
        kwargs = {k: convert(v) for k, v in value._chalk__kwargs.items()}  # pyright: ignore[reportPrivateUsage]
        return expr_pb.LogicalExprNode(
            call=expr_pb.ExprCall(
                func=convert(value._chalk__parent),  # pyright: ignore[reportPrivateUsage]
                args=args,
                kwargs=kwargs,
            )
        )


@_register
class _UnderscoreBinaryOpConverter(_UnderscoreConverter[UnderscoreBinaryOp]):  # pyright: ignore[reportUnusedClass]
    @staticmethod
    def to_proto(value: UnderscoreBinaryOp) -> expr_pb.LogicalExprNode:
        return expr_pb.LogicalExprNode(
            call=expr_pb.ExprCall(
                func=expr_pb.LogicalExprNode(
                    identifier=expr_pb.Identifier(name=value._chalk__op)  # pyright: ignore[reportPrivateUsage]
                ),
                args=[
                    convert(value._chalk__left),  # pyright: ignore[reportPrivateUsage]
                    convert(value._chalk__right),  # pyright: ignore[reportPrivateUsage]
                ],
            )
        )


@_register
class _UnderscoreUnaryOpConverter(_UnderscoreConverter[UnderscoreUnaryOp]):  # pyright: ignore[reportUnusedClass]
    @staticmethod
    def to_proto(value: UnderscoreUnaryOp) -> expr_pb.LogicalExprNode:
        return expr_pb.LogicalExprNode(
            call=expr_pb.ExprCall(
                func=expr_pb.LogicalExprNode(
                    identifier=expr_pb.Identifier(name=value._chalk__op)  # pyright: ignore[reportPrivateUsage]
                ),
                args=[convert(value._chalk__operand)],  # pyright: ignore[reportPrivateUsage]
            )
        )


@_register
class _UnderscoreIfThenElse(_UnderscoreConverter[UnderscoreIfThenElse]):  # pyright: ignore[reportUnusedClass]
    @staticmethod
    def to_proto(value: UnderscoreIfThenElse) -> expr_pb.LogicalExprNode:
        return expr_pb.LogicalExprNode(
            call=expr_pb.ExprCall(
                func=expr_pb.LogicalExprNode(identifier=expr_pb.Identifier(name="if_then_else")),
                args=[
                    convert(value._chalk__condition),  # pyright: ignore[reportPrivateUsage]
                    convert(value._chalk__if_true),  # pyright: ignore[reportPrivateUsage]
                    convert(value._chalk__if_false),  # pyright: ignore[reportPrivateUsage]
                ],
            )
        )


@_register
class _UnderscoreMD5Converter(_UnderscoreConverter[UnderscoreMD5]):  # pyright: ignore[reportUnusedClass]
    @staticmethod
    def to_proto(value: UnderscoreMD5) -> expr_pb.LogicalExprNode:
        return expr_pb.LogicalExprNode(
            call=expr_pb.ExprCall(
                func=expr_pb.LogicalExprNode(identifier=expr_pb.Identifier(name="md5")),
                args=[convert(value._chalk__value)],  # pyright: ignore[reportPrivateUsage]
            )
        )


@_register
class _UnderscoreCoalesceConverter(_UnderscoreConverter[UnderscoreCoalesce]):  # pyright: ignore[reportUnusedClass]
    @staticmethod
    def to_proto(value: UnderscoreCoalesce) -> expr_pb.LogicalExprNode:
        return expr_pb.LogicalExprNode(
            call=expr_pb.ExprCall(
                func=expr_pb.LogicalExprNode(identifier=expr_pb.Identifier(name="coalesce")),
                args=[convert(arg) for arg in value._chalk__vals],  # pyright: ignore[reportPrivateUsage]
            )
        )


@_register
class _UnderscoreBytesToStringConverter(  # pyright: ignore[reportUnusedClass]
    _UnderscoreConverter[UnderscoreBytesToString]
):
    @staticmethod
    def to_proto(value: UnderscoreBytesToString) -> expr_pb.LogicalExprNode:
        return expr_pb.LogicalExprNode(
            call=expr_pb.ExprCall(
                func=expr_pb.LogicalExprNode(identifier=expr_pb.Identifier(name="bytes_to_string")),
                args=[
                    convert(value._chalk__value),  # pyright: ignore[reportPrivateUsage]
                    convert(value._chalk__encoding),  # pyright: ignore[reportPrivateUsage]
                ],
            )
        )


@_register
class _UnderscoreStringToBytesConverter(  # pyright: ignore[reportUnusedClass]
    _UnderscoreConverter[UnderscoreStringToBytes]
):
    @staticmethod
    def to_proto(value: UnderscoreStringToBytes) -> expr_pb.LogicalExprNode:
        return expr_pb.LogicalExprNode(
            call=expr_pb.ExprCall(
                func=expr_pb.LogicalExprNode(identifier=expr_pb.Identifier(name="string_to_bytes")),
                args=[
                    convert(value._chalk__value),  # pyright: ignore[reportPrivateUsage]
                    convert(value._chalk__encoding),  # pyright: ignore[reportPrivateUsage]
                ],
            )
        )


@_register
class _UnderscoreTotalSecondsConverter(  # pyright: ignore[reportUnusedClass]
    _UnderscoreConverter[UnderscoreTotalSeconds]
):
    @staticmethod
    def to_proto(value: UnderscoreTotalSeconds) -> expr_pb.LogicalExprNode:
        return expr_pb.LogicalExprNode(
            call=expr_pb.ExprCall(
                func=expr_pb.LogicalExprNode(identifier=expr_pb.Identifier(name="total_seconds")),
                args=[convert(value._chalk__delta)],  # pyright: ignore[reportPrivateUsage]
            )
        )


@_register
class _UnderscoreGetJSONValueConverter(  # pyright: ignore[reportUnusedClass]
    _UnderscoreConverter[UnderscoreGetJSONValue]
):
    @staticmethod
    def to_proto(value: UnderscoreGetJSONValue) -> expr_pb.LogicalExprNode:
        return expr_pb.LogicalExprNode(
            call=expr_pb.ExprCall(
                func=expr_pb.LogicalExprNode(identifier=expr_pb.Identifier(name="json_value")),
                args=[
                    convert(value._chalk__value),  # pyright: ignore[reportPrivateUsage]
                    convert(value._chalk__path),  # pyright: ignore[reportPrivateUsage]
                ],
            )
        )


@_register
class _UnderscoreGunzipConverter(_UnderscoreConverter[UnderscoreGunzip]):  # pyright: ignore[reportUnusedClass]
    @staticmethod
    def to_proto(value: UnderscoreGunzip) -> expr_pb.LogicalExprNode:
        return expr_pb.LogicalExprNode(
            call=expr_pb.ExprCall(
                func=expr_pb.LogicalExprNode(identifier=expr_pb.Identifier(name="gunzip")),
                args=[convert(value._chalk__value)],  # pyright: ignore[reportPrivateUsage]
            )
        )


@_register
class _UnderscoreCosineSimilarityConverter(  # pyright: ignore[reportUnusedClass]
    _UnderscoreConverter[UnderscoreCosineSimilarity]
):
    @staticmethod
    def to_proto(value: UnderscoreCosineSimilarity) -> expr_pb.LogicalExprNode:
        return expr_pb.LogicalExprNode(
            call=expr_pb.ExprCall(
                func=expr_pb.LogicalExprNode(identifier=expr_pb.Identifier(name="cosine_similarity")),
                args=[
                    convert(value._chalk__a),  # pyright: ignore[reportPrivateUsage]
                    convert(value._chalk__b),  # pyright: ignore[reportPrivateUsage]
                ],
            )
        )


@_register
class _UnderscoreFunctionConverter(_UnderscoreConverter[UnderscoreFunction]):  # pyright: ignore[reportUnusedClass]
    @staticmethod
    def to_proto(value: UnderscoreFunction) -> expr_pb.LogicalExprNode:
        return expr_pb.LogicalExprNode(
            call=expr_pb.ExprCall(
                func=expr_pb.LogicalExprNode(
                    identifier=expr_pb.Identifier(
                        name=value._chalk__function_name  # pyright: ignore[reportPrivateUsage]
                    )
                ),
                args=[convert(arg) for arg in value._chalk__vals],  # pyright: ignore[reportPrivateUsage]
            )
        )


@_register
class _UnderscoreSagemakerPredictConverter(  # pyright: ignore[reportUnusedClass]
    _UnderscoreConverter[UnderscoreSagemakerPredict]
):
    @staticmethod
    def to_proto(value: UnderscoreSagemakerPredict) -> expr_pb.LogicalExprNode:
        return expr_pb.LogicalExprNode(
            call=expr_pb.ExprCall(
                func=expr_pb.LogicalExprNode(identifier=expr_pb.Identifier(name="sagemaker_predict")),
                kwargs={
                    "body": convert(value._chalk__body),  # pyright: ignore[reportPrivateUsage]
                    "endpoint": convert(value._chalk__endpoint),  # pyright: ignore[reportPrivateUsage]
                    "content_type": convert(value._chalk__content_type),  # pyright: ignore[reportPrivateUsage]
                    "target_model": convert(value._chalk__target_model),  # pyright: ignore[reportPrivateUsage]
                    "target_variant": convert(value._chalk__target_variant),  # pyright: ignore[reportPrivateUsage]
                    "aws_access_key_id_override": convert(
                        value._chalk__aws_access_key_id_override  # pyright: ignore[reportPrivateUsage]
                    ),
                    "aws_secret_access_key_override": convert(
                        value._chalk__aws_secret_access_key_override  # pyright: ignore[reportPrivateUsage]
                    ),
                    "aws_session_token_override": convert(
                        value._chalk__aws_session_token_override  # pyright: ignore[reportPrivateUsage]
                    ),
                    "aws_region_override": convert(
                        value._chalk__aws_region_override  # pyright: ignore[reportPrivateUsage]
                    ),
                    "aws_profile_name_override": convert(
                        value._chalk__aws_profile_name_override  # pyright: ignore[reportPrivateUsage]
                    ),
                },
            )
        )


@_register
class _UnderscoreCastConverter(_UnderscoreConverter[UnderscoreCast]):  # pyright: ignore[reportUnusedClass]
    @staticmethod
    def to_proto(value: UnderscoreCast) -> expr_pb.LogicalExprNode:
        return expr_pb.LogicalExprNode(
            call=expr_pb.ExprCall(
                func=expr_pb.LogicalExprNode(identifier=expr_pb.Identifier(name="cast")),
                args=[
                    convert(value._chalk__value),  # pyright: ignore[reportPrivateUsage]
                    convert(value._chalk__to_type),  # pyright: ignore[reportPrivateUsage]
                ],
            )
        )
