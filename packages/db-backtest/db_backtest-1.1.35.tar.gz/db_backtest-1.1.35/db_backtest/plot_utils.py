# -*- coding: utf-8 -*-

import pandas as pd

def print_table(table, name=None, fmt=None):
    ''' 在 Jupyter Notebook 中打印 Pandas 数据表格'''

    from IPython.display import display

    if isinstance(table, pd.Series):
        table = pd.DataFrame(table)

    if isinstance(table, pd.DataFrame):
        table.columns.name = name

    prev_option = pd.get_option('display.float_format') #获取当前 Pandas 的浮点数格式化选项
    if fmt is not None:
        pd.set_option('display.float_format', lambda x: fmt.format(x))

    display(table)

    if fmt is not None:
        pd.set_option('display.float_format', prev_option) #恢复
    

