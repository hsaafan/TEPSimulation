import pytest
import pint

from ..packages.graph import flowsheet
from ..packages.graph.graphing import (base, heat_exchange,
                                       streams, transport, vessels)


class TestConnections:
    @pytest.fixture
    def simple_unit(self):
        inlet = base.Stream("Stream 1")
        outlet = base.Stream("Stream 2")
        unit = base.UnitOperation("Unit")
        unit.add_inlet(inlet, "Inlet")
        unit.add_outlet(outlet, "Outlet")
        simple_unit = {"unit": unit, "inlet": inlet, "outlet": outlet}
        return(simple_unit)

    @pytest.fixture
    def two_units(self):
        source = base.UnitOperation("Source Unit")
        sink = base.UnitOperation("Sink Unit")
        connection = base.Stream("Connection")
        source.add_outlet(connection, "Outlet")
        sink.add_inlet(connection, "Inlet")
        two_units = {"source": source, "sink": sink, "connection": connection}
        return(two_units)

    def test_connection_name(self, simple_unit):
        assert simple_unit["unit"].inlets["Inlet"].id == "Stream 1"

    def test_inlet_connected_unit(self, simple_unit):
        assert simple_unit["unit"].inlets["Inlet"] is simple_unit["inlet"]

    def test_inlet_connected_stream(self, simple_unit):
        assert simple_unit["unit"] is simple_unit["inlet"].sink

    def test_inlet_null_source(self, simple_unit):
        with pytest.raises(AttributeError):
            simple_unit["inlet"].source

    def test_outlet_connected_unit(self, simple_unit):
        assert simple_unit["unit"].outlets["Outlet"] is simple_unit["outlet"]

    def test_outlet_connected_stream(self, simple_unit):
        assert simple_unit["unit"] is simple_unit["outlet"].source

    def test_outlet_null_sink(self, simple_unit):
        with pytest.raises(AttributeError):
            simple_unit["outlet"].sink

    def test_string_repr_null_connections(self, simple_unit):
        assert "broken" in str(simple_unit["outlet"]).lower()

    def test_string_repr_connection(self, two_units):
        assert (two_units["source"].id in str(two_units["connection"]) and
                two_units["sink"].id in str(two_units["connection"]))


class TestUnits:
    @pytest.fixture
    def temperature(self):
        return(pint.Quantity(10, "K"))

    @pytest.fixture
    def pressure(self):
        return(pint.Quantity(10, "psi"))

    @pytest.fixture
    def length(self):
        return(pint.Quantity(10, "m"))

    def test_set_temperature_correct(self, temperature):
        obj = base.FlowSheetObject("obj")
        obj.temperature = temperature

    def test_set_temperature_incorrect(self, pressure):
        obj = base.FlowSheetObject("obj")
        with pytest.raises(TypeError):
            obj.temperature = pressure

    def test_set_pressure_correct(self, pressure):
        obj = base.FlowSheetObject("obj")
        obj.pressure = pressure

    def test_set_pressure_incorrect(self, temperature):
        obj = base.FlowSheetObject("obj")
        with pytest.raises(TypeError):
            obj.pressure = temperature

    def test_set_stream_pressure(self, pressure):
        obj = base.Stream("obj")
        with pytest.raises(AttributeError):
            obj.pressure = pressure

    def test_set_vessel_dimensions_correct(self, length):
        obj = vessels.Vessel("obj")
        obj.set_dimensions(length, length)

    def test_set_vessel_dimensions_incorrect(self, pressure):
        obj = vessels.Vessel("obj")
        with pytest.raises(TypeError):
            obj.set_dimensions(pressure, pressure)


class TestFlowsheet:
    @pytest.fixture
    def empty_flowsheet(self):
        fs = flowsheet.FlowSheet()
        return(fs)

    @pytest.fixture
    def connected_flowsheet(self):
        fs = flowsheet.FlowSheet()
        source = base.UnitOperation("Source")
        sink = base.UnitOperation("Sink")

        fs.add_unit_operation(source)
        fs.add_unit_operation(sink)

        stream = base.Stream("Stream")
        fs.add_stream(stream, "Source", "Sink")
        return(fs)

    def test_add_unit_operation(self, empty_flowsheet):
        reactor = base.UnitOperation("Reactor")
        empty_flowsheet.add_unit_operation(reactor)
        try:
            exists = empty_flowsheet.unit_operations["Reactor"]
            assert True
        except KeyError:
            assert False

    def test_add_stream(self, empty_flowsheet):
        source = base.UnitOperation("Source")
        sink = base.UnitOperation("Sink")

        empty_flowsheet.add_unit_operation(source)
        empty_flowsheet.add_unit_operation(sink)

        stream = base.Stream("Stream")
        empty_flowsheet.add_stream(stream, "Source", "Sink")

        try:
            exists = empty_flowsheet.streams["Stream"]
            assert True
        except KeyError:
            assert False

    def test_stream_connection(self, connected_flowsheet):
        source = connected_flowsheet.unit_operations["Source"]
        sink = connected_flowsheet.unit_operations["Sink"]
        stream = connected_flowsheet.streams["Stream"]
        assert (stream.source is source and stream.sink is sink)

    def test_unit_connection(self, connected_flowsheet):
        source = connected_flowsheet.unit_operations["Source"]
        stream = connected_flowsheet.streams["Stream"]
        assert (stream is source.outlets["Outlet"])
