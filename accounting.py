#!/usr/bin/env/python
# -*- coding:utf-8 -*-

from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtSql import *

#from PyQt4.QtGui import *
#from PyQt4.QtCore import *

from mainwindow_ui import *
from sb_dialog_ui import *
from kontenplan_ui import *
from kontoauszug_ui import *
from new_kto_ui import *
from mandanten_erstellen_ui import *
import sys
import sqlite3
import treeoftable
import meteorpdf
import os

from meteorpdf.theme import colors, DefaultTheme

TABLE_WIDTH = 530

fname = ':memory:'
connection = sqlite3.connect(fname)
cursor = connection.cursor()
cursor2 = connection.cursor()

class Accounting(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
            super(Accounting, self).__init__(parent)
            self.setupUi(self)
            # Diverse Button-Signals
            self.add_booking_btn.clicked.connect(self.AddBuchung)
            self.del_booking_btn.clicked.connect(self.DelBuchung)
            self.sammelbuchung_btn.clicked.connect(self.Sammelbuchung)
            self.edit_ktoplan_btn.clicked.connect(self.EditKontenplan)
            self.action_open.triggered.connect(self.openFile)
            self.actionNew_Mand.triggered.connect(self.newMand)
            self.show_report_btn.clicked.connect(self.showReports)
            #Saldoanzeige-signal
            self.soll_kto.textChanged.connect(lambda: self.getSaldo(self.soll_kto, self.soll_saldo))
            self.haben_ktos.textChanged.connect(lambda: self.getSaldo(self.haben_ktos, self.haben_saldo))
            # Aktuelles Datum Setzen
            now = QDate.currentDate()
            self.dateEdit.setDate(now)

            #Kontextmenu für Kontenplan
            #actionEdit = QAction("Neues Unterkonto hinzufügen", self)
            #actionEdit.triggered.connect(self.addItemAction)
            #self.kontenplan.addAction(actionEdit)
            #actionDelete = QAction("Konto löschen", self)
            #actionDelete.triggered.connect(self.deleteItem)
            #self.kontenplan.addAction(actionDelete)
            #self.verticalLayout_3.addWidget(self.kontenplan)
            
            
            #self.actionSave.triggered.connect(self.SaveAll)
#-------------------------------------------------------------------------------
    def getSaldo(self, kto, label):
        '''Holt den Kontensaldo des eingegebenen Kontos und schreibt ihn in ein Label'''
        kontonummer = kto.text()
        if len(kontonummer) == 4:
            try:
                statement = 'SELECT saldo FROM "%s" ORDER BY id DESC limit 1' % kontonummer
                saldo = cursor.execute(statement)
                for row in saldo:
                    sal = row[0]
                try:
                    label.setText(sal)
                except UnboundLocalError:
                    label.setText('0.00')
            except sqlite3.OperationalError:
                label.setText('Konto existiert nicht')
    def addItemAction(self):
        return
    def deleteItem(self):
        return
    def picked(self):
        return self.kontenplan.currentFields()
#-------------------------------------------------------------------------------
    def activated(self, fields):
        field = self.kontenplan.model().asRecord(fields)
        self.statusbar.showMessage("Konto: "+field[2]+', '+field[3]+' - Saldo: '+field[4], 60000)
        kontoauszug = Kontoauszug(self)
        kontoauszug.getWrite(field[3], field[2])
        kontoauszug.show()
#-------------------------------------------------------------------------------
    def openFile(self):
        global fname
        global connection
        file_filter = "Meteor Accounting Database (*.mt)"
        fname, _ = QtGui.QFileDialog.getOpenFileName(self, u'Mandant öffnen', '', file_filter)
        connection = sqlite3.connect(fname)
        self.readDB()
#-------------------------------------------------------------------------------
    def readDB(self):
        self.buchungen.clear()
        global cursor
        global cursor2
        cursor = connection.cursor()
        cursor2 = connection.cursor()
        try:
            self.kontenplan.clear()
        except AttributeError:
            pass
        self.UpdateKontenplan()
        infos = cursor.execute("SELECT * FROM mandant")
        for row in infos:
            name = row[1]
            adresse = row[2]
            mwst1 = row[3]
            mwst2 = row[4]
            mwst3 = row[5]
        self.mand_name.setText(name)
        self.mand_address.setPlainText(adresse)
        self.mwst_1.setText(mwst1)
        self.mwst_2.setText(mwst2)
        self.mwst_3.setText(mwst3)
        self.mwst_satz.clear()
        if mwst1 == "0" or mwst1 == '0.0' or mwst1 == '0.0 %':
            mwst1 = "Keine"
        self.mwst_satz.addItem(mwst1)
        self.mwst_satz.addItem(mwst2)
        self.mwst_satz.addItem(mwst3)
        buchungen = cursor.execute("SELECT * FROM transactions")
        trans_list = list()
        buchnr = 1
        for row in buchungen:
            toplevel = [str(row[0]), row[1], row[2], row[3], row[5], row[4], row[7], '']
            haben_child = ['', '', row[2], row[4], row[6], row[3], row[7], row[8]]
            steuer_child = ['','', row[2], '2200', str(float(row[5]) - float(row[6])), row[3], row[7], '']
            buchnr += 1
            self.populateWidgets(toplevel, haben_child, steuer_child)
        self.beleg_nr.setText(str(buchnr))
#-------------------------------------------------------------------------------
    def UpdateKontenplan(self):
        cursor = connection.cursor()
        try:
            self.verticalLayout_3.removeWidget(self.kontenplan)
        except AttributeError:
            pass
        # Saldobestimmung für Kontenplan
        konten = cursor.execute("SELECT * FROM kontenplan ORDER BY kontonummer")
        kontenstring = list()
        for row in konten:
            neuer_saldo = '0.0'
            statement = 'SELECT saldo FROM "%s"' % row[4]
            saldo = cursor2.execute(statement)
            for saldi in saldo:
                neuer_saldo = saldi[0]
            kontenstring.append(row[1]+'*'+row[2]+'*'+row[3]+'*'+row[4]+'*'+neuer_saldo)
        self.kontenplan = TreeOfTableWidget(kontenstring, 2, '*')
        headers = ['Kontoname', 'Kontonummer', 'Saldo']
        self.kontenplan.model().headers = headers
        self.connect(self.kontenplan, SIGNAL("activated(QModelIndex)"), self.activated)
        self.statusbar.showMessage('Kontenplan aktualisiert.', 60000)
        self.kontenplan.expandAll()
        self.kontenplan.resizeColumnToContents(0)
        self.kontenplan.resizeColumnToContents(1)
        self.verticalLayout_3.addWidget(self.kontenplan)
#-------------------------------------------------------------------------------
    def AddBuchung(self):
        '''Getting all fields, calculate and write to TreeWidget.'''
        # Get all Values
        item = self.buchungen.topLevelItem(0)
        if not item:
            buchnr = '1'
        else:
            buchnr = str(int(item.text(0))+1)
        belegnr = self.beleg_nr.text()
        date = self.dateEdit.textFromDateTime(self.dateEdit.dateTime())
        konto = self.soll_kto.text()
        betrag = self.betrag.text()
        mwst_txt = self.mwst_satz.currentText()
        buchungstext = self.buchungs_txt.text()
        gegenkonto = self.haben_ktos.text()
        mwst_betrag = ''
        # Calculate Tax-Logic
        if mwst_txt == 'Keine':
            netto = betrag
            pass
        else:
            mwst = mwst_txt[:-2]
            mwst = float(mwst)
            mwst_betrag = str(float(betrag)/100.0*mwst)
            netto = str(float(betrag)-(float(betrag)*mwst/100.0))
        
        # Populate lists
        saldo = cursor.execute('SELECT saldo FROM "'+konto+'"')
        for row in saldo:
            saldo = row[0]
        try:
            saldo = float(saldo) + float(netto)
            saldo = str(saldo)
        except:
            saldo = netto
        gegensaldo = cursor.execute('SELECT saldo FROM "'+gegenkonto+'"')
        for row in gegensaldo:
            gegensaldo = row[0]
        try:
            gegensaldo = float(gegensaldo) - float(netto)
            gegensaldo = str(gegensaldo)
        except: gegensaldo =  '-'+netto
        trans_inserts = [belegnr, date, konto, gegenkonto, betrag, netto, buchungstext, mwst_txt]
        sql_inserts = [date, belegnr, buchungstext, gegenkonto, netto, '', saldo]
        sql_gegeninserts = [date, belegnr, buchungstext, konto, '', netto, gegensaldo]
        toplevel = [buchnr, belegnr, date, konto, betrag, gegenkonto, buchungstext, '']
        haben_child = ['', '', date, gegenkonto, netto, konto, buchungstext, mwst_txt]
        steuer_child = ['', '', date, '2200', mwst_betrag, konto, buchungstext, '']
        
        self.populateWidgets(toplevel, haben_child, steuer_child)
        
        #Write to Database
        statement = 'INSERT INTO "%s" (datum, belegnr, buchungstext, gegenkonto, soll, haben, saldo) VALUES (?,?,?,?,?,?,?)' % konto
        cursor.execute(statement, sql_inserts)
        statement = 'INSERT INTO "%s" (datum, belegnr, buchungstext, gegenkonto, soll, haben, saldo) VALUES (?,?,?,?,?,?,?)' % gegenkonto
        cursor.execute(statement, sql_gegeninserts)
        statement = 'INSERT INTO transactions (belegnr, datum, soll_kto, haben_kto, brutto, netto, text, mwst_satz) VALUES (?,?,?,?,?,?,?,?)'
        cursor.execute(statement, trans_inserts)
        connection.commit()
        # Expand all Trees
        self.buchungen.expandAll()
        # Reset fields
        if not item:
            self.beleg_nr.setText('2')
        else:
            self.beleg_nr.setText(str(int(item.text(0))+2))
        self.soll_kto.setText('')
        self.haben_ktos.setText('')
        self.betrag.setText('')
        self.mwst_satz.setCurrentIndex(0)
        self.buchungs_txt.setText('')
        self.soll_kto_lbl.setText('Soll Konto')
        self.haben_kto_lbl.setText('Haben Konto')
        self.soll_saldo.setText('Saldo')
        self.haben_saldo.setText('Saldo')
        self.buchungen.resizeColumnToContents(0)
        self.buchungen.expandAll()
        # TODO
        # Buchung in Kontenplan-Saldo hinzufügen / abgleichen
        self.UpdateKontenplan()
#-------------------------------------------------------------------------------
    def populateWidgets(self, toplevel, haben_child, steuer_child):
        ''' Populate TreeWidget'''
        main_buchung = QTreeWidgetItem(toplevel)
        child1 = QTreeWidgetItem(haben_child)
        main_buchung.addChild(child1)
        steuerin = ['0.0', '']
        if steuer_child[4] not in steuerin:
            child2 = QTreeWidgetItem(steuer_child)
            child2.setForeground(2, QColor("blue"))
            child2.setForeground(3, QColor("blue"))
            child2.setForeground(4, QColor("blue"))
            child2.setForeground(5, QColor("blue"))
            child2.setForeground(6, QColor("blue"))
            main_buchung.addChild(child2)
        else: pass
        self.buchungen.insertTopLevelItem(0,main_buchung)
        self.buchungen.resizeColumnToContents(0)
        self.buchungen.resizeColumnToContents(1)
        self.buchungen.expandAll()
#-------------------------------------------------------------------------------
    def DelBuchung(self):
        '''Deletes a selected entry in the mein TreeWidget'''
        entry = self.buchungen.currentItem()
        item = self.buchungen.indexOfTopLevelItem(entry)
        self.buchungen.takeTopLevelItem(item)
#-------------------------------------------------------------------------------
    def Sammelbuchung(self):
        win = SB(self)
        win.show()
        win.bel_nr.setText('woohoo')
        rows = cursor.execute('''SELECT * FROM transactions''')
        for row in rows:
            print row
#-------------------------------------------------------------------------------
    def EditKontenplan(self):
        win = Kontenplan(self)
        win.update.connect(self.UpdateKontenplan)
        win.show()
#-------------------------------------------------------------------------------
    def SaveAll(self):
        return
    def showReports(self):
        if self.konto_chk.isChecked():
            self.getKontoauszug('Kontoauszug', self.mand_name.text())
        if self.bilanz_chk.isChecked():
            self.getBericht(self.mand_name.text(), "bilanz")
        if self.er_chk.isChecked():
            self.getBericht(self.mand_name.text(), "er")
#-------------------------------------------------------------------------------
    def getKontoauszug(self, filename, mandname):
        doc = meteorpdf.Pdf('Kontoauszug - Alle Konten','')
        doc.set_theme(MyTheme)
        doc.add_header(u'Kontoauszug für Mandant '+mandname, meteorpdf.H2)
        doc.add_spacer()
        statement = "SELECT kontoname, kontonummer FROM kontenplan ORDER BY kontonummer"
        res = cursor.execute(statement)
        for konto in res:
            total_soll = 0.0
            total_haben = 0.0
            buchungen_table = [['Datum', 'Belegnr.', 'Text', 'Gegenkonto', 'Soll', 'Haben', 'Saldo']] # this is the header row 
            statement = 'SELECT * FROM "%s"' %konto[1]
            result = cursor2.execute(statement)
            soll_cell = 0.00
            haben_cell = 0.00
            saldo_cell = 0.00
            for row in result:
                soll_cell = row[5]
                haben_cell = row[6]
                saldo_cell = row[7]
                if soll_cell != '':
                    soll_cell = '%.2f' % float(soll_cell)
                if haben_cell != '':
                    haben_cell = '%.2f' % float(haben_cell)
                if saldo_cell != '':
                    saldo_cell = '%.2f' % float(saldo_cell)
                buchungen_table.append(list(row[1:5])+[soll_cell,haben_cell, saldo_cell])
                try:
                    total_soll = float(total_soll) + float(row[5])
                except ValueError:
                    total_soll = total_soll
                try:
                    total_haben = float(total_haben) + float(row[6])
                except ValueError:
                    total_haben = total_haben
            if not self.nullein_chk.isChecked() and total_soll == 0.00 and total_haben == 0.00 and saldo_cell == 0.00:
                continue
            else:
                doc.add_header(konto[1]+' - '+konto[0], meteorpdf.H5)
                buchungen_table.append(['Summe Bewegungen:','','','','%.2f' % total_soll,'%.2f' % total_haben , saldo_cell]) 
                doc.add_table_auszug(buchungen_table, TABLE_WIDTH)

        document = doc.render()
        outfile = open(filename+' '+mandname+'.pdf', 'w')
        outfile.write(document)
        outfile.close()
        os.system('xdg-open "'+filename+' '+mandname+'.pdf"')
    def newMand(self):
        wizard = NewMand(self)
        wizard.wizard_done.connect(self.readDB)
        wizard.kontenplanupdate.connect(self.UpdateKontenplan)
        wizard.show()
    def getBericht(self, mandname, bericht):
        ''
        ## TODO Bilanzaufbau wie bei
        # andrasoft.ch/images/Druck_Bilanz.jpg
        adresse = self.mand_address.toPlainText()
        adresse = adresse.splitlines()
        full_adresse = ''
        for part in adresse:
            full_adresse += part+'<br/>'
        print full_adresse
        if bericht == 'bilanz':
            doc = meteorpdf.Pdf('Bilanz','')
            doc.add_paragraph(full_adresse)
            doc.add_header(u'Bilanz', meteorpdf.H2)
        if bericht == 'er':
            doc = meteorpdf.Pdf('Erfolgsrechnung','')
            doc.add_header(u'Erfolgsrechnung für Mandant '+mandname, meteorpdf.H2)
        doc.set_theme(MyTheme)
        doc.add_spacer()
        konten = []
        if bericht == 'bilanz':
            konten = ['Aktiven', 'Passiven']
        if bericht == 'er':
            konten = ['Aufwand', 'Ertrag']
        for kontoart in konten:
            total = 0.00
            kontoart_table = list()
            # Idee: Put in Dict
            if kontoart == 'Aktiven':
                subkonto = ['Umlaufvermögen','Anlagevermögen']
            if kontoart == 'Passiven':
                subkonto = ['Fremdkapital', 'Eigenkapital']
            for subart in subkonto:
                statement = "SELECT kontoname, kontonummer FROM kontenplan WHERE superkonto = '%s' AND subsuperkonto = '%s'" % (kontoart, subart)
                res = cursor.execute(statement)
                buchungen_table_header = [[kontoart]] # this is the header row
                buchungen_table = [[subart]] # Second header
                subtotal = 0.00
                for konto in res:
                    statement = 'SELECT saldo FROM "%s" ORDER BY id DESC limit 1' %konto[1]
                    result = cursor2.execute(statement)
                    for row in result:
                        saldo_cell = row[0]
                        total += float(saldo_cell)
                        subtotal += float(saldo_cell)
                        if saldo_cell != '':
                            saldo_cell = '%.2f' % float(saldo_cell)
                        buchungen_table.append([konto[1], konto[0], saldo_cell])
                buchungen_table[0] = buchungen_table[0]+['','','%.2f'% subtotal,'']
                kontoart_table.append(buchungen_table)
                buchungen_table_header[0] = buchungen_table_header[0]+['','','','','%.2f' %total]
            doc.add_bilanz_header(buchungen_table_header, TABLE_WIDTH)
            for table in kontoart_table:
                doc.add_table_bilanz(table, TABLE_WIDTH)
            doc.add(meteorpdf.PageBreak())
            
            
        document = doc.render()
        outfile = open('Bilanz '+mandname+'.pdf', 'w')
        outfile.write(document)
        outfile.close()
        os.system('xdg-open "Bilanz '+mandname+'.pdf"')
        
class NewMand(QtGui.QWizard, Ui_MandantenWizard):
    wizard_done = Signal()
    kontenplanupdate = Signal()
    def __init__(self, parent=None):
        super(NewMand,self).__init__(parent)
        self.setupUi(self)
        self.new_kto_btn.clicked.connect(self.newKonto)
        self.currentIdChanged.connect(self.createDB)
        self.wizardPage1.registerField("Mandantenname*", self.mand_name)
    
    def newKonto(self):
        newkonto = NewKonto(self)
        newkonto.addKonto.connect(self.UpdateKontenplan)
        newkonto.show()

    def UpdateKontenplan(self):
        try:
            self.verticalLayout.removeWidget(self.kontenplan)
        except AttributeError:
            pass
        # Saldobestimmung für Kontenplan
        konten = cursor.execute("SELECT * FROM kontenplan")
        kontenstring = list()
        for row in konten:
            neuer_saldo = '0.0'
            statement = 'SELECT saldo FROM "%s"' % row[4]
            saldo = cursor2.execute(statement)
            for saldi in saldo:
                neuer_saldo = saldi[0]
            kontenstring.append(row[1]+'*'+row[2]+'*'+row[3]+'*'+row[4]+'*'+neuer_saldo)
        self.kontenplan = TreeOfTableWidget(kontenstring, 2, '*')
        headers = ['Kontoname', 'Kontonummer', 'Saldo']
        self.kontenplan.model().headers = headers
        self.kontenplan.expandAll()
        self.kontenplan.resizeColumnToContents(0)
        self.kontenplan.resizeColumnToContents(1)
        #self.verticalLayout.removeWidget(self.kontenplan)
        self.verticalLayout.addWidget(self.kontenplan)
        self.kontenplanupdate.emit()
    def createDB(self):
        if self.currentId() == 1:
            global connection
            connection = sqlite3.connect(self.mand_name.text()+'.mt')
            global cursor
            global cursor2
            cursor = connection.cursor()
            cursor2 = connection.cursor()
            ## Cursors ändern!
            try:
                cursor.execute("""CREATE TABLE transactions ( 
                                                    number INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    belegnr TEXT, 
                                                    datum TEXT,
                                                    soll_kto TEXT,
                                                    haben_kto TEXT,
                                                    brutto TEXT,
                                                    netto TEXT,
                                                    text TEXT,
                                                    mwst_satz TEXT
                                                    )""")
                cursor.execute("""CREATE TABLE mandant ( 
                                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    name TEXT, 
                                                    adresse TEXT,
                                                    mwst1 TEXT,
                                                    mwst2 TEXT,
                                                    mwst3 TEXT
                                                    )""")
                cursor.execute("""CREATE TABLE kontenplan ( 
                                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    superkonto TEXT,
                                                    subsuperkonto TEXT,
                                                    kontoname TEXT, 
                                                    kontonummer TEXT
                                                    )""")
            except:
                pass
            cursor.execute('''INSERT INTO mandant (name, adresse, mwst1, mwst2, mwst3) 
                                VALUES (?,?,?,?,?)''', [self.mand_name.text(), 
                                                        self.mand_address.toPlainText(), 
                                                        self.mwst1.text(), 
                                                        self.mwst2.text(), 
                                                        self.mwst3.text()])
            connection.commit()
            self.wizard_done.emit()

class SB(QtGui.QDialog, Ui_sb_dialog):
    def __init__(self, parent=None):
        super(SB, self).__init__(parent)
        self.setupUi(self)

class Kontenplan(QtGui.QDialog, Ui_Kontenplan):
    update = Signal()
    def __init__(self, parent=None):
        super(Kontenplan, self).__init__(parent)
        self.setupUi(self)
        cursor = connection.cursor()
        cursor2 = connection.cursor()
        self.UpdateKontenplan()
        self.new_kto_btn.clicked.connect(self.newKonto)
    def newKonto(self):
        newkonto = NewKonto(self)
        newkonto.addKonto.connect(self.UpdateKontenplan)
        newkonto.show()
    def UpdateKontenplan(self):
        try:
            self.verticalLayout.removeWidget(self.kontenplan)
        except AttributeError:
            pass
        # Saldobestimmung für Kontenplan
        konten = cursor.execute("SELECT * FROM kontenplan")
        kontenstring = list()
        for row in konten:
            neuer_saldo = '0.0'
            statement = 'SELECT saldo FROM "%s"' % row[4]
            saldo = cursor2.execute(statement)
            for saldi in saldo:
                neuer_saldo = saldi[0]
            kontenstring.append(row[1]+'*'+row[2]+'*'+row[3]+'*'+row[4]+'*'+neuer_saldo)
        self.kontenplan = TreeOfTableWidget(kontenstring, 2, '*')
        headers = ['Kontoname', 'Kontonummer', 'Saldo']
        self.kontenplan.model().headers = headers
        self.kontenplan.expandAll()
        self.kontenplan.resizeColumnToContents(0)
        self.kontenplan.resizeColumnToContents(1)
        #self.verticalLayout.removeWidget(self.kontenplan)
        self.verticalLayout.addWidget(self.kontenplan)
        self.update.emit()

class ServerModel(treeoftable.TreeOfTableModel):
    def __init__(self, parent=None):
        super(ServerModel, self).__init__(parent)
    def data(self, index, role):
        if role == Qt.DecorationRole:
            node = self.nodeFromIndex(index)
        return treeoftable.TreeOfTableModel.data(self, index, role)

class TreeOfTableWidget(QTreeView):
    def __init__(self, filename, nesting, separator, parent=None):
        super(TreeOfTableWidget, self).__init__(parent)
        self.setSelectionBehavior(QTreeView.SelectRows)
        self.setUniformRowHeights(True)
        model = ServerModel(self)
        self.setModel(model)
        #try:
        model.load(filename, nesting, separator)
        #except IOError, e:
        #    QMessageBox.warning(self, "Server Info - Error", unicode(e))
        self.connect(self, SIGNAL("activated(QModelIndex)"), lambda: self.activated(QModelIndex()))
        self.connect(self, SIGNAL("expanded(QModelIndex)"), self.expanded)
        self.expanded()


    def currentFields(self):
        return self.model().asRecord(self.currentIndex())


    def activated(self, index):
        self.emit(SIGNAL("activated"), self.model().asRecord(index))


    def expanded(self):
        for column in range(self.model().columnCount(
                            QModelIndex())):
            self.resizeColumnToContents(column)

class Kontoauszug(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Kontoauszug, self).__init__(parent)
        self.setupUi(self)
        
    def getWrite(self, konto, kontoname):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(fname)
        
        db.open()
        model = QSqlTableModel()
        model.setTable('"'+konto+'"')
        model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        #model.setFilter("soll_kto="+konto+" OR haben_kto="+konto)
        model.select()
        filtering = QSortFilterProxyModel(self)
        filtering.setSourceModel(model)

        #print filtering
        #model.setHeaderData(2, QtCore.Qt.Horizontal, "Datum")
        #model.setHeaderData(1, QtCore.Qt.Horizontal, "Belegnummer")
        #model.setHeaderData(3, QtCore.Qt.Horizontal, "Soll-Konto")
        #model.setHeaderData(4, QtCore.Qt.Horizontal, "Haben-Konto")
        #model.setHeaderData(6, QtCore.Qt.Horizontal, "Nettobetrag")
        #model.setHeaderData(7, QtCore.Qt.Horizontal, "Buchungstext")
        view = QTableView()
        view.setModel(filtering)
        view.setColumnHidden(0, True)
        #view.setColumnHidden(5, True)
        #view.setColumnHidden(8, True)
        view.setSelectionBehavior(QTableView.SelectRows)
        self.horizontalLayout.addWidget(view)
        self.kontoname.setText(konto+' - '+kontoname)
        self.print_btn.clicked.connect(lambda: self.createAuszug([konto, kontoname]))
        #rows = self.tableWidget.rowCount()
        #self.tableWidget.setRowCount(rows+1)
        #self.tableWidget.setItem(0,0,QTableWidgetItem('iii'))
        #self.label.setText(konto)
        
    def createAuszug(self, konto):
        doc = meteorpdf.Pdf('Kontoauszug', '')
        doc.set_theme(MyTheme)
        doc.add_header('Kontoauszug', meteorpdf.H2)
        doc.add_spacer()
        buchungen_table = [['Datum', 'Belegnr.', 'Text', 'Gegenkonto', 'Soll', 'Haben', 'Saldo']] # this is the header row 
        statement = 'SELECT * FROM "%s"' %konto[0]
        cursor = connection.cursor()
        result = cursor.execute(statement)
        total_soll = 0.00
        total_haben = 0.00
        soll_cell = 0.00
        haben_cell = 0.00
        saldo_cell = 0.00
        for row in result:
            soll_cell = row[5]
            haben_cell = row[6]
            saldo_cell = row[7]
            if soll_cell != '':
                soll_cell = '%.2f' % float(soll_cell)
            if haben_cell != '':
                haben_cell = '%.2f' % float(haben_cell)
            if saldo_cell != '':
                saldo_cell = '%.2f' % float(saldo_cell)
                if float(saldo_cell) < 0.0:
                    saldo_cell = '%.2f' % float(saldo_cell)
            buchungen_table.append(list(row[1:5])+[soll_cell,haben_cell, saldo_cell])
            try:
                total_soll = total_soll + float(row[5])
            except ValueError:
                total_soll = total_soll
            try:
                total_haben = total_haben + float(row[6])
            except ValueError:
                total_haben = total_haben
        doc.add_header(konto[1]+' - '+konto[0], meteorpdf.H5)
        buchungen_table.append(['Summe Bewegungen:','','','','%.2f' % total_soll,'%.2f' % total_haben , saldo_cell]) 
        doc.add_table_auszug(buchungen_table, TABLE_WIDTH)
        document = doc.render()
        outfile = open('test.pdf', 'w')
        outfile.write(document)
        outfile.close()
        os.system('xdg-open test.pdf')

class NewKonto(QtGui.QDialog, Ui_new_kto):
    addKonto = Signal()
    def __init__(self, parent=Kontenplan):
        super(NewKonto, self).__init__(parent)
        self.setupUi(self)
        self.comboBox.activated.connect(self.choice)
        self.buttonBox.accepted.connect(self.writeToDB)
        
    def choice(self):
        self.comboBox_2.clear()
        if self.comboBox.currentText() == 'Aktiven':
            subitems = self.aktivas()
        elif self.comboBox.currentText() == 'Passiven':
            subitems = self.passivas()
        elif self.comboBox.currentText() == 'Aufwand':
            subitems = self.aufwand()
        elif self.comboBox.currentText() == 'Ertrag':
            subitems = self.ertrag()
        for item in subitems:
            self.comboBox_2.addItem(item)
    def aktivas(self):
        subitems = [u'Umlaufvermögen', u'Anlagevermögen']
        return subitems
    def passivas(self):
        subitems = [u'Fremdkapital', 'Eigenkapital']
        return subitems
    def aufwand(self):
        subitems = [u'Leistungen', 'Material / Warenaufwand', 'Personalaufwand', 'Sonstiger Betriebsaufwand']
        return subitems
    def ertrag(self):
        subitems = ['Betr. Nebenerfolge', 'Neutraler Erfolg']
        return subitems
    def writeToDB(self):
        statement = 'CREATE TABLE "%s" (id INTEGER PRIMARY KEY AUTOINCREMENT, datum TEXT,belegnr TEXT,buchungstext TEXT,gegenkonto TEXT, soll TEXT,haben TEXT,saldo TEXT)' % self.kto_nr.text()
        cursor.execute(statement)
        statement = 'INSERT INTO kontenplan (superkonto, subsuperkonto, kontoname, kontonummer) VALUES ("%s", "%s", "%s", "%s")' % (self.comboBox.currentText(), self.comboBox_2.currentText(), self.kto_name.text(), self.kto_nr.text())
        
        cursor.execute(statement)
        statement = 'INSERT INTO "%s" (buchungstext, saldo) VALUES ("%s", "%s")' % (self.kto_nr.text(), "Anfangssaldo", self.saldo.text())
        connection.commit()
        self.addKonto.emit()

class MyTheme(DefaultTheme):
        doc = {
            'leftMargin': 35,
            'rightMargin': 35,
            'topMargin': 30,
            'bottomMargin': 35,
            'allowSplitting': False
            }
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Accounting()
    window.show()
    sys.exit(app.exec_())