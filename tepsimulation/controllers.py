import datetime

from models import Model
from views import GUIView, CLIView
import packages.utils as utils


class Controller:
    """ Program Controller class

    Used to communicate with model and view
    Attributes
    ----------

    Methods
    -------
    output_to_console
        Relays information to the view object to be shown to the user
    toggle_sim_type
        Sets the simulation type to run for a fixed time and output the data
        or continuously run the simulation and output a data stream
    run
        Start the simulation
    stop
        Stops the current simulation
    reset
        Resets the simulation
    update_progress
        Calculate the model progress and update the view
    process_gui
        Process events to prevent model from locking GUI
    """
    # Setup methods
    def __init__(self, use_gui: bool = True, time: float = 24,
                 time_step: float = 0.1, path: str = "settings/") -> None:
        # Create view and model objects
        if use_gui:
            self._view = GUIView()
        else:
            self._view = CLIView()
        self._model = Model()

        # Connect view and model objects
        self._view.connect_controller(self)
        self._model.connect_controller(self)

        # Set model parameters
        self._model.simulation_time = time
        self._model.time_step = time_step
        self._model.settings_directory = path

        self._model.import_settings()

        # Start the view
        self._view.start()

    def output_to_console(self, text: str) -> None:
        """ Output message to console with a timestamp """
        curr_time = datetime.datetime.now().strftime("%H:%M:%S")
        time_stamp = f"[{curr_time}]: "
        self._view.output_to_console(time_stamp + text)

    # Tabs
    def toggle_sim_type(self, sim_type: int) -> None:
        # TODO make this do something
        if sim_type == 0:
            # Fixed time simulation
            pass
        elif sim_type == 1:
            # Continuously runnning simulation
            pass
        else:
            raise RuntimeError("Simulation type not found")

    # Other
    def run(self) -> None:
        """ Start the model simulation """
        self.output_to_console(f'Started with seed {utils.get_seed()}')
        self._model.run(isinstance(self._view, GUIView))

    def stop(self) -> None:
        """ Force stop the simulation """
        self.output_to_console(f'Stopped simulation')
        self._model.force_stop()
        self.reset()

    def reset(self) -> None:
        """ Reset the model and view once simulation has stopped """
        self._model.reset_model()
        self._view.reset_view()

    # Signal methods
    def update_progress(self) -> None:
        """ Calculate the percent finished and update the view """
        current_time = self._model._current_step * self._model._time_step
        total_time = self._model._total_step_count * self._model._time_step
        percent_done = current_time / total_time * 100
        self._view.update_progress(percent_done)

    def process_gui(self) -> None:
        """ Process any gui events to prevent locking """
        if not isinstance(self._view, GUIView):
            raise RuntimeError("Cannot process GUI events, no GUI found")
        self._view._app.processEvents()
