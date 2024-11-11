"""Initiates the module."""
# isort:skip_file
# ruff: noqa: E402, I001

from .config import get_settings
from doplaydo.dodata_core.models import (
    Project,
    Cell,
    Device,
    Die,
    Wafer,
    DeviceData,
    Analysis,
    AnalysisFunction,
    AnalysisFunctionTargetModel,
)
from doplaydo.dodata_core import models as models
from sqlalchemy.orm import aliased
from sqlmodel import and_, or_, select

ParentCell = aliased(Cell)

settings = get_settings()
from .engine import get_session

from .db.common import attribute_filter, analysis_filter
from .db.device_data import get_data_by_query, get_data_objects_by_query

from .api.device_data import get_data_by_pkey
from .api import analysis, cell, device, device_data, project

__version__ = "0.6.2"

# ruff: noqa: D101
__all__ = [
    "Analysis",
    "AnalysisFunction",
    "AnalysisFunctionTargetModel",
    "Cell",
    "Device",
    "DeviceData",
    "Die",
    "ParentCell",
    "Project",
    "Wafer",
    "analysis",
    "and_",
    "attribute_filter",
    "analysis_filter",
    "cell",
    "device",
    "device_data",
    "get_data_by_pkey",
    "get_data_by_query",
    "get_data_objects_by_query",
    "get_session",
    "models",
    "or_",
    "project",
    "select",
    "settings",
]
