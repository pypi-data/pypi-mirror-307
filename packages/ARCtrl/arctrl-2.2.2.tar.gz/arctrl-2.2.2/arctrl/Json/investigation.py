from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList, unzip, empty)
from ..fable_modules.fable_library.option import (map, default_arg)
from ..fable_modules.fable_library.seq import (map as map_1, concat)
from ..fable_modules.fable_library.seq2 import distinct_by
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import (IEnumerable_1, string_hash)
from ..fable_modules.thoth_json_core.decode import (object, IRequiredGetter, string, IOptionalGetter, resize_array, IGetters, list_1 as list_1_1)
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Core.arc_types import (ArcAssay, ArcStudy, ArcInvestigation)
from ..Core.comment import Comment
from ..Core.Helper.identifier import create_missing_identifier
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.ontology_source_reference import OntologySourceReference
from ..Core.person import Person
from ..Core.publication import Publication
from ..Core.Table.composite_cell import CompositeCell
from .assay import (encoder as encoder_4, decoder as decoder_6, encoder_compressed as encoder_compressed_1, decoder_compressed as decoder_compressed_1)
from .comment import (encoder as encoder_6, decoder as decoder_8, ROCrate_encoder as ROCrate_encoder_5, ROCrate_decoder as ROCrate_decoder_5, ISAJson_encoder as ISAJson_encoder_5, ISAJson_decoder as ISAJson_decoder_5)
from .context.rocrate.isa_investigation_context import context_jsonvalue
from .context.rocrate.rocrate_context import (conforms_to_jsonvalue, context_jsonvalue as context_jsonvalue_1)
from .decode import Decode_objectNoAdditionalProperties
from .encode import (try_include, try_include_seq)
from .ontology_source_reference import (encoder as encoder_1, decoder as decoder_3, ROCrate_encoder as ROCrate_encoder_1, ROCrate_decoder as ROCrate_decoder_2, ISAJson_encoder as ISAJson_encoder_1, ISAJson_decoder as ISAJson_decoder_2)
from .person import (encoder as encoder_3, decoder as decoder_5, ROCrate_encoder as ROCrate_encoder_3, ROCrate_decoder as ROCrate_decoder_4, ISAJson_encoder as ISAJson_encoder_3, ISAJson_decoder as ISAJson_decoder_4)
from .publication import (encoder as encoder_2, decoder as decoder_4, ROCrate_encoder as ROCrate_encoder_2, ROCrate_decoder as ROCrate_decoder_3, ISAJson_encoder as ISAJson_encoder_2, ISAJson_decoder as ISAJson_decoder_3)
from .study import (encoder as encoder_5, decoder as decoder_7, encoder_compressed as encoder_compressed_2, decoder_compressed as decoder_compressed_2, ROCrate_encoder as ROCrate_encoder_4, ROCrate_decoder as ROCrate_decoder_1, ISAJson_encoder as ISAJson_encoder_4, ISAJson_decoder as ISAJson_decoder_1)

__A_ = TypeVar("__A_")

