import pandas as pd
from tqdm import tqdm
from wash_tool import luhn_iscard,extract_first_string

def pivot_table_deal_distinct(df_df):
    """
    对透视文件xslx,主对端银行卡都有记录，借贷重复去重
    :return: df:双向去重后数据表
    """
    df = df_df
    df["出"] = pd.to_numeric(df["出"])
    df["进"] = pd.to_numeric(df["进"])
    for row in tqdm(df.index):
        # 筛选主对端相反的数据 若用双循环遍历较慢，因此用相反的账号做两个筛选，最后取交集速度大幅加快
        data = df[(df['主端卡号'] == df.loc[row, '对端账号卡号']) & (df['对端账号卡号'] == df.loc[row, '主端卡号'])]
        if data.empty:
            continue
        else:
            # data.index为列表，包含切片内容的行号与数据类型
            # print(data.index)
            if df.loc[row]['进'] >= df.loc[data.index[0], '出']:
                df.loc[data.index[0], '出'] = None
            else:
                df.loc[row, '进'] = None

            if df.loc[row]['出'] >= df.loc[data.index[0], '进']:
                df.loc[data.index[0], '进'] = None
            else:
                df.loc[row, '出'] = None
    return df


def pivot_deduplication_unify_the_direction(df_df):
    # 禁用科学计数法
    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    # 将透视表统一成出款方向
    df = df_df

    pt = df.pivot_table(index=['主端卡号', '对端卡号'], columns='收付标志', values='交易金额',
                        aggfunc='sum').reset_index()
    # pt_time = df.pivot_table(index=['主端卡号', '对端账号卡号'], columns='收付标志', values='交易金额',
    #                     aggfunc='sum').reset_index()
    jin = pt[pt['进'].notna()][['主端卡号', '对端卡号', '进']].rename(
        columns={'进': '出', '主端卡号': '对端卡号', '对端卡号': '主端卡号'})
    chu = pt[pt['出'].notna()][['主端卡号', '对端卡号', '出']]

    new = pd.concat([jin, chu])[['主端卡号', '对端卡号', '出']]
    new = new.reset_index().drop('index', axis=1)
    new = new.sort_values(by='出', ascending=False)
    # 删除自身转账
    new = new[new['主端卡号'] != new['对端卡号']]
    # 多层数据透视去重
    new['key'] = new['主端卡号'] + new['对端卡号']
    new = new.drop_duplicates(subset=['key'], keep='first')
    new = new.drop('key', axis=1)

    return new


def tou_shi(df_toushi):
    all_pt = pd.pivot_table(df_toushi, index=['对端卡号'], values=['交易金额', '主端卡号', '对端姓名'],
                            columns=['收付标志'],
                            aggfunc={"交易金额": 'sum', '主端卡号': ['nunique', 'count'], '对端姓名': extract_first_string}).reset_index()

    all_pt.columns = ['_'.join(col) for col in all_pt.columns.values]

    all_pt.rename(columns={'对端卡号__': '对端卡号', '主端卡号_nunique_出': '关联主端个数_出',
                           '主端卡号_nunique_进': '关联主端个数_进', '主端卡号_count_出': '主端卡号交易次数_出',
                           '主端卡号_count_进': '主端卡号交易次数_进',
                           '对端姓名_extract_first_string_出': '对端姓名_出',
                           '对端姓名_extract_first_string_进': '对端姓名_进', '交易金额_sum_出': '交易金额_出',
                           '交易金额_sum_进': '交易金额_进'}, inplace=True)
    all_pt['平均出款'] = all_pt['交易金额_出'] / all_pt['主端卡号交易次数_出']
    all_pt['平均进款'] = all_pt['交易金额_进'] / all_pt['主端卡号交易次数_进']
    all_pt = all_pt[
        ['对端卡号', '交易金额_出', '对端姓名_出', '平均出款', '关联主端个数_出', '主端卡号交易次数_出', '交易金额_进',
         '对端姓名_进', '平均进款', '关联主端个数_进', '主端卡号交易次数_进']]
    print('保存透视结果...')
    all_pt['银行卡'] = all_pt['对端卡号'].apply(luhn_iscard)
    return all_pt