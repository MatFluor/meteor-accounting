# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sb_dialog.ui'
#
# Created: Sat May 17 07:07:19 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_sb_dialog(object):
    def setupUi(self, sb_dialog):
        sb_dialog.setObjectName("sb_dialog")
        sb_dialog.resize(568, 256)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/pencil.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        sb_dialog.setWindowIcon(icon)
        self.buttonBox = QtGui.QDialogButtonBox(sb_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 170, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_6 = QtGui.QLabel(sb_dialog)
        self.label_6.setGeometry(QtCore.QRect(310, 220, 81, 31))
        self.label_6.setObjectName("label_6")
        self.tableWidget = QtGui.QTableWidget(sb_dialog)
        self.tableWidget.setGeometry(QtCore.QRect(300, 10, 261, 191))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(6)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(2, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(3, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(5, 0, item)
        self.tableWidget.verticalHeader().setVisible(False)
        self.formLayoutWidget = QtGui.QWidget(sb_dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 261, 146))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_4)
        self.bel_nr = QtGui.QLineEdit(self.formLayoutWidget)
        self.bel_nr.setObjectName("bel_nr")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.bel_nr)
        self.kto = QtGui.QLineEdit(self.formLayoutWidget)
        self.kto.setObjectName("kto")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.kto)
        self.dialog_txt = QtGui.QLineEdit(self.formLayoutWidget)
        self.dialog_txt.setObjectName("dialog_txt")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.dialog_txt)
        self.date = QtGui.QDateEdit(self.formLayoutWidget)
        self.date.setCalendarPopup(True)
        self.date.setObjectName("date")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.date)
        self.label_7 = QtGui.QLabel(self.formLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_7)
        self.multi_betrag = QtGui.QLineEdit(self.formLayoutWidget)
        self.multi_betrag.setObjectName("multi_betrag")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.multi_betrag)
        self.rest_label = QtGui.QLabel(sb_dialog)
        self.rest_label.setGeometry(QtCore.QRect(410, 223, 61, 21))
        self.rest_label.setText("")
        self.rest_label.setObjectName("rest_label")

        self.retranslateUi(sb_dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), sb_dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), sb_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(sb_dialog)

    def retranslateUi(self, sb_dialog):
        sb_dialog.setWindowTitle(QtGui.QApplication.translate("sb_dialog", "Sammelbuchung erfassen", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("sb_dialog", "Restbetrag", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(0).setText(QtGui.QApplication.translate("sb_dialog", "Neue Zeile", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(1).setText(QtGui.QApplication.translate("sb_dialog", "Neue Zeile", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(2).setText(QtGui.QApplication.translate("sb_dialog", "Neue Zeile", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(3).setText(QtGui.QApplication.translate("sb_dialog", "Neue Zeile", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(4).setText(QtGui.QApplication.translate("sb_dialog", "Neue Zeile", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(5).setText(QtGui.QApplication.translate("sb_dialog", "Neue Zeile", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("sb_dialog", "GegenKonto", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("sb_dialog", "Betrag", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.label.setText(QtGui.QApplication.translate("sb_dialog", "Belegnummer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("sb_dialog", "Datum", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("sb_dialog", "Konto", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("sb_dialog", "Text", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("sb_dialog", "Betrag", None, QtGui.QApplication.UnicodeUTF8))

