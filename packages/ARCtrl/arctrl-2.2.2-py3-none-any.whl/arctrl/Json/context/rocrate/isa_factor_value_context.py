from __future__ import annotations
from dataclasses import dataclass
from typing import (Any, TypeVar)
from ....fable_modules.fable_library.reflection import (TypeInfo, string_type, record_type)
from ....fable_modules.fable_library.seq import map
from ....fable_modules.fable_library.types import Record
from ....fable_modules.fable_library.util import (to_enumerable, IEnumerable_1)
from ....fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1)

__A_ = TypeVar("__A_")

def _expr1452() -> TypeInfo:
    return record_type("ARCtrl.Json.ROCrateContext.FactorValue.IContext", [], IContext, lambda: [("sdo", string_type), ("arc", string_type), ("FactorValue", string_type), ("ArcFactorValue", string_type), ("category", string_type), ("value", string_type), ("unit", string_type)])


@dataclass(eq = False, repr = False, slots = True)
class IContext(Record):
    sdo: str
    arc: str
    FactorValue: str
    ArcFactorValue: str
    category: str
    value: str
    unit: str

IContext_reflection = _expr1452

def _arrow1467(__unit: None=None) -> IEncodable:
    class ObjectExpr1454(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
            return helpers.encode_string("http://schema.org/")

    class ObjectExpr1456(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
            return helpers_1.encode_string("sdo:PropertyValue")

    class ObjectExpr1457(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
            return helpers_2.encode_string("sdo:additionalType")

    class ObjectExpr1458(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
            return helpers_3.encode_string("sdo:name")

    class ObjectExpr1459(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
            return helpers_4.encode_string("sdo:alternateName")

    class ObjectExpr1460(IEncodable):
        def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
            return helpers_5.encode_string("sdo:propertyID")

    class ObjectExpr1461(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
            return helpers_6.encode_string("sdo:value")

    class ObjectExpr1462(IEncodable):
        def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
            return helpers_7.encode_string("sdo:valueReference")

    class ObjectExpr1463(IEncodable):
        def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
            return helpers_8.encode_string("sdo:unitText")

    class ObjectExpr1464(IEncodable):
        def Encode(self, helpers_9: IEncoderHelpers_1[Any]) -> Any:
            return helpers_9.encode_string("sdo:unitCode")

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("sdo", ObjectExpr1454()), ("FactorValue", ObjectExpr1456()), ("additionalType", ObjectExpr1457()), ("category", ObjectExpr1458()), ("categoryName", ObjectExpr1459()), ("categoryCode", ObjectExpr1460()), ("value", ObjectExpr1461()), ("valueCode", ObjectExpr1462()), ("unit", ObjectExpr1463()), ("unitCode", ObjectExpr1464())])
    class ObjectExpr1466(IEncodable):
        def Encode(self, helpers_10: IEncoderHelpers_1[Any]) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_10))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_10.encode_object(arg)

    return ObjectExpr1466()


context_jsonvalue: IEncodable = _arrow1467()

__all__ = ["IContext_reflection", "context_jsonvalue"]

