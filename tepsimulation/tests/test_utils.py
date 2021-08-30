import pytest

from ..packages import utils


class TestRandom:
    @pytest.fixture(autouse=True)
    def default_seed(self):
        utils.set_seed(None)

    @pytest.fixture
    def number_tests(self):
        return(1000)

    @pytest.fixture
    def bound_tolerance(self):
        return(1e-2)

    def test_seed_update(self, number_tests):
        for _ in range(number_tests):
            assert utils.get_seed() != utils.get_seed()

    def test_prng_in_range(self, number_tests):
        for _ in range(number_tests):
            assert -1 <= utils.get_prng() <= 1

    def test_prng_upper_bound(self, number_tests, bound_tolerance):
        ub = 0
        for _ in range(number_tests):
            ub = max(ub, utils.get_prng())
        assert abs(1 - ub) < bound_tolerance

    def test_prng_lower_bound(self, number_tests, bound_tolerance):
        lb = 0
        for _ in range(number_tests):
            lb = min(lb, utils.get_prng())
        assert abs(-1 - lb) < bound_tolerance

    def test_prng_pos_in_range(self, number_tests):
        for _ in range(number_tests):
            assert 0 <= utils.get_prng_pos() <= 1

    def test_prng_pos_upper_bound(self, number_tests, bound_tolerance):
        ub = 0
        for _ in range(number_tests):
            ub = max(ub, utils.get_prng_pos())
        assert abs(1 - ub) < bound_tolerance

    def test_prng_pos_lower_bound(self, number_tests, bound_tolerance):
        lb = 0
        for _ in range(number_tests):
            lb = min(lb, utils.get_prng_pos())
        assert abs(0 - lb) < bound_tolerance


class TestDictionaryUtils:
    @pytest.fixture
    def props(self):
        props = {"prop_a": {"prop_c": 51, "units": "C", "special_prop": 1},
                 "prop_b": {"prop_c": 25, "units": "C"}}
        return(props)

    def test_dict_keys_equal(self, props):
        assert utils.compare_dict_struct(props, props)

    def test_dict_keys_not_equal(self, props):
        not_props = {"prop_c": {"prop_a": 51, "units": "C", "special_prop": 1},
                     "prop_c": {"prop_b": 25, "units": "C"}}
        assert not utils.compare_dict_struct(props, not_props)

    def test_change_keys_to_lowercase(self):
        mixed = {
            "a": 3,
            "B": {
                    "C": 4,
                    "d": {
                          "e": 1
                        }
                }
            }
        lower = {
            "a": 3,
            "b": {
                    "c": 4,
                    "d": {
                          "e": 1
                        }
                }
            }
        assert lower == utils.dict_to_lowercase(mixed)
