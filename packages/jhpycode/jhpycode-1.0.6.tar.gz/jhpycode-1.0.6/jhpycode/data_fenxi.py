import numpy as np
import pandas as pd
from tqdm import tqdm
from wash_tool import luhn_iscard

def peer_quality(x):  # 交易性质判断
    include_keywords = ['网络', '科技', '贸易', '商贸', '电子', '工程', '建筑', '信息', '技术']
    life_firm = ['银行', '保险', '贷款', '金融', '嘀嘀', '网银', '保险', '中国', '支付', '（', '(', '分期乐','平安', '年卡', '星驿', '分期', '备付金', '天翼', '时空信息交换', '天津舒行', '快手','滴滴', '付款', '京东', '美团', '三快', '拼多多', '寻梦', '财付通', '云闪付', '抖音','淘宝', '饿了么', '拉扎斯', '盒马', '理财', '基金', '唯品会', '物流', '顺丰', '微播', '格物致品']
    pay_firm = ['银生宝', '百利宝', '开联通', '汇聚支付', '百联优力', '连连国际支付有限公司', '易宝支付', '钱袋宝',
                '五八消费', '嘉联支付', '国通星驿', '宝付网络', '支付', '宝付', '云闪付', '合众易宝', '拉卡拉',
                '现代金融']

    if pd.notnull(x['交易摘要']):
        if any(x['交易摘要'].find(s) != -1 for s in ['atm', 'ATM', '现金', '存现', '取现']):
            return '现金交易'

        if any(x['交易摘要'].find(s) != -1 for s in ['结息', '冲正', '本息', '入息', '利息']):
            return '银行系统交易'

        if any(x['交易摘要'].find(s) != -1 for s in ['提现', '充值']):
            return '三方支付充提'

    if pd.notnull(x['备注']):
        if any(x['备注'].find(s) != -1 for s in ['atm', 'ATM', '现金']):
            return '现金交易'

        if any(x['备注'].find(s) != -1 for s in ['银联转账', '柜面']):
            return '卡转卡交易'

        if any(x['备注'].find(s) != -1 for s in ['提现', '充值']):
            return '三方支付充提'

    if pd.notnull(x['对端姓名']):
        if any(x['对端姓名'].find(s) != -1 for s in ['atm', 'ATM', '现金']):
            return '现金交易'

        if any(x['对端姓名'].find(s) != -1 for s in pay_firm):
            return '三方转账/消费'

        if '公司' in x['对端姓名']:
            if any(x['对端姓名'].find(s) != -1 for s in include_keywords):
                #     if not any(x['对端姓名'].find(s) != -1 for s in life_firm):
                #         return '空壳公司'
                if not any(x['对端姓名'].find(s) != -1 for s in life_firm):
                    if not any(x['对端姓名'].find(s) != -1 for s in pay_firm):
                        return '公司交易'

    if luhn_iscard(x['对端卡号']):
        return '卡转卡交易'

    return '生活消费'


