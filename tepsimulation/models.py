from random import randint
from math import ceil
from time import sleep


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

    STOP_SIGNAL = False
    console = None
    console_buffer = ""
    is_running = False

    def connect_controller(self, controller):
        self._controller = controller

    def set_settings_path(self, settings_directory: str):
        # TODO: add path imports
        # self._materials = materials.import_materials(mat_directory)
        # self._flowsheet = flowsheet.FlowSheet(self._materials, fs_file)
        pass

    def set_seed(self, seed: int = None):
        """ Set model seed

        Seed must be a positive integer
        """
        if seed is None:
            seed = randint(1, 1e6)
        if seed <= 0:
            raise RuntimeError("Seed must be a positive integer")
        self._seed = seed

    def set_time(self, time: float, time_step: float):
        """ Set simulation time and time step

        Units of time are in hours
        """
        if time <= 0:
            raise RuntimeError("Simulation time must be a positive number")
        if time_step <= 0:
            raise RuntimeError("Time step must be a positive number")
        self._time = time
        self._time_step = time_step
        self._total_step_count = ceil(time / time_step)
        self._current_step = 0

    def append_console_buffer(self, text: str,
                              new_line: bool = True,
                              output: bool = True):
        if new_line:
            self.console_buffer += "\n"
        self.console_buffer += text
        if output:
            self.output_console_buffer()

    def output_console_buffer(self):
        if self.console_buffer != "":
            self._controller.output_to_console(self.console_buffer)
            self.console_buffer = ""

    def run(self):
        self.is_running = True
        while self.is_running:
            # FIXME: Remove sleep function
            sleep(0.01)

            self._controller.update_progress()
            self.output_console_buffer()
            self.check_stop()

            self._current_step += 1

    def check_stop(self):
        if self.STOP_SIGNAL:
            self.STOP_SIGNAL = False
            self.append_console_buffer("Stopped by user")
            self.is_running = False
        elif self._current_step >= self._total_step_count:
            self.is_running = False

    def stop(self):
        self.STOP_SIGNAL = True
        self._controller.reset()
