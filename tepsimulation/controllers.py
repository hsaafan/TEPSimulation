""" Controllers

Controllers are used to communicate between the views and models
"""
from models import Model
from views import GUIView, CLIView


class Controller:
    view = None
    model = None

    has_gui = False
    view = None
    model = None
    controller = None

    # Setup methods
    def __init__(self, use_gui: bool = True, seed: int = None,
                 time: float = 24, time_step: float = 0.1,
                 path: str = "./settings"):
        if use_gui:
            self.view = GUIView()
        else:
            self.view = CLIView()
        self.model = Model()

        self.view.connect_controller(self)
        self.model.connect_controller(self)

        self.model.set_seed(seed)
        self.model.set_time(time, time_step)
        self.model.set_settings_path(path)
        self.start_program()

    def start_program(self):
        self.view.start()

    def output_to_console(self, text: str):
        self.view.output_to_console(text)

    # Action methods
    def open_window(self):
        self.view.show_window()
        sys.exit(self._app.exec_())

    # Tabs
    def toggle_continuous_sim(self):
        # TODO
        return

    def toggle_fixed_sim(self):
        # TODO
        return

    # Other
    def run(self):
        self.model.run()

    def stop(self):
        self.model.stop()
        return

    def reset(self):
        self.model._current_step = 0
        self.model.STOP_SIGNAL = False
        self.view.update_progress_bar(0)

    # Signal methods
    def update_progress(self):
        current_time = self.model._current_step * self.model._time_step
        total_time = self.model._total_step_count * self.model._time_step
        percent_done = current_time / total_time * 100
        self.view.update_progress(percent_done)
