""" Model-View-Controller Module """
__author__ = "Hussein Saafan"
from math import ceil

import materials
import flowsheet
from random import randint


class Model:
    """ Model class

    The model portion of the model-view-controller structure.
    """
    _materials = None
    _flowsheet = None
    _seed = None
    _time = None
    _time_step = None
    _total_step_count = None
    _current_step = None
    _controller = None

    def __init__(self):
        self._seed = randint(1, 1e6)

    def connect_controller(self, controller):
        self._controller = controller

    def set_paths(self, mat_directory: str, fs_file: str):
        # TODO: add path imports
        # self._materials = materials.import_materials(mat_directory)
        # self._flowsheet = flowsheet.FlowSheet(self._materials, fs_file)
        pass

    def set_seed(self, seed: int = None):
        """ Set model seed

        Seed must be a positive integer
        """
        if seed <= 0:
            raise RuntimeError("Seed must be a positive integer")
        self._seed = seed
        return

    def set_time(self, time: float, time_step: float):
        """ Set simulation time and time step

        time is passed in hours
        time_step is passed in seconds
        """
        if time <= 0:
            raise RuntimeError("Simulation time must be a positive number")
        if time_step <= 0:
            raise RuntimeError("Time step must be a positive number")
        self._time = time
        self._time_step = time_step
        self._total_step_count = ceil(time * 3600 / time_step)
        self._current_step = 0
        return

    def step_model(self):
        while self._current_step < self._total_step_count:
            self._current_step += 1
        return


class View:
    """ View class

    The view portion of the model-view-controller structure.
    """

    def connect_controller(self, controller):
        self._controller = controller


class Controller:
    """ Controller class

    The controller portion of the model-view-controller structure.
    """

    view = None
    model = None

    def __init__(self):

        return

    def connect_view(self, view: View):
        self.view = View()
        self.view.connect_controller(self)

    def connect_model(self, model: Model):
        self.model = Model()
        self.model.connect_controller(self)

    def validate(self):

        return
