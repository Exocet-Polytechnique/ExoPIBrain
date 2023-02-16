import sys
from PySide6 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        currentTime = QtCore.QTime.currentTime()

        self.time = QtWidgets.QLabel(currentTime.toString())
        self.time.setFont(QtGui.QFont('Arial', 100))

        self.speed = QtWidgets.QLabel("Vitesse")
        self.speed.setFont(QtGui.QFont('Arial', 50))

        self.temp = QtWidgets.QLabel("Température")
        self.temp.setFont(QtGui.QFont('Arial', 50))

        self.autonomy = QtWidgets.QLabel("Autonomie")
        self.autonomy.setFont(QtGui.QFont('Arial', 50))

        self.pressure = QtWidgets.QLabel("Pression")
        self.pressure.setFont(QtGui.QFont('Arial', 50))

        self.consummation = QtWidgets.QLabel("Consommation")
        self.consummation.setFont(QtGui.QFont('Arial', 50))
        
        self.tank = QtWidgets.QLabel("H2 restant")
        self.tank.setFont(QtGui.QFont('Arial', 50))
        

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.time)
        self.layout.addWidget(self.speed)
        self.layout.addWidget(self.temp)
        self.layout.addWidget(self.autonomy)
        self.layout.addWidget(self.pressure)
        self.layout.addWidget(self.consummation)
        self.layout.addWidget(self.tank)
        



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())