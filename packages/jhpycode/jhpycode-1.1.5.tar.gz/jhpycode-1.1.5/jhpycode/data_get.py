import tkinter as tk
from tkinter import filedialog


def get_mysql_table(name: str, table: str):
    """
    链接Mysql
    :param table: 表名
    :param name: 库名
    :return: df
    """
    # 获取数据库数据
    from sqlalchemy import create_engine
    import pandas as pd
    local_con = create_engine(f'mysql+pymysql://root:PPSQmysql77]]@localhost:3306/{name}')
    df = pd.read_sql_table(table, local_con, dtype_backend='numpy_nullable')
    return df


def get_mysql_con(name: str):
    """
    链接Mysql
    :param name: 库名F
    :return: local_con
    """
    # 获取数据库数据
    from sqlalchemy import create_engine
    local_con = create_engine(f'mysql+pymysql://root:PPSQmysql77]]@localhost:3306/{name}')
    return local_con


def get_file_folder():
    """
    获取文件夹路径
    :return: path
    """
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)  # 置顶窗口
    path = filedialog.askdirectory()
    return path


def get_data():
    """
    获取单个文件路径
    :return: path
    """
    # 获取文件路径
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)  # 置顶窗口
    path = filedialog.askopenfilename()
    return path


def get_datas():
    """
    获取多个文件路径
    :return:  path of tuple
    """
    # 获取多文件路径
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)  # 置顶窗口
    path = filedialog.askopenfilenames()
    return path


def get_encoding():
    """
    二进制方式读取，获取字节数据，检测类型
    :return: encod: 文件编码list
    """
    import chardet
    import os
    from tqdm import tqdm
    path = get_file_folder()
    list1 = os.listdir(path)
    encod = []
    for i in tqdm(list1):
        with open(f"{path}/" + i, 'rb') as f:
            encod.append(chardet.detect(f.read())['encoding'])
    return encod

