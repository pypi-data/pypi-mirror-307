from __future__ import annotations
from typing import Any, Dict, Mapping, Sequence
import numpy
from ewokscore import Task

from .utils.ascii_utils import save_pattern_as_ascii

__all__ = ["SaveAsciiPattern1D"]


class SaveAsciiPattern1D(
    Task,
    input_names=["filename", "x", "y", "xunits"],
    optional_input_names=["header", "yerror", "metadata"],
    output_names=["saved"],
):
    """Save single diffractogram in ASCII format"""

    def run(self):
        header = self.get_input_value("header", dict())
        metadata = self.get_input_value("metadata", dict())
        yerror = self.get_input_value("yerror", None)

        save_pattern_as_ascii(
            self.inputs.filename,
            self.inputs.x,
            self.inputs.y,
            self.inputs.xunits,
            yerror,
            header,
            metadata,
        )
        self.outputs.saved = True


class SaveAsciiMultiPattern1D(
    Task,
    input_names=["filenames", "x_list", "y_list", "xunits_list"],
    optional_input_names=["header_list", "yerror_list", "metadata_list"],
    output_names=["saved"],
):
    def run(self):
        filenames: Sequence[str] = self.inputs.filenames
        x_list: Sequence[numpy.ndarray] = self.inputs.x_list
        y_list: Sequence[numpy.ndarray] = self.inputs.y_list
        xunits_list: Sequence[str] = self.inputs.xunits_list
        header_list: Sequence[Mapping] = self.get_input_value(
            "header_list", len(filenames) * [dict()]
        )
        yerror_list: Sequence[numpy.ndarray] | Sequence[None] = self.get_input_value(
            "yerror_list", len(filenames) * [None]
        )
        metadata_list: Sequence[Dict[str, Any]] = self.get_input_value(
            "metadata_list", len(filenames) * [dict()]
        )

        for args in zip(
            filenames,
            x_list,
            y_list,
            xunits_list,
            yerror_list,
            header_list,
            metadata_list,
        ):
            save_pattern_as_ascii(*args)

        self.outputs.saved = True
