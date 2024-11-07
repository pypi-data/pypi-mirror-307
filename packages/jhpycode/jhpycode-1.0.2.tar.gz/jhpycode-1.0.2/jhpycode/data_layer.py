import pandas as pd
from data_get import get_data
from tqdm import tqdm

def agent_under_people(uid: str, invite_id: str):
    """
    代理关系表计算会员伞下人数及具体伞下会员ID
    :param uid: 会员ID列
    :param invite_id: 上级ID列
    :return: df2 : 伞下会员表
    """
    # 读取数据框
    df = pd.read_excel(get_data(), dtype='str')
    df2 = pd.DataFrame(columns=['ID', '伞下人数'])
    dict_members = {}

    def count_subordinates(userid, members_list):
        count = 0
        subordinates = df[df[invite_id] == userid][uid]
        members_list.extend(list(subordinates))
        count += len(subordinates)
        for subordinate in subordinates:  # 如果subordinates为空则递归结束
            count += count_subordinates(subordinate, members_list)[0]
        return count, members_list

        # 计算每个用户ID下级各级成员的数量

    for user_id in tqdm(df[uid]):
        members = []
        result = count_subordinates(user_id, members)
        total_count = result[0]
        dict_members[user_id] = result[1]
        # print(f"用户ID {user_id} 下级各级成员数量: {total_count}")
        df2.loc[len(df2.index)] = [user_id, total_count]
    df2['ID'] = df2['ID'].astype("str")
    dict_members = [{'ID': k, 'value': v} for k, v in dict_members.items()]
    df3 = pd.DataFrame(dict_members).astype("str")
    df2 = pd.merge(df2, df3, on='ID')
    return df2


def agent_under_layer(uid: str, invite_id: str):
    """
    代理关系表计算会员向下还有多少层
    :param uid: 会员ID列
    :param invite_id: 上级ID列
    :return: df2: 向下级层级表
    """
    # 加载数据到DataFrame
    df = pd.read_excel(get_data(), dtype='str')

    # 递归函数计算层级
    def calculate_level(df1, id1, level=1):
        # 找到当前id的所有下级id
        sub_ids = df1[df1[invite_id] == id1][uid]

        # 如果没有下级id，则返回当前层级
        if len(sub_ids) == 0:
            return level

        # 否则，递归计算下级id的层级，并返回最大层级
        return max(calculate_level(df, sub_id, level + 1) for sub_id in sub_ids)

    # 计算每个id的层级
    tqdm.pandas(desc='apply')
    df['层级'] = df[uid].progress_apply(lambda x: calculate_level(df, x))
    df2 = df[[uid, '层级']]
    df2[uid] = df2[uid].astype("str")
    return df2


def agent_up_layer(uid: str, invite_id: str):
    """
    代理关系表计算向上层级及路径上的会员ID
    :param uid: 会员ID列
    :param invite_id: 上级ID列
    :return: df: 向上层级表
    """

    def calculate_level(user_id, uids, invite_uids):
        # 找到用户ID对应的上级ID
        superior = df[df[uids] == user_id][invite_uids]
        # 如果上级ID为空，则说明已经到达最上级，返回空列表
        if superior.empty:
            return []

        parent_id = superior.values[0]

        # if pd.isnull(parent_id):
        #     return []

        # 递归调用函数，计算上级ID的上级ID
        parents = calculate_level(parent_id, uids, invite_uids)

        # 返回上级ID的上级ID列表，加上当前上级ID
        return parents + [parent_id]

    df = pd.read_excel(get_data(), dtype='str')
    tqdm.pandas(desc='apply')
    df['上级'] = df[uid].progress_apply(lambda x: calculate_level(x, uid, invite_id))
    df['账户层级'] = df['上级'].apply(lambda x: len(x))
    df = df[[uid, '账户层级', '上级']].astype('str')

    return df