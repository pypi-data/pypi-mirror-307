from pyroll.core import CoolingPipe, Hook


@CoolingPipe.temperature_change_by_radiation
def cooling_pipe_temperature_change_by_radiation(self: CoolingPipe):
    return 0


@CoolingPipe.temperature_change_by_convection
def cooling_pipe_temperature_change_by_convection(self: CoolingPipe):
    return 0


@CoolingPipe.cooling_water_temperature
def default_cooling_water_temperature(self: CoolingPipe):
    return 298.15


@CoolingPipe.cooling_heat_transfer_coefficient
def default_cooling_heat_transfer_coefficient_cooling_pipe(self: CoolingPipe):
    """Default value from measurements by H. Wehage; (Beitrag zur rechnergestützten Erarbeitung von Projekten und
    Technologien für kontinuierliche Feinstahl- und Drahtstraßen, PhD, TU Freiberg, 1990)"""
    return 4000
