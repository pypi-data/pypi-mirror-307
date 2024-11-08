from __future__ import annotations
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ..fable_modules.fable_library.option import map
from ..fable_modules.fable_library.seq import map as map_1
from ..fable_modules.fable_library.string_ import replace
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import IEnumerable_1
from ..fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, resize_array, IGetters)
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Core.comment import Comment
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.publication import Publication
from .comment import (encoder as encoder_1, decoder as decoder_2, ROCrate_encoderDisambiguatingDescription, ROCrate_decoderDisambiguatingDescription, ISAJson_encoder as ISAJson_encoder_1)
from .context.rocrate.isa_publication_context import context_jsonvalue
from .decode import (Decode_uri, Decode_noAdditionalProperties)
from .encode import (try_include, try_include_seq)
from .ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder, OntologyAnnotation_ROCrate_encoderDefinedTerm, OntologyAnnotation_ROCrate_decoderDefinedTerm)
from .person import (ROCrate_encodeAuthorListString, ROCrate_decodeAuthorListString)

__A_ = TypeVar("__A_")

def encoder(oa: Publication) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow1972(value: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr1971(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr1971()

    def _arrow1974(value_2: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr1973(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_2)

        return ObjectExpr1973()

    def _arrow1976(value_4: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr1975(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_4)

        return ObjectExpr1975()

    def _arrow1978(value_6: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr1977(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_6)

        return ObjectExpr1977()

    def _arrow1979(oa_1: OntologyAnnotation, oa: Any=oa) -> IEncodable:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow1980(comment: Comment, oa: Any=oa) -> IEncodable:
        return encoder_1(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("pubMedID", _arrow1972, oa.PubMedID), try_include("doi", _arrow1974, oa.DOI), try_include("authorList", _arrow1976, oa.Authors), try_include("title", _arrow1978, oa.Title), try_include("status", _arrow1979, oa.Status), try_include_seq("comments", _arrow1980, oa.Comments)]))
    class ObjectExpr1981(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_4))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_4.encode_object(arg)

    return ObjectExpr1981()


def _arrow1994(get: IGetters) -> Publication:
    def _arrow1984(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("pubMedID", Decode_uri)

    def _arrow1985(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("doi", string)

    def _arrow1986(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("authorList", string)

    def _arrow1987(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("title", string)

    def _arrow1990(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("status", OntologyAnnotation_decoder)

    def _arrow1991(__unit: None=None) -> Array[Comment] | None:
        arg_11: Decoder_1[Array[Comment]] = resize_array(decoder_2)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("comments", arg_11)

    return Publication(_arrow1984(), _arrow1985(), _arrow1986(), _arrow1987(), _arrow1990(), _arrow1991())


decoder: Decoder_1[Publication] = object(_arrow1994)

def ROCrate_genID(p: Publication) -> str:
    match_value: str | None = p.DOI
    if match_value is None:
        match_value_1: str | None = p.PubMedID
        if match_value_1 is None:
            match_value_2: str | None = p.Title
            if match_value_2 is None:
                return "#EmptyPublication"

            else: 
                return "#Pub_" + replace(match_value_2, " ", "_")


        else: 
            return match_value_1


    else: 
        return match_value



def ROCrate_encoder(oa: Publication) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2002(__unit: None=None, oa: Any=oa) -> IEncodable:
        value: str = ROCrate_genID(oa)
        class ObjectExpr2001(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2001()

    class ObjectExpr2004(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            return helpers_1.encode_string("Publication")

    def _arrow2007(value_2: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2006(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_2)

        return ObjectExpr2006()

    def _arrow2011(value_4: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2010(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_4)

        return ObjectExpr2010()

    def _arrow2012(author_list: str, oa: Any=oa) -> IEncodable:
        return ROCrate_encodeAuthorListString(author_list)

    def _arrow2014(value_6: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2013(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_6)

        return ObjectExpr2013()

    def _arrow2015(oa_1: OntologyAnnotation, oa: Any=oa) -> IEncodable:
        return OntologyAnnotation_ROCrate_encoderDefinedTerm(oa_1)

    def _arrow2016(comment: Comment, oa: Any=oa) -> IEncodable:
        return ROCrate_encoderDisambiguatingDescription(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow2002()), ("@type", ObjectExpr2004()), try_include("pubMedID", _arrow2007, oa.PubMedID), try_include("doi", _arrow2011, oa.DOI), try_include("authorList", _arrow2012, oa.Authors), try_include("title", _arrow2014, oa.Title), try_include("status", _arrow2015, oa.Status), try_include_seq("comments", _arrow2016, oa.Comments), ("@context", context_jsonvalue)]))
    class ObjectExpr2017(IEncodable):
        def Encode(self, helpers_5: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_5))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_5.encode_object(arg)

    return ObjectExpr2017()


def _arrow2024(get: IGetters) -> Publication:
    def _arrow2018(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("pubMedID", Decode_uri)

    def _arrow2019(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("doi", string)

    def _arrow2020(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("authorList", ROCrate_decodeAuthorListString)

    def _arrow2021(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("title", string)

    def _arrow2022(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("status", OntologyAnnotation_ROCrate_decoderDefinedTerm)

    def _arrow2023(__unit: None=None) -> Array[Comment] | None:
        arg_11: Decoder_1[Array[Comment]] = resize_array(ROCrate_decoderDisambiguatingDescription)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("comments", arg_11)

    return Publication(_arrow2018(), _arrow2019(), _arrow2020(), _arrow2021(), _arrow2022(), _arrow2023())


ROCrate_decoder: Decoder_1[Publication] = object(_arrow2024)

def ISAJson_encoder(id_map: Any | None, oa: Publication) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], id_map: Any=id_map, oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2028(value: str, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        class ObjectExpr2027(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2027()

    def _arrow2030(value_2: str, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        class ObjectExpr2029(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_2)

        return ObjectExpr2029()

    def _arrow2032(value_4: str, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        class ObjectExpr2031(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_4)

        return ObjectExpr2031()

    def _arrow2034(value_6: str, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        class ObjectExpr2033(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_6)

        return ObjectExpr2033()

    def _arrow2035(oa_1: OntologyAnnotation, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow2036(comment: Comment, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        return ISAJson_encoder_1(id_map, comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("pubMedID", _arrow2028, oa.PubMedID), try_include("doi", _arrow2030, oa.DOI), try_include("authorList", _arrow2032, oa.Authors), try_include("title", _arrow2034, oa.Title), try_include("status", _arrow2035, oa.Status), try_include_seq("comments", _arrow2036, oa.Comments)]))
    class ObjectExpr2037(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any], id_map: Any=id_map, oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_4))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_4.encode_object(arg)

    return ObjectExpr2037()


ISAJson_allowedFields: FSharpList[str] = of_array(["pubMedID", "doi", "authorList", "title", "status", "comments"])

ISAJson_decoder: Decoder_1[Publication] = Decode_noAdditionalProperties(ISAJson_allowedFields, decoder)

__all__ = ["encoder", "decoder", "ROCrate_genID", "ROCrate_encoder", "ROCrate_decoder", "ISAJson_encoder", "ISAJson_allowedFields", "ISAJson_decoder"]

