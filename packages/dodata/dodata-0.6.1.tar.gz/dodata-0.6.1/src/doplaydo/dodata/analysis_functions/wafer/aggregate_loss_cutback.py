"""Aggregate analysis."""

from typing import Any
import matplotlib.colors as mcolors
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from collections import defaultdict

import doplaydo.dodata as dd


def format_float(value: float, decimal_places: int) -> str:
    """Format a float to a string with a fixed number of decimal places.

    Args:
        value: Value to format.
        decimal_places: Number of decimal places to display.
    """
    return f"{value:.{decimal_places}f}"


def plot_wafermap(
    losses: dict[tuple[int, int], float],
    lower_spec: float,
    upper_spec: float,
    metric: str,
    key: str | None = None,
    value: float | None = None,
    decimal_places: int = 2,
    scientific_notation: bool = False,
    fontsize: int = 20,
    fontsize_die: int = 20,
    percentile_low: int = 5,
    percentile_high: int = 95,
) -> Figure:
    """Plot a wafermap of the losses.

    Args:
        losses: Dictionary of losses.
        lower_spec: Lower specification limit.
        upper_spec: Upper specification limit.
        metric: Metric to analyze.
        key: Key of the parameter to analyze.
        value: Value of the parameter to analyze.
        decimal_places: Number of decimal places to display.
        scientific_notation: Whether to display the values in scientific notation.
        fontsize: Font size for the labels.
        fontsize_die: Font size for the die labels.
        percentile_low: Lower percentile for the color scale.
        percentile_high: Upper percentile for the color scale.
    """
    # Calculate the bounds and center of the data
    die_xs, die_ys = zip(*losses.keys())
    die_x_min, die_x_max = min(die_xs), max(die_xs)
    die_y_min, die_y_max = min(die_ys), max(die_ys)

    # Create the data array
    data = np.full((die_y_max - die_y_min + 1, die_x_max - die_x_min + 1), np.nan)
    for (i, j), v in losses.items():
        data[j - die_y_min, i - die_x_min] = v

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6.8))

    # First subplot: Heatmap
    ax1.set_xlabel("Die X", fontsize=fontsize)
    ax1.set_ylabel("Die Y", fontsize=fontsize)
    title = f"{metric} {key}={value}" if value and key else f"{metric}"
    ax1.set_title(title, fontsize=fontsize, pad=10)

    cmap = plt.get_cmap("viridis")
    vmin = np.nanpercentile(list(losses.values()), percentile_low)
    vmax = np.nanpercentile(list(losses.values()), percentile_high)

    heatmap = ax1.imshow(
        data,
        cmap=cmap,
        extent=[die_x_min - 0.5, die_x_max + 0.5, die_y_min - 0.5, die_y_max + 0.5],
        origin="lower",
        vmin=vmin,
        vmax=vmax,
    )

    ax1.set_xlim(die_x_min - 0.5, die_x_max + 0.5)
    ax1.set_ylim(die_y_min - 0.5, die_y_max + 0.5)

    for (i, j), v in losses.items():
        if not np.isnan(v):
            if v is not None:
                value_str = (
                    f"{v:.{decimal_places}e}"
                    if scientific_notation
                    else f"{v:.{decimal_places}f}"
                )
            else:
                value_str = str(v)
            ax1.text(
                i,
                j,
                value_str,
                ha="center",
                va="center",
                color="white",
                fontsize=fontsize_die,
            )

    plt.colorbar(heatmap, ax=ax1)

    # Second subplot: Binary map based on specifications
    binary_map = np.where(
        np.isnan(data),
        np.nan,
        np.where((data >= lower_spec) & (data <= upper_spec), 1, 0),
    )

    cmap_binary = mcolors.ListedColormap(["red", "green"])
    heatmap_binary = ax2.imshow(
        binary_map,
        cmap=cmap_binary,
        extent=[die_x_min - 0.5, die_x_max + 0.5, die_y_min - 0.5, die_y_max + 0.5],
        origin="lower",
        vmin=0,
        vmax=1,
    )

    ax2.set_xlim(die_x_min - 0.5, die_x_max + 0.5)
    ax2.set_ylim(die_y_min - 0.5, die_y_max + 0.5)

    for (i, j), v in losses.items():
        if not np.isnan(v):
            if v is not None:
                value_str = (
                    f"{v:.{decimal_places}e}"
                    if scientific_notation
                    else f"{v:.{decimal_places}f}"
                )
            else:
                value_str = str(v)
            ax2.text(
                i,
                j,
                value_str,
                ha="center",
                va="center",
                color="white",
                fontsize=fontsize_die,
            )

    ax2.set_xlabel("Die X", fontsize=fontsize)
    ax2.set_ylabel("Die Y", fontsize=fontsize)
    ax2.set_title('KGD "Pass/Fail"', fontsize=fontsize, pad=10)
    plt.colorbar(heatmap_binary, ax=ax2, ticks=[0, 1]).set_ticklabels(
        ["Outside Spec", "Within Spec"]
    )
    return fig


