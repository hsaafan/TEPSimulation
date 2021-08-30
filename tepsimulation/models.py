from math import ceil
from time import sleep
from os import getcwd

import packages.materials as materials
import packages.graph.flowsheet as flowsheet


class Model:
    """ Model class

    The model portion of the model-view-controller structure.
    Attributes
    ----------
    is_running: bool
        Is the simulation currently running
    settings_directory: str
        The path to the settings folder
    simulation_time: float
        The total time to simulate in hours
    time_step: float
        The time step used in the simulation in hours
    total_step_count: int
        The total model steps required for the current simulation

    Methods
    -------
    connect_controller
        Connect the model to the controller
    import_settings
        Import all the settings from the directory
    append_console_buffer
        Add messages to the console buffer
    output_console_buffer
        Output all the messages in the console buffer to the controller
    reset_model
        Reset the simulation
    run
        Start the simulation
    force_stop
        Forcefully stop the simulation while its running
    step_model
        Move the model one step forward
    """
    def __init__(self) -> None:
        self._console_buffer = ""
        self.is_running = False

    # Properties
    def settings_directory() -> dict:
        doc = """Directory of settings files"""

        def fget(self) -> str:
            """Returns the directory path."""
            return(f"{self._settings_directory}")

        def fset(self, directory: str) -> None:
            """Sets the path to the settings directory."""
            if directory is None:
                self._settings_directory = getcwd() + "/settings/"
            elif not isinstance(directory, str):
                raise TypeError(f"Expected a string value for the directory, "
                                f"got a {type(directory)} instead")
            if directory[0] == '/':
                # Passed directory is absolute
                self._settings_directory = directory
            else:
                # Assume relative
                self._settings_directory = getcwd() + "/" + directory

        return({'fget': fget, 'fset': fset, 'doc': doc})
    settings_directory = property(**settings_directory())

    def simulation_time() -> dict:
        doc = """Total time to simulate"""

        def fget(self) -> float:
            """Returns the simulation time."""
            return(self._simulation_time)

        def fset(self, value: float) -> None:
            """Sets the total simulation time."""
            if not isinstance(value, (int, float)):
                raise TypeError(f"Expected a float type time, "
                                f"got a {type(value)} instead")
            elif value <= 0:
                raise RuntimeError("Time must be a positive value")
            self._simulation_time = value

            try:
                step = self.time_step
            except AttributeError:
                step = None

            if step is not None:
                steps = ceil(self.simulation_time / step)
                self._total_step_count = steps
                self._current_step = 0

        return({'fget': fget, 'fset': fset, 'doc': doc})
    simulation_time = property(**simulation_time())

    def time_step() -> dict:
        doc = """Time step to use in the simulation"""

        def fget(self) -> float:
            """Returns the time step."""
            return(self._time_step)

        def fset(self, value: float) -> None:
            """Sets the time step."""
            if not isinstance(value, (int, float)):
                raise TypeError(f"Expected a float type time step, "
                                f"got a {type(value)} instead")
            elif value <= 0:
                raise RuntimeError("Time step must be a positive value")
            self._time_step = value

            try:
                time = self.simulation_time
            except AttributeError:
                time = None
            if time is not None:
                steps = ceil(self.simulation_time / self.time_step)
                self._total_step_count = steps
                self._current_step = 0

        return({'fget': fget, 'fset': fset, 'doc': doc})
    time_step = property(**time_step())

    def total_step_count() -> dict:
        doc = """Time step to use in the simulation"""

        def fget(self) -> int:
            """Returns the time step."""
            return(self._total_step_count)

        def fset(self) -> None:
            raise RuntimeError("Step count should not be set manually, it "
                               "is set automatically when setting the "
                               "simulation time and time step")

        return({'fget': fget, 'fset': fset, 'doc': doc})
    total_step_count = property(**total_step_count())

    # Private methods
    def _check_stop(self) -> None:
        if self._current_step >= self._total_step_count:
            self.append_console_buffer("Simulation has finished")
            self.is_running = False

    # Setup methods
    def connect_controller(self, controller) -> None:
        self._controller = controller

    def import_settings(self) -> None:
        """ Loads settings files from the disk """
        mat_dir = self._settings_directory + "components/"
        rxn_dir = self._settings_directory + "reactions/"
        unt_dir = self._settings_directory + "units/"

        self._materials = materials.import_materials(mat_dir)
        self._reactions = materials.import_reactions(rxn_dir)
        fs_dir = self._settings_directory + "flowsheet.yaml"
        self._flowsheet = flowsheet.FlowSheet()

    # Runtime methods
    def append_console_buffer(self, text: str) -> None:
        self._console_buffer += text

    def output_console_buffer(self) -> None:
        if self._console_buffer != "":
            self._controller.output_to_console(self._console_buffer)
            self._console_buffer = ""

    def reset_model(self) -> None:
        self._current_step = 0
        self.is_running = False

    def run(self, process_gui: bool = False) -> None:
        self.is_running = True
        while self.is_running:
            if process_gui:
                self._controller.process_gui()
            self.step_model()
            self._controller.update_progress()
            self._check_stop()
            self.output_console_buffer()
        self._controller.reset()

    def force_stop(self) -> None:
        self.is_running = False

    def step_model(self) -> None:
        self._flowsheet.step(self._time_step)
        # FIXME
        # measurements = self._flowsheet.poll_sensors()
        sleep(0.01)
        self._current_step += 1
