# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/karamelm1nt/Documents/Code/TEPSimulation/ui/ui_main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(800, 675)
        main_window.setAutoFillBackground(False)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.main_vertical_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.main_vertical_layout.setObjectName("main_vertical_layout")
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setObjectName("main_layout")
        self.tab_layout = QtWidgets.QTabWidget(self.central_widget)
        self.tab_layout.setTabPosition(QtWidgets.QTabWidget.North)
        self.tab_layout.setMovable(False)
        self.tab_layout.setTabBarAutoHide(False)
        self.tab_layout.setObjectName("tab_layout")
        self.tab_components = QtWidgets.QWidget()
        self.tab_components.setObjectName("tab_components")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_components)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.select_components = QtWidgets.QComboBox(self.tab_components)
        self.select_components.setObjectName("select_components")
        self.verticalLayout_2.addWidget(self.select_components)
        self.tree_components = QtWidgets.QTreeView(self.tab_components)
        self.tree_components.setObjectName("tree_components")
        self.verticalLayout_2.addWidget(self.tree_components)
        self.tab_layout.addTab(self.tab_components, "")
        self.tab_reactions = QtWidgets.QWidget()
        self.tab_reactions.setObjectName("tab_reactions")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_reactions)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.select_reactions = QtWidgets.QComboBox(self.tab_reactions)
        self.select_reactions.setObjectName("select_reactions")
        self.verticalLayout_3.addWidget(self.select_reactions)
        self.tree_reactions = QtWidgets.QTreeView(self.tab_reactions)
        self.tree_reactions.setObjectName("tree_reactions")
        self.verticalLayout_3.addWidget(self.tree_reactions)
        self.tab_layout.addTab(self.tab_reactions, "")
        self.tab_units = QtWidgets.QWidget()
        self.tab_units.setObjectName("tab_units")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_units)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.select_units = QtWidgets.QComboBox(self.tab_units)
        self.select_units.setObjectName("select_units")
        self.verticalLayout_4.addWidget(self.select_units)
        self.tree_units = QtWidgets.QTreeView(self.tab_units)
        self.tree_units.setObjectName("tree_units")
        self.verticalLayout_4.addWidget(self.tree_units)
        self.tab_layout.addTab(self.tab_units, "")
        self.tab_streams = QtWidgets.QWidget()
        self.tab_streams.setObjectName("tab_streams")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_streams)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.select_streams = QtWidgets.QComboBox(self.tab_streams)
        self.select_streams.setObjectName("select_streams")
        self.verticalLayout_6.addWidget(self.select_streams)
        self.tree_streams = QtWidgets.QTreeView(self.tab_streams)
        self.tree_streams.setObjectName("tree_streams")
        self.verticalLayout_6.addWidget(self.tree_streams)
        self.tab_layout.addTab(self.tab_streams, "")
        self.tab_sensors = QtWidgets.QWidget()
        self.tab_sensors.setObjectName("tab_sensors")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_sensors)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.select_sensors = QtWidgets.QComboBox(self.tab_sensors)
        self.select_sensors.setObjectName("select_sensors")
        self.verticalLayout_7.addWidget(self.select_sensors)
        self.tree_sensors = QtWidgets.QTreeView(self.tab_sensors)
        self.tree_sensors.setObjectName("tree_sensors")
        self.verticalLayout_7.addWidget(self.tree_sensors)
        self.tab_layout.addTab(self.tab_sensors, "")
        self.tab_disturbances = QtWidgets.QWidget()
        self.tab_disturbances.setObjectName("tab_disturbances")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab_disturbances)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.select_disturbances = QtWidgets.QComboBox(self.tab_disturbances)
        self.select_disturbances.setObjectName("select_disturbances")
        self.verticalLayout_8.addWidget(self.select_disturbances)
        self.tree_disturbances = QtWidgets.QTreeView(self.tab_disturbances)
        self.tree_disturbances.setObjectName("tree_disturbances")
        self.verticalLayout_8.addWidget(self.tree_disturbances)
        self.tab_layout.addTab(self.tab_disturbances, "")
        self.tab_options = QtWidgets.QWidget()
        self.tab_options.setObjectName("tab_options")
        self.formLayout_7 = QtWidgets.QFormLayout(self.tab_options)
        self.formLayout_7.setObjectName("formLayout_7")
        self.label_44 = QtWidgets.QLabel(self.tab_options)
        self.label_44.setObjectName("label_44")
        self.formLayout_7.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_44)
        self.comboBox_7 = QtWidgets.QComboBox(self.tab_options)
        self.comboBox_7.setObjectName("comboBox_7")
        self.formLayout_7.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox_7)
        self.rb_fixed_sim = QtWidgets.QRadioButton(self.tab_options)
        self.rb_fixed_sim.setChecked(True)
        self.rb_fixed_sim.setObjectName("rb_fixed_sim")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.rb_fixed_sim)
        self.rb_continuous_sim = QtWidgets.QRadioButton(self.tab_options)
        self.rb_continuous_sim.setObjectName("rb_continuous_sim")
        self.formLayout_7.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.rb_continuous_sim)
        self.tab_layout.addTab(self.tab_options, "")
        self.main_layout.addWidget(self.tab_layout)
        self.options_flowsheet_layout = QtWidgets.QVBoxLayout()
        self.options_flowsheet_layout.setObjectName("options_flowsheet_layout")
        self.flowsheet_viewer = QtWidgets.QOpenGLWidget(self.central_widget)
        self.flowsheet_viewer.setObjectName("flowsheet_viewer")
        self.options_flowsheet_layout.addWidget(self.flowsheet_viewer)
        self.progress_bar_layout = QtWidgets.QHBoxLayout()
        self.progress_bar_layout.setObjectName("progress_bar_layout")
        self.progress_bar = QtWidgets.QProgressBar(self.central_widget)
        self.progress_bar.setEnabled(True)
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar_layout.addWidget(self.progress_bar)
        self.run_button = QtWidgets.QPushButton(self.central_widget)
        self.run_button.setEnabled(True)
        self.run_button.setCheckable(False)
        self.run_button.setObjectName("run_button")
        self.progress_bar_layout.addWidget(self.run_button)
        self.stop_button = QtWidgets.QPushButton(self.central_widget)
        self.stop_button.setEnabled(True)
        self.stop_button.setVisible(False)
        self.stop_button.setObjectName("stop_button")
        self.progress_bar_layout.addWidget(self.stop_button)
        self.progress_bar_layout.setStretch(0, 9)
        self.progress_bar_layout.setStretch(1, 3)
        self.progress_bar_layout.setStretch(2, 3)
        self.options_flowsheet_layout.addLayout(self.progress_bar_layout)
        self.options_flowsheet_layout.setStretch(0, 8)
        self.options_flowsheet_layout.setStretch(1, 1)
        self.main_layout.addLayout(self.options_flowsheet_layout)
        self.main_layout.setStretch(0, 3)
        self.main_layout.setStretch(1, 4)
        self.main_vertical_layout.addLayout(self.main_layout)
        self.console_output = QtWidgets.QPlainTextEdit(self.central_widget)
        self.console_output.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.console_output.setReadOnly(True)
        self.console_output.setObjectName("console_output")
        self.main_vertical_layout.addWidget(self.console_output)
        self.main_vertical_layout.setStretch(0, 2)
        main_window.setCentralWidget(self.central_widget)
        self.menu_bar = QtWidgets.QMenuBar(main_window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menu_bar.setObjectName("menu_bar")
        self.menu_file = QtWidgets.QMenu(self.menu_bar)
        self.menu_file.setObjectName("menu_file")
        self.menu_import = QtWidgets.QMenu(self.menu_file)
        self.menu_import.setObjectName("menu_import")
        self.menu_export = QtWidgets.QMenu(self.menu_file)
        self.menu_export.setObjectName("menu_export")
        self.menu_help = QtWidgets.QMenu(self.menu_bar)
        self.menu_help.setObjectName("menu_help")
        main_window.setMenuBar(self.menu_bar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        self.help_about = QtWidgets.QAction(main_window)
        self.help_about.setObjectName("help_about")
        self.help_github = QtWidgets.QAction(main_window)
        self.help_github.setObjectName("help_github")
        self.import_component = QtWidgets.QAction(main_window)
        self.import_component.setObjectName("import_component")
        self.import_reaction = QtWidgets.QAction(main_window)
        self.import_reaction.setObjectName("import_reaction")
        self.import_unit = QtWidgets.QAction(main_window)
        self.import_unit.setObjectName("import_unit")
        self.export_data_stream = QtWidgets.QAction(main_window)
        self.export_data_stream.setObjectName("export_data_stream")
        self.export_output = QtWidgets.QAction(main_window)
        self.export_output.setObjectName("export_output")
        self.menu_quit = QtWidgets.QAction(main_window)
        self.menu_quit.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.menu_quit.setObjectName("menu_quit")
        self.menu_import.addAction(self.import_component)
        self.menu_import.addAction(self.import_reaction)
        self.menu_import.addAction(self.import_unit)
        self.menu_export.addAction(self.export_data_stream)
        self.menu_export.addAction(self.export_output)
        self.menu_file.addAction(self.menu_import.menuAction())
        self.menu_file.addAction(self.menu_export.menuAction())
        self.menu_file.addAction(self.menu_quit)
        self.menu_help.addAction(self.help_github)
        self.menu_help.addAction(self.help_about)
        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_help.menuAction())
        self.label_44.setBuddy(self.comboBox_7)

        self.retranslateUi(main_window)
        self.tab_layout.setCurrentIndex(0)
        self.run_button.clicked.connect(self.run_button.hide)
        self.stop_button.clicked.connect(self.stop_button.hide)
        self.run_button.clicked.connect(self.stop_button.show)
        self.stop_button.clicked.connect(self.run_button.show)
        self.menu_quit.triggered.connect(main_window.close)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Tennessee Eastman Process Simulation"))
        self.tab_layout.setTabText(self.tab_layout.indexOf(self.tab_components), _translate("main_window", "Components"))
        self.tab_layout.setTabText(self.tab_layout.indexOf(self.tab_reactions), _translate("main_window", "Reactions"))
        self.tab_layout.setTabText(self.tab_layout.indexOf(self.tab_units), _translate("main_window", "Units"))
        self.tab_layout.setTabText(self.tab_layout.indexOf(self.tab_streams), _translate("main_window", "Streams"))
        self.tab_layout.setTabText(self.tab_layout.indexOf(self.tab_sensors), _translate("main_window", "Sensors"))
        self.tab_layout.setTabText(self.tab_layout.indexOf(self.tab_disturbances), _translate("main_window", "Disturbances"))
        self.label_44.setText(_translate("main_window", "TextLabel"))
        self.rb_fixed_sim.setText(_translate("main_window", "Fixed Simulation Time"))
        self.rb_continuous_sim.setText(_translate("main_window", "Continuous Simulation"))
        self.tab_layout.setTabText(self.tab_layout.indexOf(self.tab_options), _translate("main_window", "Options"))
        self.run_button.setText(_translate("main_window", "Run"))
        self.stop_button.setText(_translate("main_window", "Stop"))
        self.console_output.setPlaceholderText(_translate("main_window", "Tennessee Eastman Process Copyright (c) 2021 Hussein Saafan"))
        self.menu_file.setTitle(_translate("main_window", "File"))
        self.menu_import.setTitle(_translate("main_window", "Import"))
        self.menu_export.setTitle(_translate("main_window", "Export"))
        self.menu_help.setTitle(_translate("main_window", "Help"))
        self.help_about.setText(_translate("main_window", "About"))
        self.help_github.setText(_translate("main_window", "GitHub"))
        self.import_component.setText(_translate("main_window", "Component"))
        self.import_reaction.setText(_translate("main_window", "Reaction"))
        self.import_unit.setText(_translate("main_window", "Unit"))
        self.export_data_stream.setText(_translate("main_window", "Data Stream"))
        self.export_output.setText(_translate("main_window", "Run Output"))
        self.export_output.setShortcut(_translate("main_window", "F5"))
        self.menu_quit.setText(_translate("main_window", "Quit"))
