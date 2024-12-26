import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QComboBox, QGridLayout

from Data.Lib.LucasClass.LucasLogManager import LogManager
from Data.Lib.LucasClass.LucasImaging import Imaging
from Data.Lib.LucasFunc.LucasFunc import  ExpressionTest

from Data.Lib.Windows.WinError import WinError
from Data.Lib.Windows.WinImgLabelSet import WinImgLabelSet
from Data.Lib.Windows.WinArgsPasser import WinArgsPasser

class WinChart(QWidget):
    def __init__(self, LogManage: LogManager, ExcelPath: str):
        super().__init__()
        self.ExcelPath: str = ExcelPath
        self.Basic_Config(LogManage, ExcelPath)
        self.Initialize()

    def Basic_Config(self, LogManage: LogManager, ExcelPath: str):
        from pandas import ExcelFile
        self.SheetNames = ExcelFile(ExcelPath).sheet_names
        self.LogManage: LogManager = LogManage
        self.WinArgsPass: WinArgsPasser = WinArgsPasser()
        self.Imaging: Imaging = None

    def Initialize(self):
        self.Window_Config()
        self.Widget_Create()
        self.Widget_Config()
        self.Widget_Connect()
        self.Layout_Set()

        self.LogManage.LogOutput(Type='WinMain', LogMassage='WinMain Initialize Complete.')

    def Window_Config(self):
        self.setWindowTitle("PySide6 基础示例")
        self.setFixedSize(526, 472)

    def Widget_Create(self):
        self.List_TextBox: list[QLineEdit] = []
        for n in range(1): self.List_TextBox.append(QLineEdit())

        self.List_ComboBox: list[QComboBox] = []
        for n in range(2): self.List_ComboBox.append(QComboBox())

        self.List_Button: list[QPushButton] = []
        for n in range(20): self.List_Button.append(QPushButton())

    def Widget_Config(self):
        self.List_TextBox[0].setText('<> = ')
        self.List_TextBox[0].setPlaceholderText('在此键入参数表达式...')
        self.List_TextBox[0].setFixedSize(330, 40)

        self.List_ComboBox[0].addItem('选择 数据表 ↓')
        self.List_ComboBox[0].addItems(self.SheetNames)
        self.List_ComboBox[0].setFixedSize(160, 40)

        self.List_ComboBox[1].addItem('选择 表类型 ↓')
        self.List_ComboBox[1].addItems(['BarChart', 'LineChart', 'PieChart'])
        self.List_ComboBox[1].setFixedSize(160, 40)

        _ = ['清    空', '添加新参数', '测试表达式']
        for n in range(3):
            self.List_Button[n].setText(f'{_[n-3]}')
            self.List_Button[n].setFixedSize(160, 60)
        _ = ['+', '-', '*', '/', '7', '8', '9', '(', '4', '5', '6', ')', '1', '2', '3', '0']
        for n in range(3, 19):
            self.List_Button[n].setText(f'{_[n-3]}')
            self.List_Button[n].setFixedSize(80, 80)
        self.List_Button[19].setText('制图')
        self.List_Button[19].setFixedSize(160, 160)

    def Widget_Connect(self): 
        self.List_Button[0].clicked.connect(self.Button_Clear)
        self.List_Button[1].clicked.connect(self.Button_AddArgu)
        self.List_Button[2].clicked.connect(self.Button_Test)
        self.List_Button[19].clicked.connect(self.Button_ToImage)

        _ = ['+', '-', '*', '/', '7', '8', '9', '(', '4', '5', '6', ')', '1', '2', '3', '0']
        for n in range(len(_)):
            self.List_Button[n+3].clicked.connect(lambda __, s=_[n]:self.KeyBoard(s))

    def Layout_Set(self):
        Layout = QGridLayout()

        Layout.addWidget(self.List_Button[0], 0, 0, 1, 2)
        Layout.addWidget(self.List_Button[1], 0, 2, 1, 2)
        Layout.addWidget(self.List_Button[2], 0, 4, 1, 2)
        n = 3
        for r in range(2, 6):
            for i in range(0, 4):
                Layout.addWidget(self.List_Button[n], r, i, 1, 1)
                n += 1
        Layout.addWidget(self.List_Button[19], 4, 4, 2, 2)

        Layout.addWidget(self.List_TextBox[0], 1, 0, 1, 4)
        Layout.addWidget(self.List_ComboBox[0], 1, 4, 1, 2)
        Layout.addWidget(self.List_ComboBox[1], 2, 4, 1, 2)

        self.setLayout(Layout)

    def Button_Clear(self):
        self.List_TextBox[0].setText('<> = ')

    def Button_AddArgu(self):
        if self.List_TextBox[0].text()[-1] == ' ':
            self.List_TextBox[0].setText(self.List_TextBox[0].text() + '<>')
        else:
            self.List_TextBox[0].setText(self.List_TextBox[0].text() + ' <>')

    def Button_Test(self):
        Expression: str = self.List_TextBox[0].text()
        result = ExpressionTest(Expression=Expression)
        if result == 'True':
            self.LogManage.LogOutput(Type='ExpressionTest', LogMassage='Expression Test Passed.')
        else:
            _WinError = WinError(self.LogManage, f'\t表达式有误:\n      {result}.')
            _WinError.exec()
            return

        if self.List_ComboBox[0].currentIndex():
            self.Imaging: Imaging = Imaging(Path=self.ExcelPath, SheetName=self.List_ComboBox[0].currentText(), LogManage=self.LogManage)
        else:
            _WinError = WinError(self.LogManage, '\t数据缺失:\n      未选择目标数据表.')
            _WinError.exec()
            return
        
        if self.List_ComboBox[1].currentIndex():
            pass
        else:
            _WinError = WinError(self.LogManage, '\t数据缺失:\n      未选择目标表类型.')
            _WinError.exec()
            return
        
        return 'True'

    def Button_ToImage(self):
        if self.Button_Test() != 'True':
            return
        # self.Imaging: Imaging = Imaging(Path=self.ExcelPath, SheetName=self.List_ComboBox[0].currentText(), LogManage=self.LogManage)

        _WinImgLabelSet = WinImgLabelSet(LogManage=self.LogManage, WinArgsPass=self.WinArgsPass, Tittle=self.List_ComboBox[1].currentText())
        _WinImgLabelSet.exec()

        Tittle_XY = self.WinArgsPass.Tittle_XY
        if Tittle_XY[2]:
            Tittle: dict = {'Tittle': None,'Tittle_X': Tittle_XY[0],'Tittle_Y': Tittle_XY[1]}
            self.Imaging.ToImage(Type=self.List_ComboBox[1].currentText(), Expression=self.List_TextBox[0].text(), Tittle=Tittle)
            self.WinArgsPass.Tittle_XY[2] = False
    
    def KeyBoard(self, ButtonID: str):
        _ = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if ButtonID in _:
            if self.List_TextBox[0].text()[-1] in _:
                self.List_TextBox[0].setText(self.List_TextBox[0].text() + f'{ButtonID}')
            elif self.List_TextBox[0].text()[-1] == ' ':
                self.List_TextBox[0].setText(self.List_TextBox[0].text() + f'{ButtonID}')
            elif self.List_TextBox[0].text()[-1] not in _:
                self.List_TextBox[0].setText(self.List_TextBox[0].text() + f' {ButtonID}')
        else:
            if self.List_TextBox[0].text()[-1] == ' ':
                self.List_TextBox[0].setText(self.List_TextBox[0].text() + f'{ButtonID}')
            else:
                self.List_TextBox[0].setText(self.List_TextBox[0].text() + f' {ButtonID}')

if __name__ == "__main__":
    LogManage: LogManager = LogManager(r'Log')

    app = QApplication(sys.argv)
    window = WinChart(LogManage=LogManage, ExcelPath='Data\Excels\苏泊尔2019-2023.xlsx')
    window.show()
    sys.exit(app.exec())
