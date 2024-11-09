from lionfuncs import LN_UNDEFINED, LionUndefinedType

from lion_core.models import SchemaModel


class TimedFuncCallConfig(SchemaModel):
    initial_delay: int = 0
    retry_default: str | LionUndefinedType = LN_UNDEFINED
    retry_timeout: int | None = None
    retry_timing: bool = False
    error_msg: str | None = None
    error_map: dict | None = None


class RetryConfig(SchemaModel):
    num_retries: int = 0
    initial_delay: int = 0
    retry_delay: int = 0
    backoff_factor: int = 1
    retry_default: str | LionUndefinedType = LN_UNDEFINED
    retry_timeout: int | None = None
    retry_timing: bool = False
    verbose_retry: bool = False
    error_msg: str | None = None
    error_map: dict | None = None
