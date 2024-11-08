from . import Config
from .utils import chosen_estimator
from pyroll.core import SymmetricRollPass


@SymmetricRollPass.Roll.neutral_angle
def neutral_angle(self: SymmetricRollPass.Roll):
    if chosen_estimator(Config.ESTIMATOR, "siebel"):
        rp = self.roll_pass
        mean_flow_stress = (rp.in_profile.flow_stress + 2 * rp.out_profile.flow_stress) / 3

        return 1 / (4 * self.working_radius * mean_flow_stress * rp.coulomb_friction_coefficient) * (
                rp.front_tension * rp.in_profile.equivalent_height - rp.back_tension * rp.gap + 2 * self.working_radius * mean_flow_stress * (
                self.entry_angle ** 2 / 2 + rp.coulomb_friction_coefficient * self.entry_angle))
