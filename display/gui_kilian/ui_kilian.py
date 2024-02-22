
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * # make sure to have PyQT5 install on your device
from PyQt5.QtGui import QFont # import the fonts
from PyQt5 import QtCore
import sys


class SpeedWidget(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Arial", 40))
        self.setStyleSheet("border: 1px solid;")
        self.data = 0.0 # default 0.0km/h
        self.afficher()

    def afficher(self):
        self.setText(f"Vitesse\n{self.data} km/h")
    
    def update(self, new_data):
        self.data = new_data
        self.afficher()

class TemperatureWidget(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Arial", 40))
        self.data = 25 # default 25°C
        self.afficher()

    def afficher(self):
        self.setText(f"Temperature\n{self.data} °C")

    def update(self, new_data):
        self.data = new_data
        self.afficher()

class TimeWidget(QtWidgets.QLabel):
    """
    Simple widget to display current time, based on
    https://www.geeksforgeeks.org/pyqt5-create-a-digital-clock/
    """
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Arial", 70))
        self.update()

    def update(self):
        # getting current time
        current_time = QtCore.QTime.currentTime()
        # converting QTime object to string
        label_time = current_time.toString('hh:mm:ss')
        # showing it to the label
        self.setText(label_time)

class NiveauBatterie(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Arial", 40))
        self.data = 100 # default 100%
        self.afficher()

    def afficher(self):
        self.setText(f"Niv. batterie\n{self.data} %")

    def update(self, new_data):
        self.data = new_data
        self.afficher()

class PressionH2(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Arial", 40))
        self.data = 2 # insert the default value
        self.afficher()

    def afficher(self):
        self.setText(f"Pression H2\n{self.data} kPa")

    def update(self, new_data):
        self.data = new_data
        self.afficher()

class ConsEnergie(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Arial", 40))
        self.data = 80
        self.afficher()

    def afficher(self):
        self.setText(f"Cons. Energie\n{self.data} %")

    def update(self, new_data):
        self.data = new_data
        self.afficher()

class MyWindow(QWidget):
    # define our window
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color : #222222; color : #FFF")
        self.initUI()

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.updateData)
        timer.timeout.connect(self.updateWidgets)
        timer.start(1000)

    # contain everything our window needs to have
    def initUI(self):
        mainLayout = QGridLayout()
        self.datas = {"vitesse" : 0.0, "temperature": 25, "batterie": 100} # put the default datas here
        self.vitesse = SpeedWidget()
        self.temperature = TemperatureWidget()
        self.time = TimeWidget()
        self.niveauBatterie = NiveauBatterie()
        self.pressionH2 = PressionH2()
        self.cons_energie = ConsEnergie()

        # mainLayout.addWidget(item, row, column, rowSpan, columnSpan)
        mainLayout.addWidget(self.temperature, 0, 0)
        mainLayout.addWidget(self.time, 0, 1)
        mainLayout.addWidget(self.niveauBatterie, 0, 2)
        mainLayout.addWidget(self.temperature, 1, 0, 0, 1)
        mainLayout.addWidget(self.vitesse, 1, 1)
        mainLayout.addWidget(self.pressionH2, 3, 0)
        mainLayout.addWidget(self.cons_energie, 3, 2)
        
        self.setLayout(mainLayout)

        # open the window in full screen
        self.showMaximized()

    # I consider that the datas that we receive are on a dictionnary
    # It can change without any problems
    def updateData(self):         
        self.datas["vitesse"] += 4
        self.datas["temperature"] += 1.5
        self.datas["batterie"] -= 2 
    
    def updateWidgets(self):
        self.vitesse.update(self.datas["vitesse"])
        self.temperature.update(self.datas["temperature"])
        self.niveauBatterie.update(self.datas["batterie"])
        self.time.update()

        



if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    window = MyWindow()

    window.show()
    
    sys.exit(app.exec_())