def encoder(inv: ArcInvestigation) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], inv: Any=inv) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2929(__unit: None=None, inv: Any=inv) -> IEncodable:
        value: str = inv.Identifier
        class ObjectExpr2928(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2928()

    def _arrow2931(value_1: str, inv: Any=inv) -> IEncodable:
        class ObjectExpr2930(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_1)

        return ObjectExpr2930()

    def _arrow2933(value_3: str, inv: Any=inv) -> IEncodable:
        class ObjectExpr2932(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_3)

        return ObjectExpr2932()

    def _arrow2935(value_5: str, inv: Any=inv) -> IEncodable:
        class ObjectExpr2934(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_5)

        return ObjectExpr2934()

    def _arrow2937(value_7: str, inv: Any=inv) -> IEncodable:
        class ObjectExpr2936(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_7)

        return ObjectExpr2936()

    def _arrow2938(osr: OntologySourceReference, inv: Any=inv) -> IEncodable:
        return encoder_1(osr)

    def _arrow2939(oa: Publication, inv: Any=inv) -> IEncodable:
        return encoder_2(oa)

    def _arrow2940(person: Person, inv: Any=inv) -> IEncodable:
        return encoder_3(person)

    def _arrow2941(assay: ArcAssay, inv: Any=inv) -> IEncodable:
        return encoder_4(assay)

    def _arrow2942(study: ArcStudy, inv: Any=inv) -> IEncodable:
        return encoder_5(study)

    def _arrow2944(value_9: str, inv: Any=inv) -> IEncodable:
        class ObjectExpr2943(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_9)

        return ObjectExpr2943()

    def _arrow2945(comment: Comment, inv: Any=inv) -> IEncodable:
        return encoder_6(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("Identifier", _arrow2929()), try_include("Title", _arrow2931, inv.Title), try_include("Description", _arrow2933, inv.Description), try_include("SubmissionDate", _arrow2935, inv.SubmissionDate), try_include("PublicReleaseDate", _arrow2937, inv.PublicReleaseDate), try_include_seq("OntologySourceReferences", _arrow2938, inv.OntologySourceReferences), try_include_seq("Publications", _arrow2939, inv.Publications), try_include_seq("Contacts", _arrow2940, inv.Contacts), try_include_seq("Assays", _arrow2941, inv.Assays), try_include_seq("Studies", _arrow2942, inv.Studies), try_include_seq("RegisteredStudyIdentifiers", _arrow2944, inv.RegisteredStudyIdentifiers), try_include_seq("Comments", _arrow2945, inv.Comments)]))
    class ObjectExpr2946(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any], inv: Any=inv) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_6))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_6.encode_object(arg)

    return ObjectExpr2946()


