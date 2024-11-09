"""
Data Model.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Generic, Iterator, List, Mapping, Sequence, TypeVar, Union

import structlog
from pydantic import Extra, ValidationError, validator
from pydantic.fields import ModelField

from .base_model import BaseModel

if TYPE_CHECKING:
    import pandas as pd


logger = structlog.get_logger(__name__)

T = TypeVar("T")


class DataModel(BaseModel):
    """Model base-class."""

    if TYPE_CHECKING:
        fields: Any
        schema: Any

    class Config(BaseModel.Config):
        """Model config."""

        extra = Extra.allow

    def __init__(self, **kwargs: Any) -> None:
        """Initialise model."""

        super().__init__(**kwargs)

    def __getattribute__(self, name: str) -> Any:
        """Get attribute."""

        if name.startswith("_"):
            return super().__getattribute__(name)

        try:
            result = super().__getattribute__(name)
        except AttributeError:
            if "_" in name:
                # fall back to attribute on child field
                head, tail = name.rsplit("_", 1)
                if head in self.__fields__:
                    head = getattr(self, head)
                    try:
                        return getattr(head, tail)
                    except AttributeError:
                        pass
            raise

        return KList(result) if isinstance(result, list) else result

    def __setattr__(self, name: str, value: Any) -> None:
        """Set attribute."""

        if name.startswith("_"):
            super().__setattr__(name, value)

        try:
            super().__setattr__(name, value)
        except ValueError:
            if "_" in name:
                # fall back to attribute on child field
                head, tail = name.rsplit("_", 1)
                if head in self.__fields__:
                    head = getattr(self, head)
                    try:
                        setattr(head, tail, value)
                    except ValueError:
                        pass
                    else:
                        return
            raise

    @validator("*", pre=True)
    def convert_datetime(cls, value: Any, field: ModelField) -> Any:
        """Correct data-type for datetime values."""

        if not isinstance(value, datetime):
            return value

        field_type = field.type_

        if not isinstance(field_type, type):
            return value

        if issubclass(field_type, str):
            suffix = "Z" if value.microsecond else ".000000Z"
            return value.astimezone(timezone.utc).replace(tzinfo=None).isoformat() + suffix
        elif issubclass(field_type, float):
            return value.timestamp()
        elif issubclass(field_type, int):
            return int(value.timestamp() * 1e9)
        else:
            return value


P = TypeVar("P", bound=DataModel)


class PaginatorDataModel(DataModel, Generic[P]):
    """Paginator data-model."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialise model."""

        super().__init__(**kwargs)

    @validator("data", pre=True, check_fields=False)
    def validate_data(cls, v: Sequence[Mapping[str, Any]], field: ModelField) -> List[P]:
        """Validate data field."""

        T = field.type_
        results = []

        for item in v:
            try:
                results += [T(**item)]
            except ValidationError as e:
                logger.warning("Skipped invalid item", name=T.__name__, item=item, error=e)

        return results

    def __getitem__(self, item: Union[str, int]) -> Any:
        """Get item."""

        if isinstance(item, int):
            return self.data[item]

        return super().__getitem__(item)

    def to_df(self) -> pd.DataFrame:
        """
        Converts the data in the object to a pandas DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing the data.
        """
        import pandas as pd

        if len(self.data) == 0:
            return pd.DataFrame()

        headers: List[str] = sorted(list(self.data[0].dict().keys()))
        return pd.DataFrame([item.dict() for item in self.data], columns=headers)


class KList(List[P]):
    """
    Represents a list of objects of DataModel type.

    This class extends the built-in List class and provides additional functionality.

    Methods:
        to_df(): Converts the list to a pandas DataFrame.

    """

    def to_df(self) -> pd.DataFrame:
        """
        Converts the list to a pandas DataFrame.

        Returns:
            pd.DataFrame: A DataFrame representation of the list.

        """
        import pandas as pd

        if len(self) == 0:
            return pd.DataFrame()

        headers: List[str] = sorted(list(self[0].dict().keys()))
        return pd.DataFrame([item.dict() for item in self], columns=headers)


class KIterator(Iterator[P]):
    """
    An iterator class that wraps another iterator and provides additional functionality.

    Args:
        iterator (Iterator[Any]): The iterator to be wrapped.

    Attributes:
        iterator (Iterator[Any]): The wrapped iterator.

    Methods:
        __iter__(): Returns the iterator object itself.
        __next__(): Returns the next item from the iterator.
        to_df(): Convert the iterator's data into a pandas DataFrame.

    """

    def __init__(self, iterator: Iterator[Any]) -> None:
        self.iterator: Iterator[Any] = iterator

    def __iter__(self) -> Any:
        return self.iterator.__iter__()

    def __next__(self) -> Any:
        return self.iterator.__next__()

    def to_df(self) -> pd.DataFrame:
        """
        Convert the iterator's data into a pandas DataFrame.

        Returns:
            pd.DataFrame: The pandas DataFrame containing the iterator's data.
        """
        import pandas as pd

        data: List[Any] = [item.dict() for item in self.iterator]
        if len(data) == 0:
            return pd.DataFrame()

        if not isinstance(data[0], DataModel):
            return pd.DataFrame(data)
        headers: List[str] = sorted(list(data[0].keys()))
        return pd.DataFrame(data, columns=headers)


DataModelBase = DataModel
