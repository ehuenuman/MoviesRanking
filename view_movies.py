#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore
from mainWindow import Ui_MainWindow
import controller

class Movies(QtGui.QMainWindow):
    """Clase principal del programa"""
    table_columns =(
        (u"Titulo",100),
        (u"Director",150),
        (u"Pais",100),
        (u"Ranking",75) )

    def __init__(self):
        """Cosntructor del programa"""
        super(Movies, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.centerWindow()
        self.loadMovies()
        self.setSignals()
        self.show()

    def centerWindow(self):
        """Funcion que centra la interfaz grafica en la pantalla"""
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def loadMovies(self):
        """Funcion que carga la base de datos en la interfaz"""
        movies = controller.obtener_movies()
        row = len(movies)
        model = QtGui.QStandardItemModel(
            row, len(self.table_columns))
        self.ui.tableView.setModel(model)
        self.ui.tableView.horizontalHeader().setResizeMode(0,
            self.ui.tableView.horizontalHeader().Stretch)

        for col, h in enumerate(self.table_columns):
            model.setHeaderData(col, QtCore.Qt.Horizontal, h[0])
            self.ui.tableView.setColumnWidth(col, h[1])

        for i, data in enumerate(movies):
            row = [data[1], data[4], data[5], data[8]]
            for j, field in enumerate(row):
                index = model.index(i, j, QtCore.QModelIndex())
                model.setData(index, field)

    def setSignals(self):
        self.ui.tableView.clicked.connect(self.infoMovies)
        self.ui.likeButton.clicked.connect(self.rankingUp)
        self.ui.unlikeButton.clicked.connect(self.rankingDown)

    def infoMovies(self):
        index = self.ui.tableView.currentIndex()
        model = self.ui.tableView.model()
        codigo = model.index(index.row(), 3, QtCore.QModelIndex()).data()
        pelicula = controller.infoFila(codigo)

        direccion = "imgCine/{0}".format(pelicula[1])
        self.ui.imgLabel.setPixmap(QtGui.QPixmap(direccion))

        title = "{0} \n{1}, {2}".format(pelicula[0], pelicula[2], pelicula[3])
        self.ui.titleLabel.setText(title)

        plot = pelicula[6]
        self.ui.infoLabel.setText(plot)

        starring = pelicula[5].split("|")
        self.ui.starringLabel.setText(starring[0])

    def rankingUp(self):
        index = self.ui.tableView.currentIndex()
        if index.row() == -1:  # No se ha seleccionado una fila
            errorQMessageBox = QtGui.QMessageBox()
            errorQMessageBox.setWindowTitle("ERROR!")
            errorQMessageBox.setText("Debe seleccionar una fila")
            errorQMessageBox.exec_()
        else:
            model = self.ui.tableView.model()
            index = self.ui.tableView.currentIndex()
            codigo = model.index(index.row(), 3, QtCore.QModelIndex()).data()
            if (codigo != 1):
                codigo2 = model.index(index.row()-1, 3, QtCore.QModelIndex()).data()
                valores = controller.infoFila(codigo)
                valores2 = controller.infoFila(codigo2)
                controller.subir(codigo, valores2)
                controller.subir(codigo2, valores)
            else:
                errorQMessageBox = QtGui.QMessageBox()
                errorQMessageBox.setWindowTitle("ERROR!")
                errorQMessageBox.setText(u"Esta pelicula no puede subir más")
                errorQMessageBox.exec_()

        self.loadMovies()

    def rankingDown(self):
        index = self.ui.tableView.currentIndex()
        if index.row() == -1:  # No se ha seleccionado una fila
            errorQMessageBox = QtGui.QMessageBox()
            errorQMessageBox.setWindowTitle("ERROR!")
            errorQMessageBox.setText("Debe seleccionar una fila")
            errorQMessageBox.exec_()
        else:
            model = self.ui.tableView.model()
            index = self.ui.tableView.currentIndex()
            codigo = model.index(index.row(), 3, QtCore.QModelIndex()).data()
            if (codigo != 7):
                codigo2 = model.index(index.row()+1, 3, QtCore.QModelIndex()).data()
                valores = controller.infoFila(codigo)
                valores2 = controller.infoFila(codigo2)
                controller.subir(codigo, valores2)
                controller.subir(codigo2, valores)
            else:
                errorQMessageBox = QtGui.QMessageBox()
                errorQMessageBox.setWindowTitle("ERROR!")
                errorQMessageBox.setText(u"La pelicula esta al tope de lo profundo")
                errorQMessageBox.exec_()

        self.loadMovies()


if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    main = Movies()
    sys.exit(app.exec_())
