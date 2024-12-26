def PathCheck(Path: str):
    from pathlib import Path as _Path
    Path = _Path(Path)
    if Path.exists():
        return True
    else:
        return False

def GetFileList(Extension: str, Path: str):
    from pathlib import Path as _Path
    Path = _Path(Path)
    MatchingFileList: dict[str] = {}
    for file in Path.rglob(f'*{Extension}'):
        if file.is_file():
            MatchingFileList[f'{file.name}'] = str(file)
    return MatchingFileList

def ExpressionTest(Expression: str):
    try:
        Expression: str = Expression        # 表达式原式

        InArgument: bool = False            # 标志在下标参数中
        EqualRight: bool = False            # 标志下表在表达式名中(在等号左边)

        ArgumentLocation: list = [-1, -1]   # 标识参数的位置[左, 右]
        Dict_Arguments: dict = {}           # 存储参数名与参数值(包括表达式名)
        Dict_Arguments_Keys: list = []      # 存储参数名(不包括表达式名)

        ''' Example -> Dict_Arguments: {
        'ExpressionName': '销售净利率', '  1.持续经营净利润（净亏损以“－”号填列）': ['  1.持续经营净利润（净亏损以“－”号填列）', '1915653117.02', '1842624762.74', '1941371527.89', '2066176439.62', '2179420437.21', nan], '一、营业总收入': ['一、营业总收入', '19853477882.97', '18596944289.02', '21585331407.47', '20170527516.66', '21303948642.66', '利润表']}'''

        for n in range(len(Expression)): # 获取参数名以及位置用以替换真值
            Key = Expression[n]
            if Key == '<':
                InArgument = True
                ArgumentLocation[0] = n+1
                continue
            if InArgument and Key == '>':
                InArgument = False
                ArgumentLocation[1] = n
                Argument = Expression[ArgumentLocation[0]: ArgumentLocation[1]]
                ArgumentLocation = [-1, -1]
                if EqualRight:
                    import random
                    Dict_Arguments[Argument] = random.randint(10, 100)
                    Dict_Arguments_Keys.append(Argument)
                else:
                    EqualRight = True
                    Dict_Arguments['ExpressionName'] = Argument
                continue

        _Expression = Expression[Expression.find('=')+1:]
        for n in Dict_Arguments_Keys:
            _Expression = _Expression.replace(f'<{n}>', str(Dict_Arguments[n]))
        ValueThisYear = eval(_Expression)
    except Exception as e:
        return e
    else:
        return 'True'

def GetSysFonts():
    from matplotlib.font_manager import fontManager
    FontsName: list = []
    for Font in fontManager.ttflist:
        FontsName.append(Font.name)

def GetPlatform():
    from platform import system
    system_name = system()
    return f"{system_name}"


if __name__ == '__main__':
    print(PathCheck(''))
    print(GetFileList('.xlsx', 'Data\Excels'))
    print(GetPlatform())
