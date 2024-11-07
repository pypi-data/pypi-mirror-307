from pyroll.core import Hook, SymmetricRollPass
from pyroll.integral_thermal.helper import mean_temperature, mean_density, mean_specific_heat_capacity

SymmetricRollPass.deformation_heat_efficiency = Hook[float]()
"""Efficiency of heat generation through deformation. 1 means that all forming energy is dissipated as heat, 0 that all energy is saved in microstructure."""

SymmetricRollPass.temperature_change_by_contact = Hook[float]()
"""Get the change in temperature by contact transfer within the roll pass."""

SymmetricRollPass.temperature_change_by_deformation = Hook[float]()
"""Get the change in temperature by deformation heat within the roll pass."""

SymmetricRollPass.temperature_change = Hook[float]()
"""Get the change in temperature within the roll pass."""

SymmetricRollPass.Roll.contact_heat_transfer_coefficient = Hook[float]()
"""Get the heat transfer coefficient for contact of rolls and workpiece."""


@SymmetricRollPass.Roll.contact_heat_transfer_coefficient
def default_contact_heat_transfer_coefficient(self: SymmetricRollPass.Roll):
    return 6e3


@SymmetricRollPass.Roll.temperature
def default_roll_temperature(self: SymmetricRollPass.Roll):
    return 293.15


@SymmetricRollPass.OutProfile.temperature
def out_temperature(self: SymmetricRollPass.OutProfile):
    return self.roll_pass.in_profile.temperature + self.roll_pass.temperature_change


@SymmetricRollPass.deformation_heat_efficiency
def default_deformation_heat_efficiency(self: SymmetricRollPass):
    return 0.95


@SymmetricRollPass.temperature_change_by_contact
def temperature_change_by_contact(self: SymmetricRollPass):
    return -(
            (
                    self.roll.contact_heat_transfer_coefficient
                    * (mean_temperature(self) - self.roll.temperature)
                    * self.duration
                    * self.contact_area
            ) / (
                    mean_density(self)
                    * mean_specific_heat_capacity(self)
                    * self.volume
            )
    )


@SymmetricRollPass.temperature_change_by_deformation
def temperature_change_by_deformation(self: SymmetricRollPass):
    deformation_resistance = (
        self.deformation_resistance
        if self.has_value("deformation_resistance")
        else (self.in_profile.flow_stress + 2 * self.out_profile.flow_stress) / 3
    )
    return (
            (
                    self.deformation_heat_efficiency
                    * deformation_resistance
                    * self.strain
            ) / (
                    mean_density(self)
                    * mean_specific_heat_capacity(self)
            )
    )


@SymmetricRollPass.temperature_change
def temperature_change(self: SymmetricRollPass):
    return self.temperature_change_by_contact + self.temperature_change_by_deformation
