from enum import StrEnum

from pydantic import BaseModel, Field, ConfigDict


class MetricBestValue(StrEnum):
    MIN = "min"
    MAX = "max"


class MetricType(StrEnum):
    SCALAR = "scalar"
    SERIES = "series"
    TIME_SERIES = "time_series"


class MetricKeyParameters(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    slice: str | None = None
    type: MetricType = MetricType.SCALAR
    best_value: MetricBestValue | None = None


class Metric(MetricKeyParameters):
    value: float | int | list[float] | list[int]
    std: float | None = None


class Metrics(BaseModel):
    metrics: list[Metric] | None = None
    model_config = ConfigDict(
        ser_json_inf_nan='strings'
    )
