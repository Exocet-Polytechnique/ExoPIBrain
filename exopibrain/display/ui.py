import sys
import threading
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

    def __init__(self, qta_id, values=[0], prefixes=[""], unit="", final_stretch=True):
        super(QtWidgets.QWidget, self).__init__()
        self.qta_id = qta_id
        self.values = values
        self.prefixes = prefixes
        self.unit = unit
        self.data_labels = []
        font = 50 / len(self.values)
        self.setFont(QtGui.QFont("Arial", int(font)))

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        icon = QtWidgets.QLabel()
        icon.setPixmap(qta.icon(self.qta_id).pixmap(self.IconSize))

        layout.addWidget(icon)
        layout.addSpacing(self.HorizontalSpacing)

        v_layout = QVBoxLayout()
        for i, value in enumerate(self.values):
            data_label = QtWidgets.QLabel(f"{prefixes[i]} {value} {unit}")
            self.data_labels.append(data_label)
            v_layout.addWidget(data_label)
        layout.addLayout(v_layout)

        if final_stretch:
            layout.addStretch()

    def update(self, new_values):
        self.values = new_values
        for i, v in new_values:
            self.data_labels[i].setText(f"{self.prefixes[i]} {v} {self.unit}")

class MyWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.time = TimeWidget()

        self.speed = DataWidget("fa5s.tachometer-alt", unit="km/h")

        self.temp = DataWidget("fa5s.thermometer-half", values=[0,0,0], prefixes=["fc_a", "fc_b", "batt"], unit="°C")

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

class GUI(object):
    """
    https://stackoverflow.com/questions/49971584/updating-pyqt5-gui-with-live-data
    """
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.widget = MyWidget()
        self.widget.resize(800, 600)
        self.widget.show()

    def run(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    gui = GUI()
    gui.run()
    #gui.join()