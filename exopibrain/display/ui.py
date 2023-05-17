import sys
import qtawesome as qta

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout

    

class TimeWidget(QtWidgets.QLabel):
    """
    https://www.geeksforgeeks.org/pyqt5-create-a-digital-clock/
    """
    def __init__(self):
        super().__init__()
        self.setFont(QtGui.QFont("Arial", 100))
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.show_time)
        timer.start(1000)
    def show_time(self):
        # getting current time
        current_time = QtCore.QTime.currentTime()
        # converting QTime object to string
        label_time = current_time.toString('hh:mm:ss')
        # showing it to the label
        self.setText(label_time)

class DataWidget(QtWidgets.QWidget):

    IconSize = QtCore.QSize(96, 96)
    HorizontalSpacing = 2


    def __init__(self, qta_id, value=0, unit="", final_stretch=True):
        super(QtWidgets.QWidget, self).__init__()
        self.qta_id = qta_id
        self.value = value
        self.unit = unit
        self.setFont(QtGui.QFont("Arial", 50))

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        icon = QtWidgets.QLabel()
        icon.setPixmap(qta.icon(self.qta_id).pixmap(self.IconSize))

        layout.addWidget(icon)
        layout.addSpacing(self.HorizontalSpacing)
        self.data_label = QtWidgets.QLabel(f"{value} {unit}")
        layout.addWidget(self.data_label)

        if final_stretch:
            layout.addStretch()

    def update(self, new_value):
        self.value = new_value
        self.data_label.setText(f"{self.value} {self.unit}")

class TemperatureWidget(DataWidget):
    def __init__(self, qta_id, value=0, unit="", final_stretch=True):
        super().__init__(qta_id, value, unit, final_stretch)

    def update(self, new_value):
        self.value = new_value
        self.data_label.setText(f"{self.value} {self.unit}")
class MyWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.time = TimeWidget()

        self.speed = DataWidget("fa5s.tachometer-alt", unit="km/h")

        self.temp = DataWidget("fa5s.thermometer-half", unit="°C")

        self.autonomy = DataWidget("fa5s.battery-half", unit="km")

        self.pressure = DataWidget("fa5s.tachometer-alt", unit="bar")

        self.consumption = DataWidget("fa5s.tachometer-alt", unit="L")
        
        self.tank = DataWidget("fa5s.tachometer-alt", unit="L")

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
        layout3.addWidget(self.consumption)
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