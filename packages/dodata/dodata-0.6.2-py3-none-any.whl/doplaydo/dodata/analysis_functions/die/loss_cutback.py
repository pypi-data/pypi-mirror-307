"""Calculates propagation loss from cutback measurement."""

from typing import Any
import numpy as np
from matplotlib import pyplot as plt

import doplaydo.dodata as dd


def run(
    die_pkey: int,
    key: str = "width_um",
    value: float = 0.3,
    length_key: str = "length_um",
    convert_to_dB: bool = True,
) -> dict[str, Any]:
    """Returns propagation loss in dB/cm.

    Args:
        die_pkey: pkey of the die to analyze.
        key: key of the attribute to filter by.
        value: value of the attribute to filter by.
        length_key: key of the length attribute.
        convert_to_dB: if True, convert power to dB.
    """
    device_data_objects = dd.get_data_by_query(
        [dd.Die.pkey == die_pkey, dd.attribute_filter(dd.Cell, key, value)]
    )

    if not device_data_objects:
        raise ValueError(
            f"No device data found with die_pkey {die_pkey}, key {key!r}, value {value}"
        )

    powers = []
    lengths_um = []

    for device_data, df in device_data_objects:
        lengths_um.append(device_data.device.cell.attributes.get(length_key))
        power = df.output_power.max()
        power = 10 * np.log10(power) if convert_to_dB else power
        powers.append(power)

    p = np.polyfit(lengths_um, powers, 1)
    propagation_loss = p[0] * 1e4 * -1

    fig = plt.figure()
    plt.plot(lengths_um, powers, "o")
    plt.plot(lengths_um, np.polyval(p, lengths_um), "r-", label="fit")

    ylabel = "Power (dBm)" if convert_to_dB else "Power (mW)"
    plt.xlabel("Length (um)")
    plt.ylabel(ylabel)
    plt.title(f"Propagation loss {key}={value}: {p[0]*1e4*-1:.2e} dB/cm ")

    return dict(
        output={"propagation_loss_dB_cm": propagation_loss},
        summary_plot=fig,
        die_pkey=die_pkey,
    )


if __name__ == "__main__":
    d = run(7732)
    print(d["output"]["propagation_loss_dB_cm"])
