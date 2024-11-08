import numpy as np

from . import Config
from .utils import chosen_estimator
from pyroll.core import RollPass


@RollPass.Roll.neutral_point
def neutral_point(self: RollPass.Roll):
    if chosen_estimator(Config.ESTIMATOR, "napatov-ribbed-profile"):
        rp = self.roll_pass

        rib_flank_angle = np.deg2rad(rp.roll.groove.rib_flank_angle)

        rib_max_height = (rp.roll.groove.nominal_outer_diameter - rp.roll.groove.base_body_height) / 2

        period_length = rp.roll.groove.rib_distance + rp.roll.groove.rib_width + 2 * np.tan(
            rib_flank_angle) * rib_max_height

        angle_theta = np.deg2rad((period_length * 180) / (rp.roll.working_radius * np.pi))

        angle_ny = np.deg2rad((((np.tan(rib_flank_angle) * rib_max_height) + rp.roll.groove.rib_width * 0.5) * 180)
                              / (rp.roll.working_radius * np.pi))

        angle_psi = np.deg2rad((((np.tan(rib_flank_angle) * rib_max_height) + rp.roll.groove.rib_width * 0.5) * 180)
                               / (rp.roll.working_radius * np.pi))

        napatov_solution = ((rp.roll.working_radius * np.sin(angle_theta + angle_ny)
                             + np.tan(rib_flank_angle + angle_theta)
                             * (2 * rp.roll.working_radius * np.square(np.sin((angle_theta + angle_ny) / 2))
                                - rib_max_height) + rp.roll.working_radius * angle_psi * rp.elongation)
                            / period_length) - 1

        return -((rp.roll.contact_length / 2) * (1 - napatov_solution))
