from __future__ import annotations
from collections.abc import Callable
from datetime import datetime
from decimal import Decimal
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.array_ import fold
from ..fable_modules.fable_library.list import (FSharpList, is_empty, length, head, of_array)
from ..fable_modules.fable_library.option import value as value_10
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.seq import (to_list, delay, map, enumerate_from_functions, choose, append, singleton, empty)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import (equals, is_iterable, get_enumerator, IEnumerator, IEnumerable_1, int32_to_string)
from ..fable_modules.thoth_json_core.decode import (Getters_2__ctor_Z4BE6C149, Getters_2, IGetters, IRequiredGetter, string, Getters_2__get_Errors, map as map_1, one_of, int_1, decimal)
from ..fable_modules.thoth_json_core.encode import list_1
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1, ErrorReason_1, IDecoderHelpers_1)
from ..ROCrate.ldobject import LDObject
from .decode import Helpers_prependPath
from .encode import date_time

__A_ = TypeVar("__A_")

def generic_encoder(obj: Any=None) -> IEncodable:
    if str(type(obj)) == "<class \'str\'>":
        class ObjectExpr2861(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any], obj: Any=obj) -> Any:
                return helpers.encode_string(obj)

        return ObjectExpr2861()

    elif str(type(obj)) == "<class \'int\'>":
        class ObjectExpr2862(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any], obj: Any=obj) -> Any:
                return helpers_1.encode_signed_integral_number(obj)

        return ObjectExpr2862()

    elif str(type(obj)) == "<class \'bool\'>":
        class ObjectExpr2863(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any], obj: Any=obj) -> Any:
                return helpers_2.encode_bool(obj)

        return ObjectExpr2863()

    elif str(type(obj)) == "<class \'float\'>":
        class ObjectExpr2864(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any], obj: Any=obj) -> Any:
                return helpers_3.encode_decimal_number(obj)

        return ObjectExpr2864()

    elif isinstance(obj, datetime):
        return date_time(obj)

    elif isinstance(obj, LDObject):
        return encoder(obj)

    elif equals(obj, None):
        class ObjectExpr2865(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any], obj: Any=obj) -> Any:
                return helpers_4.encode_null()

        return ObjectExpr2865()

    elif is_iterable(obj):
        def _arrow2869(__unit: None=None, obj: Any=obj) -> IEnumerable_1[IEncodable]:
            def _arrow2866(__unit: None=None) -> IEnumerator[Any]:
                return get_enumerator(obj)

            def _arrow2867(enumerator: IEnumerator[Any]) -> bool:
                return enumerator.System_Collections_IEnumerator_MoveNext()

            def _arrow2868(enumerator_1: IEnumerator[Any]) -> Any:
                return enumerator_1.System_Collections_IEnumerator_get_Current()

            return map(generic_encoder, enumerate_from_functions(_arrow2866, _arrow2867, _arrow2868))

        return list_1(to_list(delay(_arrow2869)))

    else: 
        raise Exception("Unknown type")



def encoder(obj: LDObject) -> IEncodable:
    values: IEnumerable_1[tuple[str, IEncodable]]
    def chooser(kv: Any, obj: Any=obj) -> tuple[str, IEncodable] | None:
        l: str = kv[0].lower()
        if (l != "additionaltype") if ((l != "schematype") if (l != "id") else False) else False:
            return (kv[0], generic_encoder(kv[1]))

        else: 
            return None


    source_2: IEnumerable_1[tuple[str, IEncodable]] = choose(chooser, obj.GetProperties(True))
    def _arrow2878(__unit: None=None, obj: Any=obj) -> IEnumerable_1[tuple[str, IEncodable]]:
        def _arrow2871(__unit: None=None) -> IEncodable:
            value: str = obj.Id
            class ObjectExpr2870(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_string(value)

            return ObjectExpr2870()

        def _arrow2877(__unit: None=None) -> IEnumerable_1[tuple[str, IEncodable]]:
            def _arrow2873(__unit: None=None) -> IEncodable:
                value_1: str = obj.SchemaType
                class ObjectExpr2872(IEncodable):
                    def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                        return helpers_1.encode_string(value_1)

                return ObjectExpr2872()

            def _arrow2876(__unit: None=None) -> IEnumerable_1[tuple[str, IEncodable]]:
                def _arrow2875(__unit: None=None) -> IEncodable:
                    value_2: str = value_10(obj.AdditionalType)
                    class ObjectExpr2874(IEncodable):
                        def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                            return helpers_2.encode_string(value_2)

                    return ObjectExpr2874()

                return singleton(("additionalType", _arrow2875())) if (obj.AdditionalType is not None) else empty()

            return append(singleton(("@type", _arrow2873())), delay(_arrow2876))

        return append(singleton(("@id", _arrow2871())), delay(_arrow2877))

    values = append(to_list(delay(_arrow2878)), source_2)
    class ObjectExpr2883(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any], obj: Any=obj) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_3))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_3.encode_object(arg)

    return ObjectExpr2883()


