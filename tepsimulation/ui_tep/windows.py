import sys

import PyQt5 as qt
import PyQt5.QtWidgets as qtw

from . import main_window, custom_widgets, about_dialog


class AboutDialog(qtw.QDialog):
    def __init__(self):
        super(AboutDialog, self).__init__()

        self.ui = about_dialog.Ui_about_dialog()
        self.ui.setupUi(self)


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = main_window.Ui_main_window()
        self.ui.setupUi(self)
