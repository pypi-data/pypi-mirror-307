from enum import StrEnum, auto

from pydantic import BaseModel, ConfigDict, Extra


class DataType(StrEnum):
    Integer = auto()
    Float = auto()
    String = auto()
    Boolean = auto()
    Date = auto()

    URL = auto()  # string variant

    Bytes = auto()  # for inline image/audio


class SemanticType(StrEnum):
    Prediction = auto()
    Metric = auto()

    Timestamp = auto()  # semantic for integer field

    JSON = auto()

    Image = auto()
    Audio = auto()
    Video = auto()
    Code = auto()


class JoinType(StrEnum):
    Inner = auto()


class ImageSematicProperties(BaseModel):
    _expected_sematic_type: SemanticType = SemanticType.Image
    preview_for_column: str


class MetricSemanticProperties(BaseModel):
    _expected_sematic_type: SemanticType = SemanticType.Metric
    diff_to_column: str


class ColumnInformation(BaseModel):
    name: str
    title: str | None = None
    tooltip: str | None = None
    type: DataType
    group_id: str | None = None
    show: bool = True
    semantic: SemanticType | None = None
    semantic_props: ImageSematicProperties | MetricSemanticProperties | dict | None = None
    join_type: JoinType | None = None

    model_config = ConfigDict(extra=Extra.forbid)


class DataFormatType(StrEnum):
    JSON = auto()
    DSV = auto()
    Binary = auto()
    Pickle = auto()  # for insecure serialized formats


class DataFormat(BaseModel):
    data_format: DataFormatType
    dsv_delimiter: str | None = None  # for DSV

    model_config = ConfigDict(extra=Extra.forbid)


class DataDescription(BaseModel):
    columns: list[ColumnInformation]
    data_format: DataFormat

    model_config = ConfigDict(extra=Extra.forbid)
