from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.list import of_array
from ...fable_modules.thoth_json_core.decode import (one_of, map, int_1, float_1, string)
from ...fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.value import Value
from ..ontology_annotation import (OntologyAnnotation_ISAJson_encoder, OntologyAnnotation_ISAJson_decoder)

def encoder(id_map: Any | None, value: Value) -> IEncodable:
    if value.tag == 1:
        class ObjectExpr1961(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any], id_map: Any=id_map, value: Any=value) -> Any:
                return helpers_1.encode_signed_integral_number(value.fields[0])

        return ObjectExpr1961()

    elif value.tag == 3:
        class ObjectExpr1962(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any], id_map: Any=id_map, value: Any=value) -> Any:
                return helpers_2.encode_string(value.fields[0])

        return ObjectExpr1962()

    elif value.tag == 0:
        return OntologyAnnotation_ISAJson_encoder(id_map, value.fields[0])

    else: 
        class ObjectExpr1963(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any], id_map: Any=id_map, value: Any=value) -> Any:
                return helpers.encode_decimal_number(value.fields[0])

        return ObjectExpr1963()



def _arrow1965(Item: int) -> Value:
    return Value(1, Item)


def _arrow1966(Item_1: float) -> Value:
    return Value(2, Item_1)


def _arrow1967(Item_2: OntologyAnnotation) -> Value:
    return Value(0, Item_2)


def _arrow1968(Item_3: str) -> Value:
    return Value(3, Item_3)


decoder: Decoder_1[Value] = one_of(of_array([map(_arrow1965, int_1), map(_arrow1966, float_1), map(_arrow1967, OntologyAnnotation_ISAJson_decoder), map(_arrow1968, string)]))

__all__ = ["encoder", "decoder"]

