from lion_core.protocols.adapters.adapter import AdapterRegistry
from lion_core.protocols.adapters.json_adapter import (
    JsonAdapter,
    JsonFileAdapter,
)
from lion_core.protocols.adapters.pandas_adapter import (
    CSVFileAdapter,
    ExcelFileAdapter,
    PandasDataFrameAdapter,
)

ADAPTERS = [
    JsonAdapter,
    JsonFileAdapter,
    PandasDataFrameAdapter,
    CSVFileAdapter,
    ExcelFileAdapter,
]


class PileAdapterRegistry(AdapterRegistry):

    _adapters = {k.obj_key: k() for k in ADAPTERS}


__all__ = ["PileAdapterRegistry"]
