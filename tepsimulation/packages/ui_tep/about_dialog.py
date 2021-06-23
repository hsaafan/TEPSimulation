# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/karamelm1nt/Documents/Code/TEPSimulation/ui/ui_about_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_about_dialog(object):
    def setupUi(self, about_dialog):
        about_dialog.setObjectName("about_dialog")
        about_dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        about_dialog.resize(487, 191)
        about_dialog.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        about_dialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(about_dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_title = QtWidgets.QLabel(about_dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_title.setFont(font)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName("label_title")
        self.verticalLayout.addWidget(self.label_title)
        self.label_copyright = QtWidgets.QLabel(about_dialog)
        self.label_copyright.setAlignment(QtCore.Qt.AlignCenter)
        self.label_copyright.setObjectName("label_copyright")
        self.verticalLayout.addWidget(self.label_copyright)
        self.label_license1 = QtWidgets.QLabel(about_dialog)
        self.label_license1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_license1.setObjectName("label_license1")
        self.verticalLayout.addWidget(self.label_license1)
        self.label_license2 = QtWidgets.QLabel(about_dialog)
        self.label_license2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_license2.setObjectName("label_license2")
        self.verticalLayout.addWidget(self.label_license2)
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.setObjectName("button_layout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.button_layout.addItem(spacerItem)
        self.button_done = QtWidgets.QPushButton(about_dialog)
        self.button_done.setObjectName("button_done")
        self.button_layout.addWidget(self.button_done)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.button_layout.addItem(spacerItem1)
        self.button_layout.setStretch(0, 2)
        self.button_layout.setStretch(1, 1)
        self.button_layout.setStretch(2, 2)
        self.verticalLayout.addLayout(self.button_layout)

        self.retranslateUi(about_dialog)
        self.button_done.clicked.connect(about_dialog.close)
        QtCore.QMetaObject.connectSlotsByName(about_dialog)

    def retranslateUi(self, about_dialog):
        _translate = QtCore.QCoreApplication.translate
        about_dialog.setWindowTitle(_translate("about_dialog", "About"))
        self.label_title.setText(_translate("about_dialog", "Tennessee Eastman Process Simulation"))
        self.label_copyright.setText(_translate("about_dialog", "Copyright (c) 2021 Hussein Saafan"))
        self.label_license1.setText(_translate("about_dialog", "This software uses the MIT license"))
        self.label_license2.setText(_translate("about_dialog", "A Copy of this license is bundled with this software"))
        self.button_done.setText(_translate("about_dialog", "Done"))
