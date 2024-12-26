import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QPushButton, QLabel, QGridLayout, QDialog
from PySide6.QtGui import QFont

from Data.Lib.LucasClass.LucasLogManager import LogManager
from Data.Lib.LucasFunc.LucasFunc import  GetFileList

class WinError(QDialog):
    def __init__(self, LogManage: LogManager, Message: str):
        super().__init__()
        self.ErrorMessage: str = Message
        self.Basic_Config(LogManage)
        self.Initialize()

    def Basic_Config(self, LogManage: LogManager):
        self.LogManage: LogManager = LogManage
        self.ExcelList: dict = GetFileList('.xlsx', 'Data\Excels')

    def Initialize(self):
        self.Window_Config()
        self.Widget_Create()
        self.Widget_Config()
        self.Widget_Connect()
        self.Layout_Set()

        self.LogManage.LogOutput(Type='WinError', LogMassage='WinMain Initialize Complete.')

    def Window_Config(self):
        self.setWindowTitle("PySide6 基础示例")
        self.setFixedSize(428, 234)

    def Widget_Create(self):
        self.List_Label: list[QLabel] = []
        for n in range(2): self.List_Label.append(QLabel())

        self.List_Button: list[QPushButton] = []
        for n in range(2): self.List_Button.append(QPushButton())

    def Widget_Config(self):
        self.List_Label[0].setText('Error')
        self.List_Label[0].setFont(QFont("微软雅黑", 20, QFont.Bold))
        self.List_Label[0].setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.List_Label[0].setStyleSheet("background-color: blue; color: white; padding: 10px;")
        self.List_Label[0].setFixedSize(200, 60)

        self.List_Label[1].setText(self.ErrorMessage)
        self.List_Label[1].setFont(QFont("微软雅黑", 10))
        self.List_Label[1].setAlignment(Qt.AlignmentFlag.AlignTop)
        self.List_Label[1].setWordWrap(True)
        # self.List_Label[1].setStyleSheet("background-color: blue; color: white; padding: 10px;")
        self.List_Label[1].setFixedSize(400, 100)

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
        Layout.addWidget(self.List_Label[1], 1, 0, 2, 4)
        Layout.addWidget(self.List_Button[0], 3, 0, 1, 2)
        Layout.addWidget(self.List_Button[1], 3, 2, 1, 2)
        Layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(Layout)

    def Cancel(self):
        self.close()

    def Confirm(self):
        self.close()

if __name__ == "__main__":
    LogManage: LogManager = LogManager(r'Log')

    app = QApplication(sys.argv)
    window = WinError(LogManage=LogManage, Message='\t测试:\n        测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试')
    window.show()
    sys.exit(app.exec())
