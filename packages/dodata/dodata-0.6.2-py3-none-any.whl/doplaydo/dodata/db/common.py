"""Common utilities for the db portion of the sdk."""

from sqlmodel import cast, Boolean, Numeric, Integer, SQLModel
from sqlalchemy.sql import ColumnElement
from .. import Analysis


def attribute_filter(
    model: SQLModel, key: str, value: int | bool | float | str
) -> ColumnElement[bool]:
    """Filter data model attributes based on the specified key and value.

    Args:
        model (SQLModel): Database model representing the data.
        key (str): Key for the attribute to filter.
        value (int | bool | float | str): Value to filter for.

    Raises:
        ValueError: If value is not of type bool, str, float, or int.
        ValueError: If key is not found in model.

    Returns:
        ColumnElement[bool]: A SQLAlchemy ColumnElement filtering condition.

    Example:
        import dodata_sdk as ddk
        ddk.attribute_filter(DeviceData, "measurement_type", "Spectrum")
        ddk.attribute_filter(Cell, "length_um", 15)
        ddk.attribute_filter(Wafer, "doping", 10e-18)
        ddk.attribute_filter(Analysis, "raised_flags", True)
    """
    if isinstance(value, int):
        return cast(model.attributes[key], Integer) == value
    elif isinstance(value, float):
        return cast(model.attributes[key], Numeric) == value
    elif isinstance(value, bool):
        return cast(model.attributes[key], Boolean) == value
    elif isinstance(value, str):
        return model.attributes[key].astext == value

    raise ValueError(
        "Can only filter attributes for strings, booleans, or numeric values."
    )


def analysis_filter(
    column_name: str, key: str, value: int | bool | float | str
) -> ColumnElement[bool]:
    """Filter data model attributes based on the specified key and value.

    Args:
        column_name (str): Name  the column to filter.
        key (str): Key for the column name to filter.
        value (int | bool | float | str): Value to filter for.

    Raises:
        ValueError: If value is not of type bool, str, float, or int.
        ValueError: If key is not found in column_name.
        AttributeError: If column_name is not found in Analysis model.

    Returns:
        ColumnElement[bool]: A SQLAlchemy ColumnElement filtering condition.

    Example:
        import dodata_sdk as ddk
        ddk.analysis_filter("parameters", "key", "width_um")
        ddk.analysis_filter("parameters", "value", 0.3)
    """
    try:
        analysis_column = getattr(Analysis, column_name)
    except AttributeError:
        raise ValueError(f"Column {column_name=} not found in Analysis model")

    if isinstance(value, int):
        return cast(analysis_column[key], Integer) == value
    elif isinstance(value, float):
        return cast(analysis_column[key], Numeric) == value
    elif isinstance(value, bool):
        return cast(analysis_column[key], Boolean) == value
    elif isinstance(value, str):
        return analysis_column[key].astext == value

    raise ValueError(
        "Can only filter attributes for strings, booleans, or numeric values."
    )
