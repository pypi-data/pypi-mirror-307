import pandas as pd
from tqdm import tqdm


def str_of_num(num):
    """
    递归实现，精确为最大单位值 + 小数点后三位
    """

    def strof_size(num, level):
        if level >= 2:
            return num, level
        elif num >= 10000:
            num /= 10000
            level += 1
            return strof_size(num, level)
        else:
            return num, level

    units = ['', '万', '亿']
    num, level = strof_size(num, 0)
    return '{}{}'.format(round(num, 3), units[level])


def luhn_iscard(card_num):
    if type(card_num) == float:
        return False
    for c in card_num:
        if not c.isdigit():
            return False
    s = 0
    card_num_length = len(card_num)
    start_with = ('6', '5', '4', '3', '9')
    if card_num_length >= 10 and card_num.startswith(start_with):
        # if card_num_length >= 10:
        for _ in range(1, card_num_length + 1):
            t = int(card_num[card_num_length - _])
            if _ % 2 == 0:
                t *= 2
                s += t if t < 10 else t % 10 + t // 10
            else:
                s += t
        return s % 10 == 0
    else:
        return False


def deal_str(data):
    data = str(data) + '\t'
    return data


def extract_first_string(x):   
    """
    取最多出现的字符串
    """
    k = list(x)
    most_common_element = max(k, key=k.count)
    return most_common_element


def format_time(x):
    from datetime import datetime
    for f in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%Y%m%d%H%M%S', '%Y/%m/%d %H:%M:%S']:
        try:
            formatted_date = datetime.strptime(x, f).strftime('%Y-%m-%d %H:%M:%S')
            return formatted_date
        except ValueError:
            pass
    return pd.NaT


def removeDup(mylist:list) -> list:
    # 列表去重
    if len(mylist) < 1:
        raise Exception("形参异常")
    result = [mylist[0]]
    for i in mylist:
        if i not in result:
            result.append(i)
    return result


def calculate_hash(row):
    # 创建Hash
    import hashlib
    new_row = row[['主端卡号', '对端卡号', '收付标志', '交易金额', '交易余额', '交易时间', '交易结果']]
    row_str = ','.join(map(str, new_row))
    return hashlib.md5(row_str.encode('utf-8')).hexdigest()

def location_extract(df_df, lie: str):
    """
    地址信息标准化提取
    :param df_df:
    :param lie: 需要标准化的地址列
    :return: df: 标准化的表
    """
    import jionlp as jio
    df = df_df
    df = pd.concat([df, pd.DataFrame(columns=['省', '市', '区', '详细'])])
    df = df[df[lie].notna()]
    for i in tqdm(df.index, desc='地址标准化'):
        df['省'][i] = jio.parse_location(df[lie][i])['province']
        df['市'][i] = jio.parse_location(df[lie][i])['city']
        df['区'][i] = jio.parse_location(df[lie][i])['county']
        df['详细'][i] = jio.parse_location(df[lie][i])['detail']
    return df