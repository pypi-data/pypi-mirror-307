import pandas as pd
import os
from tqdm import tqdm
from data_get import get_file_folder, get_data

def test_csv_data(list_msg, list_num, path):
    import csv
    ff = open(path)
    reader = csv.reader(ff)
    header = next(reader)
    list_num.append(len(header))
    print(path)
    list_msg.append(['表头'] + [path] + header)
    row = next(reader)
    list_msg.append(['第一行'] + [path] + row)
    ff.close()
    return list_msg, list_num

def jz_card_to_all(paths, method=1):
    """
    合并文件夹下经侦调取的银行卡,原始数据为易明细信息、账户信息、人员信息的csv文件
    报错:No columns to parse from file 有空文件中无表头
    :return: file :一个字典，包含合并多张表，交易明细信息、账户信息、人员信息等
    """
    # 合并经侦银行卡
    import re
    path = paths
    bool_value = True
    deal, staff, account, contact, location, compulsion, task, under = [[], [], [], [], [], [], [], []]  # 定义list
    file = {"交易明细": deal,
            '关联子账户': under,
            "账户信息": account,
            "人员信息": staff,
            '人员联系方式信息': contact,
            '人员住址信息': location,
            '强制措施信息': compulsion,
            '任务信息': task}

    def get_file(file_dir):
        for parent, dirnames, filenames in os.walk(file_dir):
            # 第一个参数是文件夹路径，第二个参数是子文件夹，第三个参数是文件名
            for filename in filenames:
                if os.path.splitext(filename)[1] == '.csv':
                    if re.search('子', filename):  # 匹配关键字
                        continue
                    for m in file.keys():
                        if re.search(m, filename):  # 匹配关键字
                            a = os.path.join(parent, filename)
                            file[m].append(a)

            if bool_value is False:
                dirnames.clear()  # 清除子文件夹列表

    get_file(path)

    for i in file.keys():
        if i == "交易明细" and method == 1:
            if os.path.exists(f'{os.path.dirname(path)}/{os.path.basename(path)}交易流水.csv'):
                os.remove(f'{os.path.dirname(path)}/{os.path.basename(path)}交易流水.csv')
            line_nums = []
            biao_test = []
            for k in tqdm(file[i], desc='数据合并'):
                # csv表头获取
                # r = test_csv_data(biao_test, line_nums, k)
                # biao_test = r[0]
                # line_nums = r[1]
                # 合并csv
                fr = open(k, 'rb').read()
                with open(f'{os.path.dirname(path)}/{os.path.basename(path)}交易流水.csv',
                          'ab') as f:  # 将结果保存为result.csv
                    f.write(fr)
            # pd.DataFrame(biao_test).to_excel(f'{os.path.dirname(path)}/{os.path.basename(path)}交易表头.xlsx',index=False)

            print('交易明细合并完毕！')
            print('正在读取交易明细')
            df = pd.read_csv(f'{os.path.dirname(path)}/{os.path.basename(path)}交易流水.csv',
                             dtype=str, encoding="GB18030", on_bad_lines='skip', encoding_errors='ignore',
                             )  # usecols=range(0, most_lenth)
            print('读取完毕！')
            df.drop_duplicates(keep='first', inplace=True)
            file[i] = df
        else:
            try:
                total = pd.DataFrame()
                line_nums = []
                biao_test = []
                for j in file[i]:  # 循环字典value里的list
                    if i == '交易明细' and method == 2:
                        r = test_csv_data(biao_test, line_nums, j)
                        biao_test = r[0]
                        b = pd.read_csv(j, encoding="GB18030", dtype=str, on_bad_lines='skip', encoding_errors='ignore')
                    else:
                        b = pd.read_csv(j, encoding="GB18030", dtype=str)
                        if i == '账户信息':
                            b['来源'] = j
                    # encoding = "gbk"使用gbk编码读csv
                    total = pd.concat([b, total], ignore_index=True, copy=False)
                if i == '交易明细':
                    pd.DataFrame(biao_test).to_excel(f'{os.path.dirname(path)}/{os.path.basename(path)}交易表头.xlsx',
                                                     index=False)
                total.drop_duplicates(keep='first', inplace=True)
                file[i] = total  # 将合并表赋值给对应value
            except:
                if i == '交易明细':
                    pd.DataFrame(biao_test).to_excel(f'{os.path.dirname(path)}/{os.path.basename(path)}交易表头.xlsx',
                                                     index=False)

    return file


def xlsx_to_all(paths):
    path = paths
    bool_value = True

    def get_file(file_dir):
        file_name = []
        for parent, dirnames, filenames in os.walk(file_dir):
            # 第一个参数是文件夹路径，第二个参数是子文件夹，第三个参数是文件名
            for filename in filenames:
                if os.path.splitext(filename)[1] == '.xlsx' or os.path.splitext(filename)[1] == '.xls':
                    a = os.path.join(parent, filename)
                    file_name.append(a)

            if bool_value is False:
                dirnames.clear()  # 清除子文件夹列表
        return file_name

    file_s = get_file(path)

    total = pd.DataFrame()
    for k in tqdm(file_s, desc='数据合并'):
        b = pd.read_excel(k, dtype=str)
        total = pd.concat([b, total], ignore_index=True, copy=False)
    total.drop_duplicates(keep='first', inplace=True)
    return total


def sheet_to_all(sheet: str):
    """
    合并文件夹下指定xlsx文件sheet
    :param sheet: 指定sheet名
    :return: data: 合并表
    """
    from data_get import get_file_folder
    path = get_file_folder()
    list1 = os.listdir(path)
    data = pd.DataFrame()
    for i in list1:
        b = pd.read_excel(f"{path}/" + i, sheet_name=sheet, dtype=str)
        b = b.where(b.notnull(), '')
        data = pd.concat([b, data], ignore_index=True)
    return data


def multiple_sheet_to_all(sheet_name_list: list = None):
    """
    合并多sheet的excel
    :param sheet_name_list:
    :return: dict_all: 存放多表的字典
    """
    if sheet_name_list is None:
        sheet_name_list = ['注册信息', '登录日志', '账户明细']
    path = get_file_folder()
    filename = os.listdir(path)

    dict_all = {}
    for j in sheet_name_list:
        data = pd.DataFrame()
        for i in tqdm(filename):
            b = pd.read_excel(path + "/" + i, sheet_name=j, dtype=str)
            b = b.where(b.notnull(), '')
            data = pd.concat([b, data], ignore_index=True)
        dict_all[j] = data

    return dict_all