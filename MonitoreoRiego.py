# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MonitoreoRiego.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MonitoreoRiego(object):
    def setupUi(self, MonitoreoRiego):
        MonitoreoRiego.setObjectName("MonitoreoRiego")
        MonitoreoRiego.resize(704, 452)
        self.centralwidget = QtWidgets.QWidget(MonitoreoRiego)
        self.centralwidget.setObjectName("centralwidget")
        self.temp_boton = QtWidgets.QPushButton(self.centralwidget)
        self.temp_boton.setGeometry(QtCore.QRect(40, 140, 131, 51))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Imag/caliente.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.temp_boton.setIcon(icon)
        self.temp_boton.setIconSize(QtCore.QSize(30, 30))
        self.temp_boton.setObjectName("temp_boton")
        self.tablaDatos = QtWidgets.QTableWidget(self.centralwidget)
        self.tablaDatos.setGeometry(QtCore.QRect(380, 100, 311, 311))
        self.tablaDatos.setObjectName("tablaDatos")
        self.tablaDatos.setColumnCount(3)
        self.tablaDatos.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tablaDatos.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablaDatos.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablaDatos.setHorizontalHeaderItem(2, item)
        self.humedad_boton = QtWidgets.QPushButton(self.centralwidget)
        self.humedad_boton.setGeometry(QtCore.QRect(190, 140, 131, 51))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Imag/humedad.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.humedad_boton.setIcon(icon1)
        self.humedad_boton.setIconSize(QtCore.QSize(30, 30))
        self.humedad_boton.setObjectName("humedad_boton")
        self.nivel_boton = QtWidgets.QPushButton(self.centralwidget)
        self.nivel_boton.setGeometry(QtCore.QRect(110, 210, 131, 51))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Imag/nivel-de-agua.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.nivel_boton.setIcon(icon2)
        self.nivel_boton.setIconSize(QtCore.QSize(30, 30))
        self.nivel_boton.setObjectName("nivel_boton")
        self.stop_boton = QtWidgets.QPushButton(self.centralwidget)
        self.stop_boton.setGeometry(QtCore.QRect(30, 310, 131, 51))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Imag/detener.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.stop_boton.setIcon(icon3)
        self.stop_boton.setIconSize(QtCore.QSize(30, 30))
        self.stop_boton.setObjectName("stop_boton")
        self.seleccione_label = QtWidgets.QLabel(self.centralwidget)
        self.seleccione_label.setGeometry(QtCore.QRect(10, 70, 621, 41))
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(10)
        self.seleccione_label.setFont(font)
        self.seleccione_label.setObjectName("seleccione_label")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 641, 51))
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Demi")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MonitoreoRiego.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MonitoreoRiego)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 704, 21))
        self.menubar.setObjectName("menubar")
        MonitoreoRiego.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MonitoreoRiego)
        self.statusbar.setObjectName("statusbar")
        MonitoreoRiego.setStatusBar(self.statusbar)

        self.retranslateUi(MonitoreoRiego)
        QtCore.QMetaObject.connectSlotsByName(MonitoreoRiego)

    def retranslateUi(self, MonitoreoRiego):
        _translate = QtCore.QCoreApplication.translate
        MonitoreoRiego.setWindowTitle(_translate("MonitoreoRiego", "Monitoreo de riego"))
        self.temp_boton.setText(_translate("MonitoreoRiego", "Temperatura"))
        item = self.tablaDatos.horizontalHeaderItem(0)
        item.setText(_translate("MonitoreoRiego", "Valor"))
        item = self.tablaDatos.horizontalHeaderItem(1)
        item.setText(_translate("MonitoreoRiego", "Fecha"))
        item = self.tablaDatos.horizontalHeaderItem(2)
        item.setText(_translate("MonitoreoRiego", "Hora"))
        self.humedad_boton.setText(_translate("MonitoreoRiego", "Humedad"))
        self.nivel_boton.setText(_translate("MonitoreoRiego", "Nivel de agua"))
        self.stop_boton.setText(_translate("MonitoreoRiego", "Detener"))
        self.seleccione_label.setText(_translate("MonitoreoRiego", "Seleccione la variable que desea que se despliegue en la tabla:"))
        self.label.setText(_translate("MonitoreoRiego", "Sistema de monitoreo y riego de una huerta."))
import Imagenes_rc