def get_decoder(expect_object: bool) -> Decoder_1[Any]:
    def decode(expect_object_1: bool, expect_object: Any=expect_object) -> Decoder_1[Any]:
        class ObjectExpr2887(Decoder_1[LDObject]):
            def Decode(self, helpers: IDecoderHelpers_1[Any], value: Any, expect_object_1: Any=expect_object_1) -> FSharpResult_2[LDObject, tuple[str, ErrorReason_1[__A_]]]:
                if helpers.is_object(value):
                    getters: Getters_2[__A_, Any] = Getters_2__ctor_Z4BE6C149(helpers, value)
                    properties: IEnumerable_1[str] = helpers.get_properties(value)
                    result: LDObject
                    get: IGetters = getters
                    t: str
                    object_arg: IRequiredGetter = get.Required
                    t = object_arg.Field("@type", string)
                    def _arrow2885(__unit: None=None) -> str:
                        object_arg_1: IRequiredGetter = get.Required
                        return object_arg_1.Field("@id", string)

                    o: LDObject = LDObject(_arrow2885(), t)
                    with get_enumerator(properties) as enumerator:
                        while enumerator.System_Collections_IEnumerator_MoveNext():
                            property: str = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                            if (property != "@type") if (property != "@id") else False:
                                def _arrow2886(__unit: None=None) -> Any:
                                    arg_5: Decoder_1[Any] = decode(False)
                                    object_arg_2: IRequiredGetter = get.Required
                                    return object_arg_2.Field(property, arg_5)

                                o.SetProperty(property, _arrow2886())

                    result = o
                    match_value: FSharpList[tuple[str, ErrorReason_1[__A_]]] = Getters_2__get_Errors(getters)
                    if not is_empty(match_value):
                        errors: FSharpList[tuple[str, ErrorReason_1[__A_]]] = match_value
                        return FSharpResult_2(1, ("", ErrorReason_1(7, errors))) if (length(errors) > 1) else FSharpResult_2(1, head(match_value))

                    else: 
                        return FSharpResult_2(0, result)


                else: 
                    return FSharpResult_2(1, ("", ErrorReason_1(0, "an object", value)))


        decode_object: Decoder_1[LDObject] = ObjectExpr2887()
        class ObjectExpr2889(Decoder_1[Array[Any]]):
            def Decode(self, helpers_1: IDecoderHelpers_1[Any], value_1: Any, expect_object_1: Any=expect_object_1) -> FSharpResult_2[Array[Any], tuple[str, ErrorReason_1[__A_]]]:
                if helpers_1.is_array(value_1):
                    i: int = -1
                    def folder(acc: FSharpResult_2[Array[Any], tuple[str, ErrorReason_1[__A_]]], value_2: __A_) -> FSharpResult_2[Array[Any], tuple[str, ErrorReason_1[__A_]]]:
                        nonlocal i
                        i = (i + 1) or 0
                        if acc.tag == 0:
                            acc_1: Array[Any] = acc.fields[0]
                            match_value_1: FSharpResult_2[Any, tuple[str, ErrorReason_1[__A_]]]
                            copy_of_struct: Decoder_1[Any] = decode(False)
                            match_value_1 = copy_of_struct.Decode(helpers_1, value_2)
                            if match_value_1.tag == 0:
                                (acc_1.append(match_value_1.fields[0]))
                                return FSharpResult_2(0, acc_1)

                            else: 
                                def _arrow2888(__unit: None=None, acc: Any=acc, value_2: Any=value_2) -> tuple[str, ErrorReason_1[__A_]]:
                                    tupled_arg: tuple[str, ErrorReason_1[__A_]] = match_value_1.fields[0]
                                    return Helpers_prependPath((".[" + int32_to_string(i)) + "]", tupled_arg[0], tupled_arg[1])

                                return FSharpResult_2(1, _arrow2888())


                        else: 
                            return acc


                    return fold(folder, FSharpResult_2(0, []), helpers_1.as_array(value_1))

                else: 
                    return FSharpResult_2(1, ("", ErrorReason_1(0, "an array", value_1)))


        resize_array: Decoder_1[Array[Any]] = ObjectExpr2889()
        if expect_object_1:
            def _arrow2890(value_4: LDObject, expect_object_1: Any=expect_object_1) -> Any:
                return value_4

            return map_1(_arrow2890, decode_object)

        else: 
            def _arrow2892(value_5: LDObject, expect_object_1: Any=expect_object_1) -> Any:
                return value_5

            def _arrow2893(value_6: Array[Any], expect_object_1: Any=expect_object_1) -> Any:
                return value_6

            def _arrow2894(value_7: str, expect_object_1: Any=expect_object_1) -> Any:
                return value_7

            def _arrow2895(value_8: int, expect_object_1: Any=expect_object_1) -> Any:
                return value_8

            def _arrow2896(value_9: Decimal, expect_object_1: Any=expect_object_1) -> Any:
                return value_9

            return one_of(of_array([map_1(_arrow2892, decode_object), map_1(_arrow2893, resize_array), map_1(_arrow2894, string), map_1(_arrow2895, int_1), map_1(_arrow2896, decimal)]))


    return decode(expect_object)


def _arrow2897(value: Any=None) -> LDObject:
    return value


decoder: Decoder_1[LDObject] = map_1(_arrow2897, get_decoder(True))

generic_decoder: Decoder_1[Any] = get_decoder(False)

__all__ = ["generic_encoder", "encoder", "get_decoder", "decoder", "generic_decoder"]

