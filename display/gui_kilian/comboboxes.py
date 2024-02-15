import sys
from PyQt5.QtWidgets import *

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)

        mainLayout = QGridLayout()
        

        # Tab 1.1
        self.tab1_1 = QWidget()
        self.tab1_1.layout = QVBoxLayout()
        self.tab1_1.layout.addWidget(QLabel('<font size = 8><b>Type something </font'))

        self.lineEdit = QLineEdit()
        self.btn_print = QPushButton('Print')
        self.btn_print.clicked.connect(self.typesomething)
        self.tab1_1.layout.addWidget(self.lineEdit)
        self.tab1_1.layout.addWidget(self.btn_print)

        self.tab1_1.setLayout(self.tab1_1.layout)

        # Tab 1.2
        self.btn = QPushButton('A button')
        self.btn.clicked.connect(lambda : print("Hello World!"))

        self.tab1_2 = QWidget()
        self.tab1_2.layout = QVBoxLayout()
        self.tab1_2.layout.addWidget(self.btn)
        self.tab1_2.setLayout(self.tab1_2.layout)

        # Tab 1 parent
        self.tabs1 = QTabWidget()
        self.tabs1.addTab(self.tab1_1, 'Tab 1.1')
        self.tabs1.addTab(self.tab1_2, 'Tab 1.2')

        # Tab 2 parent
        self.btn2 = QPushButton('B button')
        self.btn2.clicked.connect(lambda : print('B button clicked'))

        self.tabs2 = QTabWidget()
        self.tabs2.addTab(self.btn2, 'Tab 2')

        mainLayout.addWidget(self.tabs1, 0, 0)
        mainLayout.addWidget(self.tabs2, 0, 1)
        self.setLayout(mainLayout)

    def typesomething(self):
        print(self.lineEdit.text())
app = QApplication(sys.argv)

demo = AppDemo()
demo.show()

sys.exit(app.exec())