def max_pd(df, nums=10, rates=0.01):
    print('正在分析资金特征...')

    def max_pianduan(df_df, num=10, rate=0.005):
        # 标记'转账'行
        df_zz = df_df.copy()

        df_zz['is_transfer'] = df_zz['交易判断综合'] == '转账'
        if not df_zz['is_transfer'].any():
            return 0
        # 找出所有连续的'转账'片段
        df_zz['transfer_group'] = (df_zz['is_transfer'] != df_zz['is_transfer'].shift()).cumsum()

        # 对于每个片段，计算长度和开始结束位置
        transfer_group = df_zz[df_zz['is_transfer']].groupby('transfer_group').agg(start=('is_transfer', 'idxmin'),
                                                                                   end=('is_transfer', 'idxmax'))
        transfer_group['start'] = df_zz.groupby('transfer_group').apply(lambda x: x.index.min())
        transfer_group['end'] = df_zz.groupby('transfer_group').apply(lambda x: x.index.max())
        transfer_group['length'] = transfer_group['end'] - transfer_group['start'] + 1
        transfer_group['gap'] = transfer_group['start'] - transfer_group['end'].shift(1) - 1

        # 尝试合并片段
        max_length = 0

        for i, row_i in transfer_group.iterrows():
            gap = 0
            total_length = 0
            for j, row_j in transfer_group.iterrows():
                if j <= i:
                    max_length = max(max_length, row_i['length'])
                    total_length = row_i['length']
                    continue
                gap = gap + row_j['gap']  # 计算两个片段之间的间隔
                total_length = total_length + row_j['length']

                if gap > num:
                    break
                if gap > max_length * rate:
                    break

                max_length = max(max_length, total_length)

        return max_length

    df_six = df.copy()

    # df_six['交易判断综合'] = df_six['交易判断'].apply(
    #     lambda x: '转账' if x in ['公司交易', '卡转卡交易', '现金交易', '银行系统交易'] else '非转账')
    df_six = df_six.sort_values(by=['主端卡号', '时间戳'], ascending=False).reset_index(drop=True)

    df_pt_seven = {}
    for b in tqdm(list(df_six['主端卡号'].unique()), desc='计算最大转账次数'):
        tmp_b = df_six[df_six['主端卡号'] == b][['交易判断综合']]
        max_zz = max_pianduan(tmp_b, nums, rates)
        df_pt_seven[b] = max_zz

    df_six['change'] = df_six['交易判断综合'].ne(df_six['交易判断综合'].shift()).astype(int)
    df_six['segment'] = df_six['change'].cumsum()
    result = df_six.groupby(['segment', '主端卡号', '交易判断综合']).size().reset_index(name='最大连续转账')
    result = result[['主端卡号', '交易判断综合', '最大连续转账']]

    df_pt_six = pd.pivot_table(result[result['交易判断综合'] == '转账'], index=['主端卡号'], values='最大连续转账',
                               aggfunc='max').reset_index()

    outcome = pd.DataFrame(list(df_pt_seven.items()), columns=['主端卡号', '最大连续转账(允许少量消费)'])
    outcome = pd.merge(outcome, df_pt_six, on='主端卡号', how='left')
    return outcome, result