def _arrow2959(get: IGetters) -> ArcInvestigation:
    def _arrow2947(__unit: None=None) -> str:
        object_arg: IRequiredGetter = get.Required
        return object_arg.Field("Identifier", string)

    def _arrow2948(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("Title", string)

    def _arrow2949(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("Description", string)

    def _arrow2950(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("SubmissionDate", string)

    def _arrow2951(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("PublicReleaseDate", string)

    def _arrow2952(__unit: None=None) -> Array[OntologySourceReference] | None:
        arg_11: Decoder_1[Array[OntologySourceReference]] = resize_array(decoder_3)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("OntologySourceReferences", arg_11)

    def _arrow2953(__unit: None=None) -> Array[Publication] | None:
        arg_13: Decoder_1[Array[Publication]] = resize_array(decoder_4)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("Publications", arg_13)

    def _arrow2954(__unit: None=None) -> Array[Person] | None:
        arg_15: Decoder_1[Array[Person]] = resize_array(decoder_5)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("Contacts", arg_15)

    def _arrow2955(__unit: None=None) -> Array[ArcAssay] | None:
        arg_17: Decoder_1[Array[ArcAssay]] = resize_array(decoder_6)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("Assays", arg_17)

    def _arrow2956(__unit: None=None) -> Array[ArcStudy] | None:
        arg_19: Decoder_1[Array[ArcStudy]] = resize_array(decoder_7)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("Studies", arg_19)

    def _arrow2957(__unit: None=None) -> Array[str] | None:
        arg_21: Decoder_1[Array[str]] = resize_array(string)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("RegisteredStudyIdentifiers", arg_21)

    def _arrow2958(__unit: None=None) -> Array[Comment] | None:
        arg_23: Decoder_1[Array[Comment]] = resize_array(decoder_8)
        object_arg_11: IOptionalGetter = get.Optional
        return object_arg_11.Field("Comments", arg_23)

    return ArcInvestigation(_arrow2947(), _arrow2948(), _arrow2949(), _arrow2950(), _arrow2951(), _arrow2952(), _arrow2953(), _arrow2954(), _arrow2955(), _arrow2956(), _arrow2957(), _arrow2958())


decoder: Decoder_1[ArcInvestigation] = object(_arrow2959)

def encoder_compressed(string_table: Any, oa_table: Any, cell_table: Any, inv: ArcInvestigation) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2963(__unit: None=None, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        value: str = inv.Identifier
        class ObjectExpr2962(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2962()

    def _arrow2965(value_1: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        class ObjectExpr2964(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_1)

        return ObjectExpr2964()

    def _arrow2967(value_3: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        class ObjectExpr2966(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_3)

        return ObjectExpr2966()

    def _arrow2969(value_5: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        class ObjectExpr2968(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_5)

        return ObjectExpr2968()

    def _arrow2971(value_7: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        class ObjectExpr2970(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_7)

        return ObjectExpr2970()

    def _arrow2972(osr: OntologySourceReference, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        return encoder_1(osr)

    def _arrow2973(oa: Publication, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        return encoder_2(oa)

    def _arrow2974(person: Person, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        return encoder_3(person)

    def _arrow2975(assay: ArcAssay, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        return encoder_compressed_1(string_table, oa_table, cell_table, assay)

    def _arrow2976(study: ArcStudy, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        return encoder_compressed_2(string_table, oa_table, cell_table, study)

    def _arrow2978(value_9: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        class ObjectExpr2977(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_9)

        return ObjectExpr2977()

    def _arrow2979(comment: Comment, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        return encoder_6(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("Identifier", _arrow2963()), try_include("Title", _arrow2965, inv.Title), try_include("Description", _arrow2967, inv.Description), try_include("SubmissionDate", _arrow2969, inv.SubmissionDate), try_include("PublicReleaseDate", _arrow2971, inv.PublicReleaseDate), try_include_seq("OntologySourceReferences", _arrow2972, inv.OntologySourceReferences), try_include_seq("Publications", _arrow2973, inv.Publications), try_include_seq("Contacts", _arrow2974, inv.Contacts), try_include_seq("Assays", _arrow2975, inv.Assays), try_include_seq("Studies", _arrow2976, inv.Studies), try_include_seq("RegisteredStudyIdentifiers", _arrow2978, inv.RegisteredStudyIdentifiers), try_include_seq("Comments", _arrow2979, inv.Comments)]))
    class ObjectExpr2980(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any], string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_6))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_6.encode_object(arg)

    return ObjectExpr2980()


def decoder_compressed(string_table: Array[str], oa_table: Array[OntologyAnnotation], cell_table: Array[CompositeCell]) -> Decoder_1[ArcInvestigation]:
    def _arrow2993(get: IGetters, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table) -> ArcInvestigation:
        def _arrow2981(__unit: None=None) -> str:
            object_arg: IRequiredGetter = get.Required
            return object_arg.Field("Identifier", string)

        def _arrow2982(__unit: None=None) -> str | None:
            object_arg_1: IOptionalGetter = get.Optional
            return object_arg_1.Field("Title", string)

        def _arrow2983(__unit: None=None) -> str | None:
            object_arg_2: IOptionalGetter = get.Optional
            return object_arg_2.Field("Description", string)

        def _arrow2984(__unit: None=None) -> str | None:
            object_arg_3: IOptionalGetter = get.Optional
            return object_arg_3.Field("SubmissionDate", string)

        def _arrow2985(__unit: None=None) -> str | None:
            object_arg_4: IOptionalGetter = get.Optional
            return object_arg_4.Field("PublicReleaseDate", string)

        def _arrow2986(__unit: None=None) -> Array[OntologySourceReference] | None:
            arg_11: Decoder_1[Array[OntologySourceReference]] = resize_array(decoder_3)
            object_arg_5: IOptionalGetter = get.Optional
            return object_arg_5.Field("OntologySourceReferences", arg_11)

        def _arrow2987(__unit: None=None) -> Array[Publication] | None:
            arg_13: Decoder_1[Array[Publication]] = resize_array(decoder_4)
            object_arg_6: IOptionalGetter = get.Optional
            return object_arg_6.Field("Publications", arg_13)

        def _arrow2988(__unit: None=None) -> Array[Person] | None:
            arg_15: Decoder_1[Array[Person]] = resize_array(decoder_5)
            object_arg_7: IOptionalGetter = get.Optional
            return object_arg_7.Field("Contacts", arg_15)

        def _arrow2989(__unit: None=None) -> Array[ArcAssay] | None:
            arg_17: Decoder_1[Array[ArcAssay]] = resize_array(decoder_compressed_1(string_table, oa_table, cell_table))
            object_arg_8: IOptionalGetter = get.Optional
            return object_arg_8.Field("Assays", arg_17)

        def _arrow2990(__unit: None=None) -> Array[ArcStudy] | None:
            arg_19: Decoder_1[Array[ArcStudy]] = resize_array(decoder_compressed_2(string_table, oa_table, cell_table))
            object_arg_9: IOptionalGetter = get.Optional
            return object_arg_9.Field("Studies", arg_19)

        def _arrow2991(__unit: None=None) -> Array[str] | None:
            arg_21: Decoder_1[Array[str]] = resize_array(string)
            object_arg_10: IOptionalGetter = get.Optional
            return object_arg_10.Field("RegisteredStudyIdentifiers", arg_21)

        def _arrow2992(__unit: None=None) -> Array[Comment] | None:
            arg_23: Decoder_1[Array[Comment]] = resize_array(decoder_8)
            object_arg_11: IOptionalGetter = get.Optional
            return object_arg_11.Field("Comments", arg_23)

        return ArcInvestigation(_arrow2981(), _arrow2982(), _arrow2983(), _arrow2984(), _arrow2985(), _arrow2986(), _arrow2987(), _arrow2988(), _arrow2989(), _arrow2990(), _arrow2991(), _arrow2992())

    return object(_arrow2993)


def ROCrate_genID(i: ArcInvestigation) -> str:
    return "./"


def ROCrate_encoder(oa: ArcInvestigation) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2997(__unit: None=None, oa: Any=oa) -> IEncodable:
        value: str = ROCrate_genID(oa)
        class ObjectExpr2996(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2996()

    class ObjectExpr2998(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            return helpers_1.encode_string("Investigation")

    class ObjectExpr2999(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            return helpers_2.encode_string("Investigation")

    def _arrow3001(__unit: None=None, oa: Any=oa) -> IEncodable:
        value_3: str = oa.Identifier
        class ObjectExpr3000(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_3)

        return ObjectExpr3000()

    def _arrow3003(__unit: None=None, oa: Any=oa) -> IEncodable:
        value_4: str = ArcInvestigation.FileName()
        class ObjectExpr3002(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_4)

        return ObjectExpr3002()

    def _arrow3005(value_5: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr3004(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_5)

        return ObjectExpr3004()

    def _arrow3007(value_7: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr3006(IEncodable):
            def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
                return helpers_6.encode_string(value_7)

        return ObjectExpr3006()

    def _arrow3009(value_9: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr3008(IEncodable):
            def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
                return helpers_7.encode_string(value_9)

        return ObjectExpr3008()

    def _arrow3011(value_11: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr3010(IEncodable):
            def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
                return helpers_8.encode_string(value_11)

        return ObjectExpr3010()

    def _arrow3012(osr: OntologySourceReference, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_1(osr)

    def _arrow3013(oa_1: Publication, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_2(oa_1)

    def _arrow3014(oa_2: Person, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_3(oa_2)

    def _arrow3015(s: ArcStudy, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_4(None, s)

    def _arrow3016(comment: Comment, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_5(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow2997()), ("@type", ObjectExpr2998()), ("additionalType", ObjectExpr2999()), ("identifier", _arrow3001()), ("filename", _arrow3003()), try_include("title", _arrow3005, oa.Title), try_include("description", _arrow3007, oa.Description), try_include("submissionDate", _arrow3009, oa.SubmissionDate), try_include("publicReleaseDate", _arrow3011, oa.PublicReleaseDate), try_include_seq("ontologySourceReferences", _arrow3012, oa.OntologySourceReferences), try_include_seq("publications", _arrow3013, oa.Publications), try_include_seq("people", _arrow3014, oa.Contacts), try_include_seq("studies", _arrow3015, oa.Studies), try_include_seq("comments", _arrow3016, oa.Comments), ("@context", context_jsonvalue)]))
    class ObjectExpr3017(IEncodable):
        def Encode(self, helpers_9: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_9))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_9.encode_object(arg)

    return ObjectExpr3017()


def _arrow3029(get: IGetters) -> ArcInvestigation:
    identifier: str
    match_value: str | None
    object_arg: IOptionalGetter = get.Optional
    match_value = object_arg.Field("identifier", string)
    identifier = create_missing_identifier() if (match_value is None) else match_value
    def _arrow3018(__unit: None=None) -> FSharpList[tuple[ArcStudy, FSharpList[ArcAssay]]] | None:
        arg_3: Decoder_1[FSharpList[tuple[ArcStudy, FSharpList[ArcAssay]]]] = list_1_1(ROCrate_decoder_1)
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("studies", arg_3)

    pattern_input: tuple[FSharpList[ArcStudy], FSharpList[FSharpList[ArcAssay]]] = unzip(default_arg(_arrow3018(), empty()))
    studies_raw: FSharpList[ArcStudy] = pattern_input[0]
    def projection(a: ArcAssay) -> str:
        return a.Identifier

    class ObjectExpr3020:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow3019(x: str, y: str) -> bool:
                return x == y

            return _arrow3019

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    assays: Array[ArcAssay] = list(distinct_by(projection, concat(pattern_input[1]), ObjectExpr3020()))
    studies: Array[ArcStudy] = list(studies_raw)
    def mapping(a_1: ArcStudy) -> str:
        return a_1.Identifier

    study_identifiers: Array[str] = list(map_1(mapping, studies_raw))
    def _arrow3021(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("title", string)

    def _arrow3022(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("description", string)

    def _arrow3023(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("submissionDate", string)

    def _arrow3024(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("publicReleaseDate", string)

    def _arrow3025(__unit: None=None) -> Array[OntologySourceReference] | None:
        arg_13: Decoder_1[Array[OntologySourceReference]] = resize_array(ROCrate_decoder_2)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("ontologySourceReferences", arg_13)

    def _arrow3026(__unit: None=None) -> Array[Publication] | None:
        arg_15: Decoder_1[Array[Publication]] = resize_array(ROCrate_decoder_3)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("publications", arg_15)

    def _arrow3027(__unit: None=None) -> Array[Person] | None:
        arg_17: Decoder_1[Array[Person]] = resize_array(ROCrate_decoder_4)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("people", arg_17)

    def _arrow3028(__unit: None=None) -> Array[Comment] | None:
        arg_19: Decoder_1[Array[Comment]] = resize_array(ROCrate_decoder_5)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("comments", arg_19)

    return ArcInvestigation(identifier, _arrow3021(), _arrow3022(), _arrow3023(), _arrow3024(), _arrow3025(), _arrow3026(), _arrow3027(), assays, studies, study_identifiers, _arrow3028())


ROCrate_decoder: Decoder_1[ArcInvestigation] = object(_arrow3029)

def ROCrate_encodeRoCrate(oa: ArcInvestigation) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow3033(value: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr3032(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr3032()

    def _arrow3035(value_2: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr3034(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_2)

        return ObjectExpr3034()

    def _arrow3036(oa_1: ArcInvestigation, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder(oa_1)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@type", _arrow3033, "CreativeWork"), try_include("@id", _arrow3035, "ro-crate-metadata.json"), try_include("about", _arrow3036, oa), ("conformsTo", conforms_to_jsonvalue), ("@context", context_jsonvalue_1)]))
    class ObjectExpr3037(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_2))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_2.encode_object(arg)

    return ObjectExpr3037()


ISAJson_allowedFields: FSharpList[str] = of_array(["@id", "filename", "identifier", "title", "description", "submissionDate", "publicReleaseDate", "ontologySourceReferences", "publications", "people", "studies", "comments", "@type", "@context"])

def ISAJson_encoder(id_map: Any | None, inv: ArcInvestigation) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], id_map: Any=id_map, inv: Any=inv) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow3041(__unit: None=None, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        value: str = ROCrate_genID(inv)
        class ObjectExpr3040(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr3040()

    def _arrow3043(__unit: None=None, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        value_1: str = ArcInvestigation.FileName()
        class ObjectExpr3042(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_1)

        return ObjectExpr3042()

    def _arrow3045(__unit: None=None, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        value_2: str = inv.Identifier
        class ObjectExpr3044(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_2)

        return ObjectExpr3044()

    def _arrow3047(value_3: str, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        class ObjectExpr3046(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_3)

        return ObjectExpr3046()

    def _arrow3049(value_5: str, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        class ObjectExpr3048(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_5)

        return ObjectExpr3048()

    def _arrow3051(value_7: str, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        class ObjectExpr3050(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_7)

        return ObjectExpr3050()

    def _arrow3053(value_9: str, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        class ObjectExpr3052(IEncodable):
            def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
                return helpers_6.encode_string(value_9)

        return ObjectExpr3052()

    def _arrow3054(osr: OntologySourceReference, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        return ISAJson_encoder_1(id_map, osr)

    def _arrow3055(oa: Publication, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        return ISAJson_encoder_2(id_map, oa)

    def _arrow3056(person: Person, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        return ISAJson_encoder_3(id_map, person)

    def _arrow3057(s: ArcStudy, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        return ISAJson_encoder_4(id_map, None, s)

    def _arrow3058(comment: Comment, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        return ISAJson_encoder_5(id_map, comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow3041()), ("filename", _arrow3043()), ("identifier", _arrow3045()), try_include("title", _arrow3047, inv.Title), try_include("description", _arrow3049, inv.Description), try_include("submissionDate", _arrow3051, inv.SubmissionDate), try_include("publicReleaseDate", _arrow3053, inv.PublicReleaseDate), try_include_seq("ontologySourceReferences", _arrow3054, inv.OntologySourceReferences), try_include_seq("publications", _arrow3055, inv.Publications), try_include_seq("people", _arrow3056, inv.Contacts), try_include_seq("studies", _arrow3057, inv.Studies), try_include_seq("comments", _arrow3058, inv.Comments)]))
    class ObjectExpr3059(IEncodable):
        def Encode(self, helpers_7: IEncoderHelpers_1[Any], id_map: Any=id_map, inv: Any=inv) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_7))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_7.encode_object(arg)

    return ObjectExpr3059()


def _arrow3071(get: IGetters) -> ArcInvestigation:
    identifer: str
    match_value: str | None
    object_arg: IOptionalGetter = get.Optional
    match_value = object_arg.Field("identifier", string)
    identifer = create_missing_identifier() if (match_value is None) else match_value
    def _arrow3060(__unit: None=None) -> FSharpList[tuple[ArcStudy, FSharpList[ArcAssay]]] | None:
        arg_3: Decoder_1[FSharpList[tuple[ArcStudy, FSharpList[ArcAssay]]]] = list_1_1(ISAJson_decoder_1)
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("studies", arg_3)

    pattern_input: tuple[FSharpList[ArcStudy], FSharpList[FSharpList[ArcAssay]]] = unzip(default_arg(_arrow3060(), empty()))
    studies_raw: FSharpList[ArcStudy] = pattern_input[0]
    def projection(a: ArcAssay) -> str:
        return a.Identifier

    class ObjectExpr3062:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow3061(x: str, y: str) -> bool:
                return x == y

            return _arrow3061

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    assays: Array[ArcAssay] = list(distinct_by(projection, concat(pattern_input[1]), ObjectExpr3062()))
    studies: Array[ArcStudy] = list(studies_raw)
    def mapping(a_1: ArcStudy) -> str:
        return a_1.Identifier

    study_identifiers: Array[str] = list(map_1(mapping, studies_raw))
    def _arrow3063(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("title", string)

    def _arrow3064(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("description", string)

    def _arrow3065(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("submissionDate", string)

    def _arrow3066(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("publicReleaseDate", string)

    def _arrow3067(__unit: None=None) -> Array[OntologySourceReference] | None:
        arg_13: Decoder_1[Array[OntologySourceReference]] = resize_array(ISAJson_decoder_2)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("ontologySourceReferences", arg_13)

    def _arrow3068(__unit: None=None) -> Array[Publication] | None:
        arg_15: Decoder_1[Array[Publication]] = resize_array(ISAJson_decoder_3)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("publications", arg_15)

    def _arrow3069(__unit: None=None) -> Array[Person] | None:
        arg_17: Decoder_1[Array[Person]] = resize_array(ISAJson_decoder_4)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("people", arg_17)

    def _arrow3070(__unit: None=None) -> Array[Comment] | None:
        arg_19: Decoder_1[Array[Comment]] = resize_array(ISAJson_decoder_5)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("comments", arg_19)

    return ArcInvestigation(identifer, _arrow3063(), _arrow3064(), _arrow3065(), _arrow3066(), _arrow3067(), _arrow3068(), _arrow3069(), assays, studies, study_identifiers, _arrow3070())


ISAJson_decoder: Decoder_1[ArcInvestigation] = Decode_objectNoAdditionalProperties(ISAJson_allowedFields, _arrow3071)

__all__ = ["encoder", "decoder", "encoder_compressed", "decoder_compressed", "ROCrate_genID", "ROCrate_encoder", "ROCrate_decoder", "ROCrate_encodeRoCrate", "ISAJson_allowedFields", "ISAJson_encoder", "ISAJson_decoder"]

