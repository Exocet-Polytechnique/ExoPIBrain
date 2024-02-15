from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * # make sure to have PyQT5 install on your device
from PyQt5.QtGui import QFont # import the fonts
import time
import sys

class SpeedWidget(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Arial", 70))
        self.setText("Vitesse : ... km/h")

class TemperatureWidget(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Arial", 70))
        self.setText("Temperature : ... °C")

class NiveauBatterie(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Arial", 70))
        self.setText("Niveau de batterie : ... %")

class MyWindow(QWidget):
    # define our window
    def __init__(self):
        super().__init__()
        self.resize(1920, 1080)
        self.initUI()

    # contain everything our window needs to have
    def initUI(self):
        mainLayout = QGridLayout()
        self.vitesse = SpeedWidget()
        self.temperature = TemperatureWidget()
        self.niveauBatterie = NiveauBatterie()

        mainLayout.addWidget(self.vitesse, 0, 0)
        mainLayout.addWidget(self.temperature, 1, 0)
        mainLayout.addWidget(self.niveauBatterie, 2, 0)
        
        self.setLayout(mainLayout)
        

def main():
    app = QApplication(sys.argv)
    window = MyWindow()

    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()