def card_analyse(df_df, df_zh=pd.DataFrame()):
    from functools import reduce
    df_tmp = df_df.copy()
    extra = []

    # 工具
    def relevancy_num(x):  # 关联数
        zd_list = list(set(df_tmp['主端卡号']))
        m = list(set(x))
        count = 0
        for g in m:
            if g in zd_list:
                count = count + 1
        return count

    def primary_quality(x):  # 卡性质判断
        if x['消费率'] <= 0.2:
            if x['转账进出比'] >= 4 and x['交易流水'] >= 500000 and x['峰值次数'] >= 20 and 100 <= x['转账单次进款平均值'] <= 5000:
                return '收款卡'
            if x['转账进出比'] <= 0.3 and x['交易流水'] >= 500000 and x['峰值次数'] >= 20 and 100 <= x['转账单次出款平均值'] <= 5000:
                return '出款卡'
            if x['交易流水'] >= 500000 and x['峰值次数'] >= 10 and x['转账单次进款平均值'] >= 3000 and x['转账单次出款平均值'] >= 3000:
                return '中转卡'
            if x['交易流水'] >= 500000:
                return '工作卡'

        if x['最大连续转账(允许少量消费)'] >= 200:
            if x['转账进出比'] >= 5 and x['交易流水'] >= 500000 and x['峰值次数'] >= 20 and 100 <= x['转账单次进款平均值'] <= 2000:
                return '间断收款卡'
            if x['转账进出比'] <= 0.3 and x['交易流水'] >= 500000 and x['峰值次数'] >= 20 and 100 <= x['转账单次出款平均值'] <= 2000:
                return '间断出款卡'
            if x['交易流水'] >= 500000 and x['峰值次数'] >= 10 and x['转账单次进款平均值'] >= 3000 and x['转账单次出款平均值'] >= 3000:
                return '间断中转卡'
            if x['交易流水'] >= 500000:
                return '间断工作卡'

        if x['峰值次数'] >= 100:
            if x['峰值金额'] >= 100000:
                if x['交易流水'] >= 300000 and x['转账单次进款平均值'] >= 100 and x['转账单次出款平均值'] >= 100:
                    return '间断工作卡'

        if x['大金额转账率'] >= 0.4:
            if (x['交易次数']) >= 100:
                if x['消费率'] <= 0.5:
                    return '个人卡或数据少大金额交易较多'

        return '个人卡或数据少'

    if '交易判断' not in df_tmp.columns:
        tqdm.pandas(desc='交易判断')
        df_tmp['交易判断'] = df_tmp.progress_apply(peer_quality, axis=1)

    df_tmp['交易判断综合'] = df_tmp['交易判断'].apply(
        lambda x: '转账' if x in ['公司交易', '卡转卡交易', '现金交易', '银行系统交易'] else '非转账')

    print('正在统计资金...')
    df_pt_one = pd.pivot_table(df_tmp, index=["主端卡号"],
                               values=['交易金额', '交易时间'],
                               aggfunc={"交易金额": ["sum", "count"],
                                        # "对端卡号": relevancy_num,
                                        # '冻结次数': 'first',
                                        '交易时间': ['max', 'min']
                                        }).reset_index()
    df_pt_one.columns = ['_'.join(col) for col in df_pt_one.columns.values]
    df_pt_one.rename(columns={'主端卡号_': '主端卡号',
                              # '对端卡号_relevancy_num': '关联主端个数',
                              # '冻结次数_first': '冻结次数',
                              '交易金额_sum': '交易流水',
                              '交易金额_count': '交易次数',
                              '交易时间_max': '最后交易时间',
                              '交易时间_min': '首次交易时间'}, inplace=True)

    df_pt_two = df_tmp.sort_values(by=['时间戳'], ascending=False).reset_index()[['主端卡号', '交易余额']]
    df_pt_two = df_pt_two.groupby('主端卡号').first().reset_index()

    df_pt_three = pd.pivot_table(df_tmp[df_tmp['交易判断综合'] == '转账'], index=["主端卡号"], columns='收付标志',
                                 values=['交易金额'],
                                 aggfunc={"交易金额": ["count", 'mean']
                                          # "对端卡号": pd.Series.nunique
                                          }).reset_index()
    df_pt_three.columns = ['_'.join(col) for col in df_pt_three.columns.values]
    df_pt_three.rename(
        columns={'主端卡号__': '主端卡号', '交易金额_count_出': '转账出款次数', '交易金额_count_进': '转账进款次数',
                 '交易金额_mean_出': '转账单次出款平均值', '交易金额_mean_进': '转账单次进款平均值'}, inplace=True)
    # 交易峰值
    print('正在计算峰值...')
    df_tmp['峰值日期'] = df_tmp['交易时间'].dt.strftime('%Y-%m-%d')
    df_pt_four = df_tmp.groupby(['主端卡号', '峰值日期']).agg({'交易金额': ['count', 'sum']}).reset_index()
    df_pt_four.columns = ['_'.join(col) for col in df_pt_four.columns.values]
    df_pt_four.rename(columns={'主端卡号_': '主端卡号', '峰值日期_': '峰值日期', '交易金额_count': '峰值次数', '交易金额_sum': '峰值金额'}, inplace=True)
    idx = df_pt_four.groupby('主端卡号')['峰值次数'].idxmax()
    df_pt_four = df_pt_four.loc[idx]

    print('正在分析交易性质...')
    df_pt_five = pd.pivot_table(df_tmp, index=["主端卡号"], columns='交易判断',
                                values=['交易金额'],
                                aggfunc={"交易金额": ["count", 'sum']
                                         }).reset_index()
    df_pt_five.columns = ['_'.join(col) for col in df_pt_five.columns.values]
    df_pt_five.rename(columns={'主端卡号__': '主端卡号',
                               '交易金额_count_三方转账/消费': '三方转账/消费次数',
                               '交易金额_count_公司交易': '公司交易次数',
                               '交易金额_count_生活消费': '生活消费次数',
                               '交易金额_count_卡转卡交易': '卡转卡交易次数',
                               '交易金额_count_三方支付充提': '三方支付充提次数',
                               '交易金额_count_现金交易': '现金交易次数',
                               '交易金额_count_银行系统交易': '银行系统交易次数',
                               '交易金额_sum_三方转账/消费': '三方转账/消费金额',
                               '交易金额_sum_公司交易': '公司交易金额',
                               '交易金额_sum_生活消费': '生活消费金额',
                               '交易金额_sum_卡转卡交易': '卡转卡交易金额',
                               '交易金额_sum_三方支付充提': '三方支付充提金额',
                               '交易金额_sum_现金交易': '现金交易金额',
                               '交易金额_sum_银行系统交易': '银行系统交易金额',
                               }, inplace=True)

    df_pt_ten = pd.pivot_table(df_tmp[df_tmp['交易金额'] >= 10000], index=['主端卡号'], values=['交易金额'], aggfunc=['count']).reset_index()
    df_pt_ten.columns = ['_'.join(col) for col in df_pt_ten.columns.values]
    df_pt_ten.rename(columns={'主端卡号_': '主端卡号', 'count_交易金额': '大金额交易次数'}, inplace=True)
    new_line = ['三方转账/消费次数', '公司交易次数', '生活消费次数', '卡转卡交易次数', '三方支付充提次数', '现金交易次数',
                '银行系统交易次数',
                '三方转账/消费金额', '公司交易金额', '生活消费金额', '卡转卡交易金额', '三方支付充提金额', '现金交易金额',
                '银行系统交易金额']

    for i in new_line:
        if i not in df_pt_five.columns:
            df_pt_five[i] = 0

    if '对端isDuke' in df_tmp.columns:
        df_pt_nine = pd.pivot_table(df_tmp[df_tmp['对端isDuke'].isin([True, 'True'])], index=["主端卡号"], columns='收付标志',
                                    values=['对端卡号'],
                                    aggfunc={"对端卡号": pd.Series.nunique
                                             }).reset_index()

        df_pt_nine.columns = ['_'.join(col) for col in df_pt_nine.columns.values]
        df_pt_nine.rename(columns={'主端卡号_': '主端卡号', '对端卡号_出': '出款关联赌客数', '对端卡号_进': '进款关联赌客数'}, inplace=True)
        extra.append(df_pt_nine)

    df_pt = max_pd(df_tmp, 10, 0.01)[0]

    if not df_zh.empty:
        zh_zh = df_zh.copy()
        zh_msg = zh_zh[['交易卡号', '账户开户名称', '开户人证件号码']].drop_duplicates(keep='first').rename(columns={'交易卡号': '主端卡号'})
        zh_msg.dropna(subset=['主端卡号'], inplace=True)

        zh_zh = zh_zh[~zh_zh['账户状态'].isin(['关闭', '销户', '已关户', '销卡', '已销户', '关户', '注销'])]

        zh_zh['账户余额'] = pd.to_numeric(zh_zh["账户余额"], errors='coerce')
        zh_zh = zh_zh[['交易卡号', '账户余额']].rename(columns={'交易卡号': '主端卡号'})
        zh_zh = pd.pivot_table(zh_zh, index=["主端卡号"], values=['账户余额'], aggfunc=np.sum).reset_index()
        zh_zh['账户状态'] = '非销户'
        extra.append(zh_msg)
        extra.append(zh_zh)
    # 合并
    dff = [df_pt_one] + extra + [df_pt_two, df_pt_three, df_pt_four, df_pt, df_pt_five, df_pt_ten]
    df_merge = reduce(lambda left, right: pd.merge(left, right, on=['主端卡号'], how='left'), dff)
    # df_merge.fillna(0,inplace=True)

    # 清洗
    # nan + 1 =nan 所以确保家数不存在nan ,交易次数理论上不存在nan故未处理,同时保证被除数不为nan和0,不会出现结果nan便于后续做判断
    for k in new_line:
        df_merge[k].fillna(0, inplace=True)

    df_merge['转账进款次数'].fillna(0, inplace=True)
    df_merge['转账出款次数'].fillna(1, inplace=True)  # 做除数
    df_merge['交易次数'].fillna(1, inplace=True)

    df_merge['消费率'] = (df_merge['生活消费次数'] + df_merge['三方支付充提次数'] + df_merge['三方转账/消费次数']) / df_merge['交易次数']
    df_merge['消费率'] = df_merge['消费率'].apply(lambda x: round(x, 2))
    df_merge['消费占比'] = (df_merge['生活消费金额'] + df_merge['三方支付充提金额'] + df_merge['三方转账/消费金额']) / df_merge['交易流水']
    df_merge['消费占比'] = df_merge['消费占比'].apply(lambda x: round(x, 2))
    df_merge['转账进出比'] = df_merge['转账进款次数'] / df_merge['转账出款次数']
    df_merge['转账进出比'] = df_merge['转账进出比'].apply(lambda x: round(x, 2))
    df_merge['大金额转账率'] = df_merge['大金额交易次数'] / df_merge['交易次数']
    # 性质判断
    df_merge['卡性质'] = df_merge.apply(primary_quality, axis=1)

    return df_merge


