import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout
class DataWidget(QtWidgets.QLabel):
    def __init__(self, text):
        super().__init__(text=text)
        self.setFont(QtGui.QFont("Arial", 50))

class TimeWidget(QtWidgets.QLabel):
    def __init__(self, qtime):
        super().__init__(text=qtime.toString())
        self.setFont(QtGui.QFont("Arial", 100))
    
class MyWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.time = TimeWidget(QtCore.QTime.currentTime())

        self.speed = DataWidget("Vitesse")

        self.temp = DataWidget("Temperature")

        self.autonomy = DataWidget("Autonomie")

        self.pressure = DataWidget("Pression")

        self.consummation = DataWidget("Consommation")
        
        self.tank = DataWidget("H2 restant")
        
        layout1 = QGridLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        layout1.setContentsMargins(0,0,0,0)
        layout1.setSpacing(20)

        layout1.addWidget(self.time, 0, 0, 1, 3)

        layout2.addWidget(self.speed)
        layout2.addWidget(self.temp)
        layout2.addWidget(self.autonomy)
        layout1.addLayout(layout2, 1,0)
        layout3.addWidget(self.pressure)
        layout3.addWidget(self.consummation)
        layout3.addWidget(self.tank)
        layout1.addLayout(layout3,2,0)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())