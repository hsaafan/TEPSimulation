import warnings
from collections import OrderedDict
import pint

from .. import utils

from .graphing import (base, heat_exchange, sensors,
                       streams, transport, vessels)


class FlowSheet:
    def __init__(self) -> None:
        # Using ordered dictionaries to perserve output data order
        self.unit_operations = OrderedDict()
        self.streams = OrderedDict()
        self.sensors = OrderedDict()

    def add_unit_operation(self, unit_op: base.UnitOperation) -> None:
        if unit_op.id in self.unit_operations.keys():
            warnings.warn(f"Unit {unit_op.id} already exists, overriding")
        self.unit_operations[unit_op.id] = unit_op

    def add_stream(self, stream: base.Stream,
                   source_id: str, sink_id: str,
                   source_port: str = "Outlet",
                   sink_port: str = "Inlet") -> None:
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

    def add_sensor(self, sensor: sensors.Sensor,
                   target: list,
                   offset: pint.Quantity = None,
                   stdv: pint.Quantity = None) -> None:
        if sensor.id in self.sensors.keys():
            warnings.warn(f"Sensor {sensor.id} already exists, overriding")

        sensor.flowsheet = self  # Attach flowsheet to sensor

        # Setup sensor
        sensor.hook(target)
        if offset is not None:
            sensor.sensor_offset = offset
        if stdv is not None:
            sensor.sensor_stdv = stdv

        # Add sensor to flowsheet data
        self.sensors[sensor.id] = sensor

    def get_sensor_order(self) -> list:
        sensor_order = []
        for id in self.sensors.keys():
            sensor_order.append(id)
        return(sensor_order)

    def poll_sensors(self) -> list:
        sensor_data = []
        for id, sensor in self.sensors.items():
            sensor_data.append(sensor.poll())
        return(sensor_data)

    def step(self, time_step: pint.Quantity) -> list:
        for id, unit_operation in self.unit_operations.items():
            unit_operation.step(time_step)
        return(self.poll_sensors())
