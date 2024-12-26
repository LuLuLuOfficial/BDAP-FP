import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QComboBox, QLabel, QGridLayout
from PySide6.QtGui import QFont

from Data.Lib.LucasClass.LucasLogManager import LogManager
from Data.Lib.LucasFunc.LucasFunc import PathCheck, GetFileList

from Data.Lib.Windows.WinError import WinError
from Data.Lib.Windows.WinChart import WinChart

class WinMain(QWidget):
    def __init__(self, LogManage: LogManager):
        super().__init__()
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

        self.LogManage.LogOutput(Type='WinMain', LogMassage='WinMain Initialize Complete.')

    def Window_Config(self):
        self.setWindowTitle("PySide6 基础示例")
        self.setFixedSize(428, 220)

    def Widget_Create(self):
        self.List_Label: list[QLabel] = []
        for n in range(2): self.List_Label.append(QLabel())

        self.List_TextBox: list[QLineEdit] = []
        for n in range(1): self.List_TextBox.append(QLineEdit())

        self.List_ComboBox: list[QComboBox] = []
        for n in range(1): self.List_ComboBox.append(QComboBox())

        self.List_Button: list[QPushButton] = []
        for n in range(1): self.List_Button.append(QPushButton())

    def Widget_Config(self):
        self.List_Label[0].setText('数据图表化')
        self.List_Label[0].setFont(QFont("微软雅黑", 20, QFont.Bold))
        self.List_Label[0].setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.List_Label[0].setStyleSheet("background-color: blue; color: white; padding: 10px;")
        self.List_Label[0].setFixedSize(200, 60)

        self.List_Label[1].setText('Excel路径:')
        self.List_Label[1].setFont(QFont("微软雅黑", 10))
        self.List_Label[1].setAlignment(Qt.AlignmentFlag.AlignBottom)
        # self.List_Label[1].setStyleSheet("background-color: blue; color: white; padding: 10px;")
        self.List_Label[1].setFixedSize(200, 40)

        self.List_TextBox[0].setFixedSize(405, 40)
        self.List_TextBox[0].setPlaceholderText('在此键入Excel文件路径...')

        self.List_ComboBox[0].addItem('选择 Excel 文件 ↓')
        self.List_ComboBox[0].addItems(list(self.ExcelList.keys()))
        self.List_ComboBox[0].setFixedSize(200, 40)

        self.List_Button[0].setText('Confirm')
        self.List_Button[0].setFixedSize(200, 40)

    def Widget_Connect(self): 
        self.List_ComboBox[0].currentIndexChanged.connect(self.ComboBoxSelect)
        self.List_Button[0].clicked.connect(self.Confirm)

    def Layout_Set(self):
        Layout = QGridLayout()

        Layout.addWidget(self.List_Label[0], 0, 1, 1, 2)
        Layout.addWidget(self.List_Label[1], 1, 0, 1, 2)
        Layout.addWidget(self.List_TextBox[0], 2, 0, 1, 4)
        Layout.addWidget(self.List_ComboBox[0], 3, 0, 1, 2)
        Layout.addWidget(self.List_Button[0], 3, 2, 1, 2)
        Layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(Layout)

    def ComboBoxSelect(self, index):
        if index == 0:
            self.List_TextBox[0].setText('')
            return
        SelectedItem = self.List_ComboBox[0].currentText()
        self.List_TextBox[0].setText(self.ExcelList[SelectedItem])

    def Confirm(self):
        SelectedItem = self.List_TextBox[0].text()
        self.LogManage.LogOutput(Type='WinMain', LogMassage=f'Selected Item -> <{SelectedItem}>.')

        if SelectedItem and PathCheck(SelectedItem):
            _WinChart = WinChart(self.LogManage, SelectedItem)
            _WinChart.show()
        else:
            _WinError = WinError(self.LogManage, '\t路径错误:\n      不存在的文件路径, 请检查路径是否正确填写或检查文件存在性, 并重新尝试.')
            _WinError.exec()

if __name__ == "__main__":
    LogManage: LogManager = LogManager(r'Log')

    app = QApplication(sys.argv)
    window = WinMain(LogManage=LogManage)
    window.show()
    sys.exit(app.exec())
