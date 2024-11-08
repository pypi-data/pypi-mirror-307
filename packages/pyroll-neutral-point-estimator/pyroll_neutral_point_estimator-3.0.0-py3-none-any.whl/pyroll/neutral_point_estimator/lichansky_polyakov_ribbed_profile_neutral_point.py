import numpy as np

from . import Config
from .utils import chosen_estimator
from pyroll.core import RollPass


@RollPass.Roll.neutral_point
def neutral_point(self: RollPass.Roll):
    if chosen_estimator(Config.ESTIMATOR, "lichansky-polyakov-ribbed-profile"):
        rp = self.roll_pass

        rib_flank_angle = np.deg2rad(rp.roll.groove.rib_flank_angle)

        rib_max_height = (rp.roll.groove.nominal_outer_diameter - rp.roll.groove.base_body_height) / 2

        period_length = rp.roll.groove.rib_distance + rp.roll.groove.rib_width + 2 * np.tan(
            rib_flank_angle) * rib_max_height

        rib_base_width = rp.roll.groove.rib_width + 2 * np.tan(rib_flank_angle) * rib_max_height

        median_height_outer_rib_distance = (period_length + rp.roll.groove.rib_width + np.tan(rib_flank_angle)
                                            * rib_max_height)

        entry_angle = np.abs(self.entry_angle)

        neutral_point_angle = np.arcsin(((np.cos(entry_angle) + rp.coulomb_friction_coefficient * np.sin(entry_angle)
                                          - 1) * ((rp.roll_force / rp.roll.contact_area) * rp.roll.working_radius * (
                    2 * period_length
                    - rib_base_width)) + rib_base_width * median_height_outer_rib_distance * (rp.roll.working_radius
                                                                                              - rib_max_height / 2)
                                         * np.sin(entry_angle)) / (2 * (
                    rp.coulomb_friction_coefficient * (rp.roll_force / rp.roll.contact_area)
                    * rp.roll.working_radius * (2 * period_length - rib_base_width)) + rib_base_width
                                                                   * median_height_outer_rib_distance * (
                                                                               rp.roll.working_radius - rib_max_height / 2)))

        return -np.sin(neutral_point_angle) * self.working_radius
