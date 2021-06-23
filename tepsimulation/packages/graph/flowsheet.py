import warnings
from collections import OrderedDict
import pint

from .. import utils

from .graphing import (base, heat_exchange, sensors,
                       streams, transport, vessels)


class FlowSheet:
    def __init__(self):
        # Using ordered dictionaries to perserve output data order
        self.unit_operations = OrderedDict()
        self.streams = OrderedDict()
        self.sensors = OrderedDict()

    def add_unit_operation(self, unit_op: base.UnitOperation):
        if unit_op.id in self.unit_operations.keys():
            warnings.warn(f"Unit {unit_op.id} already exists, overriding")
        self.unit_operations[unit_op.id] = unit_op

    def add_stream(self, stream: base.Stream,
                   source_id: str, sink_id: str,
                   source_port: str = "Outlet",
                   sink_port: str = "Inlet"):
        if stream.id in self.streams.keys():
            warnings.warn(f"Stream {stream.id} already exists, overriding")

        # Connect stream to source
        source = self.unit_operations[source_id]
        stream.source = source
        source.add_outlet(stream, outlet_id=source_port)

        # Connect stream to sink
        sink = self.unit_operations[sink_id]
        stream.sink = sink
        sink.add_inlet(stream, inlet_id=sink_port)

        # Add stream to flowsheet data
        self.streams[stream.id] = stream
        return

    def add_sensor(self, sensor: sensors.Sensor, sensor_id: str):
        pass

    def get_sensor_order(self):
        sensor_order = []
        for id in self.sensors.keys():
            sensor_order.append(id)
        return(sensor_order)

    def poll_sensors(self):
        sensor_data = []
        for sensor in self.sensors:
            sensor_data.append(sensor.poll())
        return(sensor_data)

    def step(self, time_step: pint.Quantity):
        for unit_operation in self.unit_operations:
            unit_operation.step(time_step)
        return(self.poll_sensors())
