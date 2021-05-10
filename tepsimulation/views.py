""" Views

Views are used to relay information to the user.
"""
import sys
from math import ceil

import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
from PyQt5.QtGui import QDesktopServices

from ui_tep import windows


class View:
    """ View class

    The view portion of the model-view-controller structure.
    """
    _controller = None

    def __init__(self):
        return

    def start(self):
        raise RuntimeError("No view has been selected, cannot start")

    def connect_controller(self, controller):
        self._controller = controller

    def update_progress(self, percent_done):
        raise RuntimeError("No progress bar is available in this view")

    def show_copyright_information(self):
        info = ""
        info += "Tennessee Eastman Process Simulation\n"
        info += "Copyright (c) 2021 Hussein Saafan\n"
        info += "This software uses the MIT license\n"
        info += "A copy of this license is bundled with this software"
        return(info)

    def open_github(self):
        return("https://github.com/hsaafan/TEPSimulation")


class CLIView(View):

    def start(self):
        # CHECK Is anything needed here?
        return

    def update_progress(self, percent_done):
        print(percent_done)

    def show_copyright_information(self):
        print(super().show_copyright_information())

    def open_github(self):
        print(super().open_github())


class GUIView(View):
    """ GUI View Class

    A user view using Qt5.
    """
    _app = None
    _main_window = None
    _about_dialog = None

    def __init__(self):
        self._app = qtw.QApplication(sys.argv)
        self._main_window = windows.MainWindow()
        self._about_dialog = windows.AboutDialog()

    def start(self):
        self._connect_inputs()
        self._main_window.show()
        sys.exit(self._app.exec_())

    def show_copyright_information(self):
        self._about_dialog.show()

    def open_github(self):
        url = super().open_github()
        QDesktopServices.openUrl(qtc.QUrl(url))

    def update_progress(self, percent_done):
        bar = self._main_window.ui.progress_bar
        bar.setValue(ceil(percent_done))

    def _connect_inputs(self):
        # Menubar
        help_about = self._main_window.ui.help_about
        help_git = self._main_window.ui.help_github

        help_about.triggered.connect(self.show_copyright_information)
        help_git.triggered.connect(self.open_github)
        # TODO: add other menubar entries here

        # Tabs
        fixed_sim = self._main_window.ui.rb_fixed_sim
        continuous_sim = self._main_window.ui.rb_continuous_sim

        fixed_sim.toggled.connect(self._controller.toggle_fixed_sim)
        continuous_sim.toggled.connect(self._controller.toggle_continuous_sim)

        # Other
        run_button = self._main_window.ui.run_button
        stop_button = self._main_window.ui.stop_button
        self.console = self._main_window.ui.console_output

        run_button.clicked.connect(self._controller.run)
        stop_button.clicked.connect(self._controller.stop)