def cash_level_penetrate(df_df, direction, hour, mothon, collide=pd.DataFrame(), biaoshilie=pd.DataFrame(), only_bank=0,
                         only_cash=0):
    """
    :param df_df:
    :param direction:
    :param hour:
    :param mothon: 模式1,用上层碰撞结果;模式2,在MySQL中撞本批流水先找到目标(交易标识)
    :param collide:
    :param biaoshilie:
    :param only_bank:
    :param only_cash:
    :return:
    """
    if direction == '充值':
        direction = '进'

    if direction == '提现':
        direction = '出'

    df = df_df.copy().astype(str)

    if only_bank == 1:  # 是否只保留银行卡和支付宝号
        df['对端卡号'].fillna('-', inplace=True)
        start_with = ('6', '2088', '4', '34', '37', '51', '52', '53', '54', '55', '955')
        df = df[(df['对端卡号'].str.startswith(start_with)) & (df['对端卡号'].str.len() >= 10)].reset_index(drop=True)

    df['时间戳'] = df['时间戳'].astype('int64')
    df = df[df['交易结果'] == '成功']
    df["交易金额"] = pd.to_numeric(df["交易金额"])

    # 因均是从后往前找,所以穿透的方向影响数据的排序
    if direction == '进':
        df = df.sort_values(by=['主端卡号', '时间戳'], ascending=False).reset_index(drop=True)
    if direction == '出':
        df = df.sort_values(by=['主端卡号', '时间戳'], ascending=True).reset_index(drop=True)

    if mothon == 1:
        last_collide = collide.copy().astype(str)
        last_collide['时间戳'] = last_collide['时间戳'].astype('int64')
        last_collide["交易金额"] = pd.to_numeric(last_collide["交易金额"])

        # 设定范围减小处理时间
        new_waters = df[df['主端卡号'].isin(last_collide['对端卡号'])]
        last_collide = last_collide[last_collide['对端卡号'].isin(new_waters['主端卡号'])].reset_index(drop=True)
        new_waters = new_waters[new_waters['时间戳'] >= (last_collide['时间戳'].min() - hour * 3600)]
        new_waters = new_waters[new_waters['时间戳'] <= (last_collide['时间戳'].max() + hour * 3600)]
        new_waters = new_waters[new_waters['收付标志'] == direction].copy()

        pos_index = []
        collide_form = pd.DataFrame()

        for i in tqdm(last_collide.index, desc='匹配上层记录'):
            new_water_tmp = new_waters[new_waters['交易金额'] == last_collide.loc[i, '交易金额']]
            if new_water_tmp.empty:
                continue
            new_water_tmp = new_water_tmp[new_water_tmp['对端卡号'] == last_collide.loc[i, '主端卡号']]
            if new_water_tmp.empty:
                continue
            new_water_tmp = new_water_tmp[new_water_tmp['主端卡号'] == last_collide.loc[i, '对端卡号']]
            if new_water_tmp.empty:
                continue

            if last_collide.loc[i, '交易金额'] >= 10000:
                new_water_tmp = new_water_tmp[((last_collide.loc[i, '时间戳'] - 120) <= new_water_tmp['时间戳']) & (
                        new_water_tmp['时间戳'] <= (last_collide.loc[i, '时间戳'] + 120))]  # 发现过大额转账时间差距20多分钟
            else:
                new_water_tmp = new_water_tmp[((last_collide.loc[i, '时间戳'] - 10) <= new_water_tmp['时间戳']) & (
                        new_water_tmp['时间戳'] <= (last_collide.loc[i, '时间戳'] + 10))]

            if new_water_tmp.empty:
                continue

            pos_index = pos_index + list(new_water_tmp.index)
            tmp = pd.concat([last_collide[last_collide.index == i].reset_index(), new_water_tmp.reset_index()], axis=1)
            collide_form = pd.concat([collide_form, tmp])

        print('匹配上', len(pos_index))

    if only_cash == 1:
        return collide_form, pos_index

    if mothon == 2:
        # 筛选需寻找流水记录
        mask = (df['交易标识'].isin(biaoshilie['交易标识']))  # 目标筛选
        pos_index = np.flatnonzero(mask)  # 目标行号
        target = df.iloc[pos_index]  # target

    if mothon == 1:
        target = df[df.index.isin(pos_index)]

    print('目标', len(target), '重复', len(pos_index) - len(target))

    # 穿透
    relevancy = {}  # 结果
    skip = []  # 中途已找目标
    # 从后往前找,利于将连续的目标合并一起找,注意方向不同,排序不同
    result_index = []

    for i in tqdm(list(set(target['主端卡号'])), desc='资金穿透'):
        # 设置边界防止越界(合并表,防止找到其他主端数据)
        find_data = df[df['主端卡号'] == i]
        find_target = target[target['主端卡号'] == i]

        for index, row in find_target.iloc[::-1].iterrows():  # 倒序循环
            result_index.append(index)
            if index in skip:  # 检测是否已找过
                continue
            cash = row['交易金额']  # 起始需找金额
            # times = row['交易时间']  # 起始交易时间
            # time_array = time.strptime(times, "%Y-%m-%d %H:%M:%S")
            # time_stamp = int(time.mktime(time_array))  # 转时间戳

            money = 0  # 已找金额
            zh_list = []  # 已找对端
            start_zh = [row['对端卡号']]

            for inds in reversed(range(index)):  # 从起始行号往前找
                if inds < find_data.index[0]:  # 找到该主端数据最新数据结束
                    break
                p = df.iloc[inds]  # 获取该条数据
                # if abs(time_stamp - int(time.mktime(time.strptime(p['交易时间'], "%Y-%m-%d %H:%M:%S")))) >= hour * 3600:  # 判断是否在起始时间之前,不在则结束
                if abs(int(row['时间戳']) - int(p['时间戳'])) >= (hour * 3600):  # 判断是否在起始时间之前,不在则结束
                    break
                # 若为同方向则判断是否也是要找的目标并记录行号及对端,将金额累加到需要找到金额
                if p['收付标志'] == direction:
                    if inds in list(pos_index):
                        cash = cash + p['交易金额']
                        skip.append(inds)
                        start_zh.append(p['对端卡号'])
                    continue
                # 记录已找到金额及对端
                money = money + p['交易金额']
                zh_list.append(p['对端卡号'])

                result_index.append(inds)

                # 判断是否到达需找金额
                if money >= cash:
                    break
            # 记录结果
            relevancy[str(money) + '#' + str(start_zh) + '@' + i + '=' + str(row['时间戳']) + '$' + str(cash)] = zh_list

    outcome = pd.DataFrame(list(relevancy.items()), columns=['上一层', '下一层'])

    # 清洗
    outcome = outcome.astype(str)

    outcome['总金额'] = outcome['上一层'].apply(lambda x: x.split('$')[1])
    outcome['总金额'] = pd.to_numeric(outcome['总金额'])
    outcome['起点交易时间'] = outcome['上一层'].apply(lambda x: x.split('$')[0].split('=')[1])
    outcome['主端'] = outcome['上一层'].apply(lambda x: x.split('$')[0].split('=')[0].split('@')[1])
    outcome['上层'] = outcome['上一层'].apply(lambda x: x.split('$')[0].split('=')[0].split('@')[0].split('#')[1])
    outcome['已找到金额'] = outcome['上一层'].apply(lambda x: x.split('$')[0].split('=')[0].split('@')[0].split('#')[0])
    outcome['已找到金额'] = pd.to_numeric(outcome['已找到金额'])
    outcome.drop(['上一层'], axis=1, inplace=True)
    outcome.replace("[\()['\]]", '', regex=True, inplace=True)

    # 调整顺序
    outcome.insert(0, '上一层', outcome.pop('上层'))
    outcome.insert(1, '主端', outcome.pop('主端'))
    outcome.insert(4, '已找到金额', outcome.pop('已找到金额'))
    outcome['下一层'] = outcome.pop('下一层')

    collide_next = df[df.index.isin(result_index)]
    collide_next['对端iscard'] = collide_next['对端卡号'].apply(luhn_iscard)

    if mothon == 1:
        return collide_next, collide_form, outcome
    if mothon == 2:
        return collide_next, outcome
