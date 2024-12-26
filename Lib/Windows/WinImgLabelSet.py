import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QPushButton, QLabel, QGridLayout, QDialog, QLineEdit
from PySide6.QtGui import QFont

from Data.Lib.LucasClass.LucasLogManager import LogManager

from Data.Lib.Windows.WinArgsPasser import WinArgsPasser

class WinImgLabelSet(QDialog):
    def __init__(self, LogManage: LogManager, WinArgsPass: WinArgsPasser, Tittle: str):
        super().__init__()
        

        self.Basic_Config(LogManage, WinArgsPass, Tittle)
        self.Initialize()

    def Basic_Config(self, LogManage: LogManager, WinArgsPass: WinArgsPasser, Tittle: str):
        self.LogManage: LogManager = LogManage
        self.WinArgsPass: WinArgsPasser = WinArgsPass

        self.Tittle: str = Tittle

    def Initialize(self):
        self.Window_Config()
        self.Widget_Create()
        self.Widget_Config()
        self.Widget_Connect()
        self.Layout_Set()

        self.LogManage.LogOutput(Type='WinImgLabelSet', LogMassage='WinImgLabelSet Initialize Complete.')

    def Window_Config(self):
        self.setWindowTitle("PySide6 基础示例")
        self.setFixedSize(428, 234)

    def Widget_Create(self):
        self.List_Label: list[QLabel] = []
        for n in range(3): self.List_Label.append(QLabel())

        self.List_TextBox: list[QLineEdit] = []
        for n in range(2): self.List_TextBox.append(QLineEdit())

        self.List_Button: list[QPushButton] = []
        for n in range(2): self.List_Button.append(QPushButton())

    def Widget_Config(self):
        self.List_Label[0].setText(self.Tittle)
        self.List_Label[0].setFont(QFont("微软雅黑", 20, QFont.Bold))
        self.List_Label[0].setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.List_Label[0].setStyleSheet("background-color: blue; color: white; padding: 10px;")
        self.List_Label[0].setFixedSize(200, 60)

        self.List_Label[1].setText('X轴标签:')
        self.List_Label[1].setFont(QFont("微软雅黑", 10))
        self.List_Label[1].setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.List_Label[1].setWordWrap(True)
        # self.List_Label[1].setStyleSheet("background-color: blue; color: white; padding: 10px;")
        self.List_Label[1].setFixedSize(100, 35)

        self.List_Label[2].setText('Y轴标签:')
        self.List_Label[2].setFont(QFont("微软雅黑", 10))
        self.List_Label[2].setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.List_Label[2].setWordWrap(True)
        # self.List_Label[2].setStyleSheet("background-color: blue; color: white; padding: 10px;")
        self.List_Label[2].setFixedSize(100, 35)

        self.List_TextBox[0].setPlaceholderText('在此键入X轴标签...')
        self.List_TextBox[0].setText(self.WinArgsPass.Tittle_XY[0])
        self.List_TextBox[0].setFixedSize(200, 40)
        
        self.List_TextBox[1].setPlaceholderText('在此键入Y轴标签...')
        self.List_TextBox[1].setText(self.WinArgsPass.Tittle_XY[1])
        self.List_TextBox[1].setFixedSize(200, 40)

        self.List_Button[0].setText('Cancel')
        self.List_Button[0].setFixedSize(200, 40)

        self.List_Button[1].setText('Confirm')
        self.List_Button[1].setFixedSize(200, 40)

    def Widget_Connect(self): 
        self.List_Button[0].clicked.connect(self.Cancel)
        self.List_Button[1].clicked.connect(self.Confirm)

    def Layout_Set(self):
        Layout = QGridLayout()

        Layout.addWidget(self.List_Label[0], 0, 1, 1, 2)
        Layout.addWidget(self.List_Label[1], 1, 0, 1, 1)
        Layout.addWidget(self.List_Label[2], 1, 2, 1, 1)
        Layout.addWidget(self.List_TextBox[0], 2, 0, 1, 2)
        Layout.addWidget(self.List_TextBox[1], 2, 2, 1, 2)
        Layout.addWidget(self.List_Button[0], 3, 0, 1, 2)
        Layout.addWidget(self.List_Button[1], 3, 2, 1, 2)
        Layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(Layout)

    def Cancel(self):
        self.WinArgsPass.Tittle_XY[2] = False
        self.close()

    def Confirm(self):
        self.WinArgsPass.Tittle_XY = [self.List_TextBox[0].text(), self.List_TextBox[1].text(), True]
        self.close()

if __name__ == "__main__":
    LogManage: LogManager = LogManager(r'Log')
    WinArgsPass: WinArgsPasser = WinArgsPasser()

    app = QApplication(sys.argv)
    window = WinImgLabelSet(LogManage=LogManage, WinArgsPass=WinArgsPass, Tittle='BarChart')
    window.show()
    sys.exit(app.exec())
