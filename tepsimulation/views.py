import sys
from math import ceil

import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
from PyQt5.QtGui import QDesktopServices

from packages.ui_tep import windows


class View:
    """ View class

    The view portion of the model-view-controller structure used as an
    interface between the user and program

    Attributes
    ----------

    Methods
    -------
    connect_controller
        Link a controller to the current view

    Dummy Methods
    -------------
    These methods are overwritten by a subclass
    start
        Start the program
    update_progress
        Display the current simulation progress
    show_copyright_information
        Display the copyright information of the program
    open_github
        Opens a link to the programs GitHubs
    """
    def connect_controller(self, controller) -> None:
        self._controller = controller

    # Dummy methods
    def start(self) -> None:
        raise RuntimeError("No view has been selected, cannot start")

    def reset_view(self) -> None:
        raise RuntimeError("No view has been selected, cannot reset")

    def update_progress(self, percent_done) -> None:
        raise RuntimeError("No progress bar is available in this view")

    def show_copyright_information(self) -> str:
        info = ""
        info += "Tennessee Eastman Process Simulation\n"
        info += "Copyright (c) 2021 Hussein Saafan\n"
        info += "This software uses the MIT license\n"
        info += "A copy of this license is bundled with this software"
        return(info)

    def open_github(self) -> str:
        return("https://github.com/hsaafan/TEPSimulation")

    def output_to_console(self, text: str) -> None:
        raise RuntimeError("No console available to output to")


class CLIView(View):
    """ Displays information through a command line interface

    See the View class documentation for information on methods and attributes
    """
    def start(self) -> None:
        # CHECK Is anything needed here?
        self.show_copyright_information()

    def update_progress(self, percent_done: float) -> None:
        """ Displays a progress bar in the command line """
        bar_length = 40
        fill_length = int(percent_done * bar_length // 100)
        bar = '█' * fill_length + '-' * (bar_length - fill_length)
        print(f'\rProgress |{bar}| {percent_done}%', end='\r')
        # Print New Line on Complete
        if percent_done >= 100:
            print()

    def show_copyright_information(self) -> None:
        print(super().show_copyright_information())

    def open_github(self) -> None:
        print(super().open_github())

    def output_to_console(self, text: str) -> None:
        print(text)


class GUIView(View):
    """ Displays information through a Qt GUI

    See the View class documentation for information on methods and attributes
    """
    def __init__(self) -> None:
        """ Create the Qt windows """
        self._app = qtw.QApplication(sys.argv)
        self._main_window = windows.MainWindow()
        self._about_dialog = windows.AboutDialog()

    def _connect_inputs(self) -> None:
        """ Connects Qt widgets to controller """
        # Menubar
        help_about = self._main_window.ui.help_about
        help_git = self._main_window.ui.help_github

        help_about.triggered.connect(self.show_copyright_information)
        help_git.triggered.connect(self.open_github)
        # TODO: add other menubar entries here

        # Tabs
        fixed_sim = self._main_window.ui.rb_fixed_sim
        continuous_sim = self._main_window.ui.rb_continuous_sim

        fixed_sim.toggled.connect(self._controller.toggle_sim_type, 0)
        continuous_sim.toggled.connect(self._controller.toggle_sim_type, 1)

        # Other
        run_button = self._main_window.ui.run_button
        stop_button = self._main_window.ui.stop_button
        self.console = self._main_window.ui.console_output

        run_button.clicked.connect(self._controller.run)
        stop_button.clicked.connect(self._controller.stop)

    def start(self) -> None:
        self._connect_inputs()
        self._main_window.show()
        sys.exit(self._app.exec_())

    def reset_view(self) -> None:
        """ Resets the progress bar and start/stop buttons """
        if self._main_window.ui.run_button.isHidden():
            self._main_window.ui.run_button.show()
            self._main_window.ui.stop_button.hide()
        elif self._main_window.ui.stop_button.isHidden():
            self._main_window.ui.run_button.hide()
            self._main_window.ui.stop_button.show()
        self.update_progress(0)

    def show_copyright_information(self) -> None:
        self._about_dialog.show()

    def open_github(self) -> None:
        url = super().open_github()
        QDesktopServices.openUrl(qtc.QUrl(url))

    def update_progress(self, percent_done) -> None:
        bar = self._main_window.ui.progress_bar
        bar.setValue(ceil(percent_done))

    def output_to_console(self, text: str) -> None:
        self._main_window.ui.console_output.appendPlainText(text)
