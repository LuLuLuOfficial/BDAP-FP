import pandas

from Data.Lib.LucasClass.LucasLogManager import LogManager
from Data.Lib.LucasFunc.LucasFunc import GetPlatform

class Imaging():
    def __init__(self, Path: str, SheetName: str, LogManage: LogManager):
        self.Basic_Config(Path=Path, SheetName=SheetName, LogManage=LogManage)

    def Basic_Config(self, Path: str, SheetName: str, LogManage: LogManager):
        self.Path_Excel: str = Path
        self.LogManage: LogManager = LogManage
        self.DF = pandas.read_excel(self.Path_Excel, header=None, dtype=str, sheet_name=SheetName)

        self.Index_KeyYear: list[str] = self.DF.iloc[0, :].tolist()
        self.Index_KeyItem: list[str] = self.DF.iloc[:, 0].tolist()

        self.List_Year: list[str] = self.Index_KeyYear[1: -1]

    def ToImage(self, Type: str, Expression: str, Tittle: dict):
        ''' Example -> Tittle: {
        'Tittle': <Tittle>,
        'Tittle_X': <Tittle_X>,
        'Tittle_Y': <Tittle_Y>}'''

        ''' Example -> CalculateEnd: {
        'Name': '销售净利率', 2019: 9.65, 2020: 9.91, 2021: 8.99, 2022: 10.24, 2023: 10.23}'''

        Tittle: dict = Tittle
        List_Year = self.List_Year
        CalculateEnd = self.ComputedExpression(Expression=Expression)
        Tittle['Tittle'] = CalculateEnd['Name']
        Values: int = [CalculateEnd[int(year)] for year in List_Year]

        import matplotlib.pyplot as plt
        from matplotlib import rcParams

        Platform: str = GetPlatform()
        Font: list[str] = []
        if Platform == 'Windows': Font = ['SimHei']
        elif Platform == 'Darwin': Font = ['STHeiti']
        elif Platform == 'Linux': Font = []
        rcParams['font.sans-serif'] = Font  # 设置字体
        rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

        if Type == 'BarChart':      # 条形图
            fig, ax = plt.subplots()
            bars = ax.bar(List_Year, Values)
            for bar in bars:
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.1,  # 位置：条形顶部
                        round(yval, 2), ha='center', va='bottom', fontsize=10)  # 显示的数值和样式
            ax.set_title(Tittle['Tittle'])
            ax.set_xlabel(Tittle['Tittle_X'])
            ax.set_ylabel(Tittle['Tittle_Y'])
            plt.show()
        elif Type == 'LineChart':   # 折线图
            fig, ax = plt.subplots()
            ax.plot(List_Year, Values, marker='o', linestyle='-', color='b', label=Tittle['Tittle'])
            for i, value in enumerate(Values):
                ax.text(List_Year[i], value + 0.1,  # 位置：数据点的上方
                        round(value, 2), ha='center', va='bottom', fontsize=10)  # 显示的数值和样式
            ax.set_title(Tittle['Tittle'])
            ax.set_xlabel(Tittle['Tittle_X'])
            ax.set_ylabel(Tittle['Tittle_Y'])
            plt.show()
        elif Type == 'PieChart':    # 饼  图
            plt.pie(Values, labels=List_Year, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
            plt.title(Tittle['Tittle'])
            plt.show()

    def ComputedExpression(self, Expression: str):
        Expression: str = Expression        # 表达式原式

        InArgument: bool = False            # 标志在下标参数中
        EqualRight: bool = False            # 标志下表在表达式名中(在等号左边)

        ArgumentLocation: list = [-1, -1]   # 标识参数的位置[左, 右]
        Dict_Arguments: dict = {}           # 存储参数名与参数值(包括表达式名)
        Dict_Arguments_Keys: list = []      # 存储参数名(不包括表达式名)

        CalculateEnd: dict = {}             # 计算结果

        ''' Example -> Dict_Arguments: {
        'ExpressionName': '销售净利率', '  1.持续经营净利润（净亏损以“－”号填列）': ['  1.持续经营净利润（净亏损以“－”号填列）', '1915653117.02', '1842624762.74', '1941371527.89', '2066176439.62', '2179420437.21', nan], '一、营业总收入': ['一、营业总收入', '19853477882.97', '18596944289.02', '21585331407.47', '20170527516.66', '21303948642.66', '利润表']}'''

        ''' Example -> CalculateEnd: {
        'Name': '销售净利率', 2019: 9.65, 2020: 9.91, 2021: 8.99, 2022: 10.24, 2023: 10.23}'''

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
                    Dict_Arguments[Argument] = self.DF.iloc[self.Index_KeyItem.index(Argument), :].tolist()
                    Dict_Arguments_Keys.append(Argument)
                else:
                    EqualRight = True
                    Dict_Arguments['ExpressionName'] = Argument
                    CalculateEnd['Name'] = Argument
                continue

        for Year in self.Index_KeyYear[1:-1]: # 计算表达式结果
            _Expression = Expression[Expression.find('=')+1:]
            _Index = self.Index_KeyYear.index(Year)
            for n in Dict_Arguments_Keys:
                _Expression = _Expression.replace(f'<{n}>', Dict_Arguments[n][_Index])
            ValueThisYear = eval(_Expression)
            CalculateEnd[int(Year)] = round(ValueThisYear, 2)

        return CalculateEnd

if __name__ == "__main__":
    LogManage: LogManager = LogManager(r'Log')
    Test_Imaging: Imaging = Imaging(Path='Data\Excels\苏泊尔2019-2023.xlsx', SheetName='三表', LogManage=LogManage)
    Test_Imaging.ToImage(Type='BarChart', Expression='<销售净利率> = <  1.持续经营净利润（净亏损以“－”号填列）> / <一、营业总收入> * 100', Tittle={'Tittle_X': '年份','Tittle_Y': '%'})
    Test_Imaging.ToImage(Type='LineChart', Expression='<销售净利率> = <  1.持续经营净利润（净亏损以“－”号填列）> / <一、营业总收入> * 100', Tittle={'Tittle_X': '年份','Tittle_Y': '%'})
    Test_Imaging.ToImage(Type='PieChart', Expression='<销售净利率> = <  1.持续经营净利润（净亏损以“－”号填列）> / <一、营业总收入> * 100', Tittle={'Tittle_X': '年份','Tittle_Y': '%'})
