import pytest
import os
import warnings

import pint

from ..packages import materials


@pytest.mark.filterwarnings("ignore:Component simple material:UserWarning",
                            "ignore:Adding new components:UserWarning")
class TestMaterials:
    @pytest.fixture
    def simple_material(self):
        # Create material file
        file_path = "simple_component"
        component_file = """
        Name: simple material
        Molar Mass:
          Value: 1.0
          Units: g / mol
        Antoines:
          A: 1.0
          B: 2.0
          C: 3.0
          Base: 2.71828
          Pressure Units: Pa
          Temperature Units: celsius
        Liquid Density:
          A: 1.0
          B: 2.0
          C: 3.0
          Temperature Units: celsius
          Density Units: lb / ft ** 3
        Liquid Specific Enthalpy:
          A: 1.0
          B: 2.0
          C: 3.0
          Temperature Units: celsius
          Enthalpy Units: cal / g
        Gas Specific Enthalpy:
          A: 1.0
          B: 2.0
          C: 3.0
          Temperature Units: celsius
          Enthalpy Units: cal / g
        Vaporization Heat:
          Value: 1.0
          Units: british_thermal_unit / lb
        """
        with open(file_path, 'w+') as f:
            f.write(component_file)
        simple_material = materials.Component(file_path)
        yield simple_material
        os.remove(file_path)
        materials.ComponentList.components = []
        materials.ComponentList.list_created = False
        return

    @pytest.fixture
    def component_list(self, simple_material):
        simple_material
        clist = materials.ComponentList()
        yield clist
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            materials.ComponentList.list_created = False

    @pytest.fixture
    def temperature(self):
        return(pint.Quantity("293 kelvin"))

    def test_create_fixture(self, simple_material):
        assert True

    def test_molar_mass_loaded(self, simple_material):
        mm = simple_material.molar_mass
        assert pint.Quantity("1 g/mol") == mm

    def test_vaporization_heat_loaded(self, simple_material):
        vh = simple_material.vaporization_heat
        assert pint.Quantity("1 british_thermal_unit/lb") == vh

    def test_name_loaded(self, simple_material):
        name = simple_material.name
        id = simple_material.id  # alias
        assert "simple material" == id == name

    def test_vapor_pressure(self, simple_material, temperature):
        T = temperature.to("celsius").magnitude
        value = 2.71828 ** (1 + 2/(3 + T))
        pressure = pint.Quantity(pytest.approx(value), "Pa")

        assert pressure == simple_material.vapor_pressure(temperature)

    def test_liquid_density(self, simple_material, temperature):
        T = temperature.to("celsius").magnitude
        value = 1 + (2 + 3 * T) * T
        rho_l = pint.Quantity(pytest.approx(value), "lb / ft ** 3")

        assert rho_l == simple_material.liquid_density(temperature)

    @pytest.mark.xfail(reason="test not implemented")
    def test_liquid_specific_enthalpy(self, simple_material, temperature):
        assert False

    @pytest.mark.xfail(reason="test not implemented")
    def test_liquid_specific_enthalpy_change(self, simple_material,
                                             temperature):
        assert False

    @pytest.mark.xfail(reason="test not implemented")
    def test_gas_specific_enthalpy(self, simple_material, temperature):
        assert False

    @pytest.mark.xfail(reason="test not implemented")
    def test_liquid_gas_enthalpy_change(self, simple_material, temperature):
        assert False

    def test_create_component_list(self, component_list):
        component_list

    def test_change_component_list_mass(self, component_list):
        addition = pint.Quantity("300 kg")
        component_list["simple material"].mass += addition
        assert component_list["simple material"].mass == addition

    def test_change_component_list_moles(self, component_list):
        addition = pint.Quantity("300 moles")
        component_list["simple material"].moles += addition
        assert component_list["simple material"].moles == addition


class TestReactions:
    pass


class TestImports:
    pass
