from sys import argv, exit
from PySide6.QtWidgets import QApplication

from Data.Lib.Windows.WinMain import WinMain
from Data.Lib.LucasClass.LucasLogManager import LogManager

if __name__ == "__main__":
    LogManage: LogManager = LogManager(r'Log')

    app = QApplication(argv)
    window = WinMain(LogManage=LogManage)
    window.show()
    exit(app.exec())
