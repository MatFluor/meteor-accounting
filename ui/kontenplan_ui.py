# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'kontenplan.ui'
#
# Created: Sat May 17 07:07:19 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Kontenplan(object):
    def setupUi(self, Kontenplan):
        Kontenplan.setObjectName("Kontenplan")
        Kontenplan.resize(634, 466)
        self.new_kto_btn = QtGui.QPushButton(Kontenplan)
        self.new_kto_btn.setGeometry(QtCore.QRect(10, 10, 171, 25))
        self.new_kto_btn.setObjectName("new_kto_btn")
        self.del_kto_btn = QtGui.QPushButton(Kontenplan)
        self.del_kto_btn.setGeometry(QtCore.QRect(250, 10, 121, 25))
        self.del_kto_btn.setObjectName("del_kto_btn")
        self.edit_kto_btn = QtGui.QPushButton(Kontenplan)
        self.edit_kto_btn.setGeometry(QtCore.QRect(480, 10, 131, 25))
        self.edit_kto_btn.setObjectName("edit_kto_btn")
        self.verticalLayoutWidget = QtGui.QWidget(Kontenplan)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 40, 631, 421))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.retranslateUi(Kontenplan)
        QtCore.QMetaObject.connectSlotsByName(Kontenplan)

    def retranslateUi(self, Kontenplan):
        Kontenplan.setWindowTitle(QtGui.QApplication.translate("Kontenplan", "Kontenplan", None, QtGui.QApplication.UnicodeUTF8))
        self.new_kto_btn.setText(QtGui.QApplication.translate("Kontenplan", "Neues Konto hinzufügen", None, QtGui.QApplication.UnicodeUTF8))
        self.del_kto_btn.setText(QtGui.QApplication.translate("Kontenplan", "Konto löschen", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_kto_btn.setText(QtGui.QApplication.translate("Kontenplan", "Konto bearbeiten", None, QtGui.QApplication.UnicodeUTF8))

import images_rc
