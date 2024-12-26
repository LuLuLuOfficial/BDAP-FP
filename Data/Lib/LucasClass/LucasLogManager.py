class LogManager():
    def __init__(self, OutPutPath_Root) -> None:
        self.TimeStamp: str = ''
        self.OutPutPath_Root: str = OutPutPath_Root
        self.OutPutPath_File: str = OutPutPath_Root

        self.LogLimit: list[bool, int] = [True, 10]

        self.Initialize()

    def Initialize(self):
        self.TimeStamp = self.GetTimeStamp()
        self.OutPutPath_File += rf'\{self.TimeStamp}.txt'
        with open(file=self.OutPutPath_File, mode='w', encoding='utf-8') as file:
            from Data.Lib.LucasClass.LucasIdentity import Author_Lucas
            for Line in Author_Lucas():
                file.write(f'{Line}\n')
            file.write(f'\nLog File Created At {self.TimeStamp}\n\n\n\n\n\n')
            file.close()
        self.CheckLogLimit()

    def GetTimeStamp(self):
        from time import localtime, strftime
        Time_Local: str = localtime()
        Time_Formatted: str = strftime("%Y-%m-%d %H-%M-%S", Time_Local)
        return Time_Formatted
    
    def SetLogLimit(self, Mode: bool = True, Limit: int = 10):
        self.LogLimit = {Mode, Limit}

    def CheckLogLimit(self):
        from pathlib import Path as _Path
        Path = _Path(self.OutPutPath_Root)
        Files = [f for f in Path.iterdir() if f.is_file() and f.suffix.lower() == '.txt']
        if not Files:
            return
        while (self.LogLimit[0]) and (len(Files) > self.LogLimit[1]):
            OldestFile = min(Files, key=lambda f: f.stat().st_mtime)
            self.LogOutput(Type = f'Operate', LogMassage = f'Deleted Oldest LogFile -> {OldestFile}.')
            OldestFile.unlink()
            Files = [f for f in Path.iterdir() if f.is_file() and f.suffix.lower() == '.txt']

    def LogOutput(self, Type: str = 'Normal', LogMassage: str = 'Invalid Information.', DoPrint: bool = True):
        TimeStamp = self.GetTimeStamp()
        LogText: str = f'{TimeStamp} |-| {Type}: {LogMassage}'
        if DoPrint:
            print(LogText)
        with open(file=self.OutPutPath_File, mode='a', encoding='utf-8') as file:
            file.write(f'{LogText}\n')

if __name__ == '__main__':
    LogManage = LogManager(OutPutPath_Root=r'Log')
    for n in range(10):
        LogManage.LogOutput()
