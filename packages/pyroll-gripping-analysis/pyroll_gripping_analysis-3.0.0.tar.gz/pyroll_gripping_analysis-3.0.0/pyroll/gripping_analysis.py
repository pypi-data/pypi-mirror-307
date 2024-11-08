import sys
import scipy
import shapely
import numpy as np

from pyroll.core import SymmetricRollPass, PassSequence, Unit
from pyroll.core.hooks import Hook, root_hooks

VERSION = "3.0.0"

SymmetricRollPass.bite_angle = Hook[np.ndarray]()
"""Angle of bite."""

SymmetricRollPass.passed_gripping_condition = Hook[bool]()
"""Array of entry points of the gripping elements."""


@SymmetricRollPass.bite_angle
def bite_angle(self: SymmetricRollPass):
    return -np.arcsin(self.entry_point / self.roll.min_radius)


@SymmetricRollPass.passed_gripping_condition
def passed_gripping_condition(self: SymmetricRollPass):
    if np.tan(self.bite_angle) > self.coulomb_friction_coefficient:
        return True
    else:
        return False


root_hooks.add(SymmetricRollPass.passed_gripping_condition)
root_hooks.add(SymmetricRollPass.bite_angle)


try:
    from pyroll.report.pluggy import hookimpl, plugin_manager
    from pyroll.report.utils import create_sequence_plot


    @hookimpl(specname="unit_plot")
    def mean_bite_angles_plot(unit: Unit):
        if isinstance(unit, PassSequence):
            if any(isinstance(subunit, SymmetricRollPass) for subunit in unit):
                fig, ax = create_sequence_plot(unit)
                ax.set_ylabel(r"Mean Bite Angle $\alpha_0$")
                ax.set_title("Bite Angle")

                units = list(unit)
                if len(units) > 0:
                    x, y = np.transpose(
                        [
                            (index, np.rad2deg(unit.bite_angle))
                            for index, unit in enumerate(units)
                            if isinstance(unit, SymmetricRollPass)
                        ]
                    )

                ax.bar(x=x, height=y, width=0.8)

                return fig


    plugin_manager.register(sys.modules[__name__])

except ImportError:
    pass  # report not installed