def run(
    wafer_pkey: int,
    lower_spec: float,
    upper_spec: float,
    analysis_function_id: str,
    metric: str,
    key: str | None = None,
    value: float | None = None,
    decimal_places: int = 2,
    scientific_notation: bool = False,
    fontsize: int = 20,
    fontsize_die: int = 20,
    percentile_low: int = 5,
    percentile_high: int = 95,
) -> dict[str, Any]:
    """Returns wafer map of metric after analysis_function_id.

    Args:
        wafer_pkey: pkey of the wafer to analyze.
        lower_spec: Lower specification limit.
        upper_spec: Upper specification limit.
        analysis_function_id: Name of the die function to analyze.
        metric: Metric to analyze.
        key: Key of the parameter to analyze.
        value: Value of the parameter to analyze.
        decimal_places: Number of decimal places to display.
        scientific_notation: Whether to display the values in scientific notation.
        fontsize: Font size for the labels.
        fontsize_die: Font size for the die labels.
        percentile_low: Lower percentile for the color scale.
        percentile_high: Upper percentile for the color scale.
    """
    filter_clauses = [dd.AnalysisFunction.analysis_function_id == analysis_function_id]

    if key is not None:
        filter_clauses.append(
            dd.analysis_filter(column_name="parameters", key="key", value=key)
        )
    if value is not None:
        filter_clauses.append(
            dd.analysis_filter(column_name="parameters", key="value", value=value)
        )

    analyses = dd.db.analysis.get_analyses_for_wafer_by_pkey(
        wafer_pkey=wafer_pkey,
        target_model="die",
        filter_clauses=filter_clauses,
    )

    analyses_per_die: dict[tuple[int, int], list[dd.Analysis]] = defaultdict(list)

    for analysis in analyses:
        analyses_per_die[(analysis.die.x, analysis.die.y)].append(analysis)

    result: dict[tuple[int, int], dd.Analysis] = {}
    for coord, analyses in analyses_per_die.items():
        max_analysis_index = np.argmax([a.pkey for a in analyses])
        last_analysis = analyses[max_analysis_index]
        o = last_analysis.output[metric]  # get the last analysis (most recent)
        if not isinstance(o, float | int):
            raise ValueError(f"Analysis output {o} is not a float or int")
        result[coord] = o

    result_list = [value for value in result.values() if isinstance(value, int | float)]
    result_array = np.array(result_list)
    if np.any(np.isnan(result_array)) or not result:
        raise ValueError(
            f"No analysis for {wafer_pkey=} {analysis_function_id=} found."
        )

    summary_plot = plot_wafermap(
        result,
        value=value,
        key=key,
        lower_spec=lower_spec,
        upper_spec=upper_spec,
        metric=metric,
        decimal_places=decimal_places,
        scientific_notation=scientific_notation,
        fontsize=fontsize,
        fontsize_die=fontsize_die,
        percentile_low=percentile_low,
        percentile_high=percentile_high,
    )

    return dict(
        output={"losses": result_list},
        summary_plot=summary_plot,
        wafer_pkey=wafer_pkey,
    )


if __name__ == "__main__":
    parameters = {
        "key": "components",
        "upper_spec": 1.15,
        "lower_spec": 0,
        "analysis_function_id": "die_cutback",
        "metric": "component_loss",
    }
    wafer_pkey = 25
    d = run(wafer_pkey, **parameters)
    print(d["output"]["losses"])
