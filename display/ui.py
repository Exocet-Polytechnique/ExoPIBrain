import sys
import qtawesome as qta
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout

class TimeWidget(QtWidgets.QLabel):
    """
    Simple widget to display current time, based on
    https://www.geeksforgeeks.org/pyqt5-create-a-digital-clock/
    """
    def __init__(self):
        super().__init__()
        self.setFont(QtGui.QFont("Arial", 100))

    def show_time(self):
        # getting current time
        current_time = QtCore.QTime.currentTime()
        # converting QTime object to string
        label_time = current_time.toString('hh:mm:ss')
        # showing it to the label
        self.setText(label_time)


class DataWidget(QtWidgets.QWidget):

    IconSize = QtCore.QSize(196, 196)
    HorizontalSpacing = 2

    def __init__(self, qta_id, values=[0], prefixes=[""], unit="", final_stretch=True):
        """
        qta_id (str): The id of the icon to display.
        values (list): The values to display.
        prefixes (list): The prefixes to display before each value.
        unit (str): The unit to display after each value.
        final_stretch (bool): Whether to add a stretch at the end of the layout.
        """
        super(QtWidgets.QWidget, self).__init__()
        self.qta_id = qta_id
        self.values = values
        self.prefixes = prefixes
        self.unit = unit
        self.data_labels = []
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.icon = QtWidgets.QLabel()
        self.icon.setPixmap(qta.icon(self.qta_id).pixmap(self.IconSize))

        layout.addWidget(self.icon)
        layout.addSpacing(self.HorizontalSpacing)

        v_layout = QVBoxLayout()
        font_size = 50 if len(self.values) == 1 else 30
        for i, value in enumerate(self.values):
            data_label = QtWidgets.QLabel(f"{prefixes[i]} {value} {unit}")
            data_label.setFont(QtGui.QFont("Arial", font_size))
            self.data_labels.append(data_label)
            v_layout.addWidget(data_label)
        layout.addLayout(v_layout)

        if final_stretch:
            layout.addStretch()

    def update(self, new_values):
        """
        new_values (list): The new values to display.
        """
        self.values = new_values
        for i, v in enumerate(new_values):
            self.data_labels[i].setText(f"{self.prefixes[i]} {v:.1f} {self.unit}")

class EfficiencyWidget(DataWidget):
    ICON_NAME = "fa5s.leaf"
    EFFICIENCY_TOLERANCE = 0.1
    def __init__(self, value, final_stretch=False):
        """
        Displays the efficiency of the fuel cell to guide the throttle
        value (float): The initial value to display.
        final_stretch (bool): Whether to add a stretch at the end of the layout.
        """
        super().__init__("fa5s.leaf", values=[value], unit="%", final_stretch=final_stretch) 

    def update(self, new_value):
        """
        Updates the displayed efficiency.
        new_value (float): The new value to display.
        """
        self.values = [new_value]
        sign = '+' if new_value > 0 else ''
        self.data_labels[0].setText(f"{sign}{new_value:.1f} {self.unit}")
        if -self.EFFICIENCY_TOLERANCE < new_value < self.EFFICIENCY_TOLERANCE:
            new_color = "green"
        else:
            new_color = "red"
        self.icon.setPixmap(qta.icon(self.qta_id, color=new_color).pixmap(self.IconSize))
        

class MyWidget(QtWidgets.QMainWindow):
    ALERT_COLOR = "red"
    WARNING_COLOR = "yellow"
    BG_COLOR= "white"
    assert_signal = QtCore.pyqtSignal(str)
    def __init__(self):
        """
        This class is the main window of the GUI.
        """
        super().__init__()
        self.time = TimeWidget()
        self.eff_widget = EfficiencyWidget(0.0)
        self.speed = DataWidget("fa5s.tachometer-alt", unit="km/h")
        self.temp = DataWidget("fa5s.thermometer-half", values=[0,0,0], prefixes=["fc_a", "fc_b", "batt"], unit="°C")
        self.autonomy = DataWidget("fa5s.battery-half", unit="km")
        self.pressure = DataWidget("fa5s.compress-arrows-alt", unit="bar")
        self.power = DataWidget("fa5s.bolt", unit="W")
        self.tank = DataWidget("fa5s.spray-can", unit="L")

        self.assert_signal.connect(self.handle_alert)

        self.setStyleSheet(f"background-color: {self.BG_COLOR};")
        layout1 = QGridLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        top_layout = QHBoxLayout()
        layout1.setContentsMargins(0,0,0,0)
        top_layout.addWidget(self.time)
        top_layout.addWidget(self.eff_widget)
        layout1.addLayout(top_layout, 0,0)
        layout2.addWidget(self.speed)
        layout2.addWidget(self.temp)
        layout2.addWidget(self.autonomy)
        layout1.addLayout(layout2, 1,0)
        layout3.addWidget(self.pressure)
        layout3.addWidget(self.power)
        layout3.addWidget(self.tank)
        layout1.addLayout(layout3,2,0)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)

    def handle_alert(self, assert_type=None):
        """
        When an alert is received, this method changes the background color of the GUI.
        assert_type (str): The type of alert to display.
        """
        if assert_type == "alert":
            self.setStyleSheet(f"background-color: {self.ALERT_COLOR};")
        elif assert_type == "warning":
            self.setStyleSheet(f"background-color: {self.WARNING_COLOR};")            
        

class GUI(object):
    """
    https://stackoverflow.com/questions/49971584/updating-pyqt5-gui-with-live-data
    """
    ASSERT_LIFETIME = 2

    def __init__(self):
        """
        This class is the main class of the GUI.
        """
        self.app = QtWidgets.QApplication([])
        self.widget = MyWidget()
        
        self.widget.resize(1920, 1080)
        self.widget.show()

        self.in_assert = False
        self.assert_counter = 0

        self.current_data = {"batt_temp": 0.0, "fca_temp": 0.0, "fcb_temp": 0.0, "speed": 0.0, "total_power": 0.0, "est_auto": 0.0, "total_tank": 0.0, "pressure": 0.0, "efficiency": 0.0} 
        timer = QtCore.QTimer(self.widget)
        timer.timeout.connect(self.update_widget)
        timer.start(1000)


    def update_data(self, **kwargs):
        """
        Updates the data to display.
        **kwargs (dict): The data to display.
        """
        self.current_data = {**self.current_data, **kwargs}

    def update_widget(self):
        """
        Updates the widget with the current data.
        """
        self.widget.time.show_time()
        self.widget.eff_widget.update(self.current_data["efficiency"])
        self.widget.speed.update([self.current_data["speed"]])
        self.widget.temp.update([self.current_data["fca_temp"], self.current_data["fcb_temp"], self.current_data["batt_temp"]])
        self.widget.pressure.update([self.current_data["pressure"]])
        self.widget.power.update([self.current_data["total_power"]])
        self.widget.tank.update([self.current_data["total_tank"]])
        self.widget.autonomy.update([self.current_data["est_auto"]])

        if self.in_assert:
            self.assert_counter += 1

        if self.assert_counter >= self.ASSERT_LIFETIME:
            self.assert_counter = 0
            self.in_assert = False
            self.widget.setStyleSheet(f"background-color: {self.widget.BG_COLOR};")

        
    def dispatch_alert(self, alert_type):
        """
        Dispatches an alert to the GUI. 
        alert_type (str): The type of alert to display.
        """
        self.in_assert = True
        self.widget.assert_signal.emit(alert_type)
        
    def run(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    gui = GUI()
    gui.run()