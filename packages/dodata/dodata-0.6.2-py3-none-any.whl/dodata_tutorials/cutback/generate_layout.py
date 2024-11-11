"""Generates a layout for a chip with a cutback sweep."""

from functools import partial
import gdsfactory as gf


size = (6050, 4100)
pack = partial(gf.pack, max_size=size, add_ports_prefix=False, spacing=2)
add_gc = gf.routing.add_fiber_array
ring_double = gf.components.cutback_loss_mmi1x2


@gf.cell(check_ports=False)
def cutback() -> gf.Component:
    """Returns a component cutback sweep."""
    loss = (0, 1, 2)
    cutback_sweep = gf.components.cutback_loss_mmi1x2(
        component=gf.components.mmi1x2(), loss=loss
    )
    cutback_sweep_gratings = [add_gc(c) for c in cutback_sweep]

    for loss, c in zip(loss, cutback_sweep_gratings):
        c.name = f"cutback_loss_{loss}"

    c = pack(cutback_sweep_gratings)
    if len(c) > 1:
        print(f"Failed to pack in 1 component of {size}, got {len(c)}")
        c = gf.grid(c)
    else:
        c = c[0]
    return c


@gf.cell(check_ports=False)
def top() -> gf.Component:
    """Returns a top cell."""
    c = gf.Component()
    ref = c << cutback()
    c.add_ports(ref.ports)
    return c


if __name__ == "__main__":
    from gdsfactory.labels import get_test_manifest

    c = top()
    c.write_gds("test_chip.gds")
    df = get_test_manifest(c, one_setting_per_column=True)
    df.to_csv("test_manifest.csv", index=False)
    print(df)
    # print(df.cell_settings[0])
    # df = write_settings_table()
    # df.to_csv("cell_table.csv", index=False)
    c.show()
