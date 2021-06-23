import pint

from . import base, streams


class VesselJacket(base.UnitOperation):
    """ Jacket for vessels used to exchange heat """
    def __init__(self,
                 id: str,
                 inlet: streams.MaterialStream,
                 outlet: streams.MaterialStream,
                 heat_in: streams.EnergyStream,
                 heat_out: streams.EnergyStream):
        super().__init__(id)
        self.add_inlet(inlet, "fluid")
        self.add_outlet(outlet, "fluid")

        self.add_inlet(heat_in, "heat")
        self.add_outlet(heat_out, "heat")


class HeatExchanger(base.UnitOperation):
    """ Heat exchanger

    Attributes
    ----------
    thermal_inlet: MaterialStream
        The stream that is used to cool/heat the process fluid
    thermal_outlet: MaterialStream
        The stream to send the thermal fluid to after heat exchange
    process_inlet: MaterialStream
        The stream that is being cooled/heated
    process_outlet: MaterialStream
        The stream to send the process fluid to after heat exchange
    thermal_volume: pint.Quantity
        The volume of the piping that the thermal fluid passes through
    """
    def __init__(self,
                 thermal_inlet: streams.MaterialStream,
                 thermal_outlet: streams.MaterialStream,
                 process_inlet: streams.MaterialStream,
                 process_outlet: streams.MaterialStream,
                 thermal_volume: pint.Quantity):
        self.add_inlet(thermal_inlet, "thermal")
        self.add_outlet(thermal_outlet, "thermal")

        self.add_inlet(process_inlet, "process")
        self.add_outlet(process_outlet, "process")

        if base.pint_check(thermal_volume, '[volume]'):
            self.thermal_volume = thermal_volume

    def get_overall_heat_transfer_coefficient(self):
        # FIXME Currently have the stripper condenser values here, need to
        # figure out what they actually refer to
        U = 0.404655 * (1 - 1 / (1 + (self.outlets["process"].flowrate)**4))
        return(U)

    def get_thermal_heat_duty(self):
        # Calculate heat provided by thermal fluid
        tin = self.inlets["thermal"]
        tout = self.outlets["thermal"]
        temp_diff = tin.temeprature - tout.temperature
        specific_heat_capacity = tin.heat_capacity
        mass_flowrate = tin.mass_flowrate
        heat_duty = mass_flowrate * specific_heat_capacity * temp_diff
        return(heat_duty)

    def get_process_heat_duty(self, overall_heat_transfer_coefficient):
        # Calculate heat consumed by process fluid
        tout = self.outlets["thermal"]
        pout = self.outlets["process"]
        U = overall_heat_transfer_coefficient

        heat_duty = U * (tout.temperature - pout.temperature)
        # heat_duty *= (1 - 0.25 * variance)
        return(heat_duty)

    def get_thermal_temperature_change(self,
                                       thermal_heat_duty,
                                       process_heat_duty):
        # Calculate heat capacity of thermal fluid
        tin = self.inlets["thermal"]

        thermal_mass = tin.density * self.thermal_volume
        heat_capacity = tin.heat_capacity * thermal_mass
        change = (thermal_heat_duty - process_heat_duty) / heat_capacity
        return(change)

    def update_thermal_outlet_temperature(self, time_step: pint.Quantity):
        tout = self.outlets["thermal"]

        U = self.get_overall_heat_transfer_coefficient()
        Q_process = self.get_process_heat_duty(U)
        Q_thermal = self.get_thermal_heat_duty()
        delT = self.get_thermal_temperature_change(Q_thermal, Q_process)

        tout.temperature += time_step * delT

    def step_events(self, time_step: pint.Quantity):
        self.update_thermal_outlet_temperature(time_step)
