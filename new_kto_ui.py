# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_kto.ui'
#
# Created: Thu May 15 17:23:43 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_new_kto(object):
    def setupUi(self, new_kto):
        new_kto.setObjectName("new_kto")
        new_kto.resize(326, 197)
        self.buttonBox = QtGui.QDialogButtonBox(new_kto)
        self.buttonBox.setGeometry(QtCore.QRect(10, 160, 311, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtGui.QWidget(new_kto)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 311, 151))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        self.comboBox = QtGui.QComboBox(self.formLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBox)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_4)
        self.comboBox_2 = QtGui.QComboBox(self.formLayoutWidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBox_2)
        self.kto_nr = QtGui.QLineEdit(self.formLayoutWidget)
        self.kto_nr.setObjectName("kto_nr")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.kto_nr)
        self.kto_name = QtGui.QLineEdit(self.formLayoutWidget)
        self.kto_name.setObjectName("kto_name")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.kto_name)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_5)
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_2)
        self.saldo = QtGui.QLineEdit(self.formLayoutWidget)
        self.saldo.setObjectName("saldo")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.saldo)

        self.retranslateUi(new_kto)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), new_kto.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), new_kto.reject)
        QtCore.QMetaObject.connectSlotsByName(new_kto)

    def retranslateUi(self, new_kto):
        new_kto.setWindowTitle(QtGui.QApplication.translate("new_kto", "Neues Konto hinzufügen", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("new_kto", "Art", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("new_kto", "Aktiven", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("new_kto", "Aufwand", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(2, QtGui.QApplication.translate("new_kto", "Passiven", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(3, QtGui.QApplication.translate("new_kto", "Ertrag", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("new_kto", "Kategorie", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("new_kto", "Kontonummer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("new_kto", "Kontoname", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("new_kto", "Saldo", None, QtGui.QApplication.UnicodeUTF8))

