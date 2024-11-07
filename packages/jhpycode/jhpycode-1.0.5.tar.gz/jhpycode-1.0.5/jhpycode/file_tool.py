import os
import pandas as pd
from tqdm import tqdm
from  data_get import get_file_folder,get_data

def table_splitting(df_df, lie: str):
    """
    按某列拆分文件
    :param df_df: 需要拆分的数据
    :param lie: 拆分列
    """
    df = df_df
    path = get_file_folder()
    card_list = list(set(df[lie]))
    for card in tqdm(card_list):
        if pd.isnull(card):
            continue
        card_data = df[df[lie] == card]
        card_data.to_excel(path + '/' + card + '.xlsx', index=False)


def files_classify():
    """
    以移动清单移动文件，需要准备一个文件清单包含需要移动的文件名和移动后的文件夹。
    也可完成每个文件建一个文件夹
    """
    # 读取清单.xlsx
    checklist = pd.read_excel(get_data(), dtype='str')

    # 读取需要整理的文件夹
    folder_path = get_file_folder()

    # 遍历清单中的每一行
    for index, row in checklist.iterrows():
        # 获取文件名和文件夹名
        file_name = row[0]
        folder_name = row[1]
        # 在需要整理的文件夹下新建文件夹
        new_folder_path = os.path.join(folder_path, folder_name)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)

        # 遍历需要整理的文件夹下的文件
        for file in os.listdir(folder_path):
            # 如果文件名包含清单中的字符串，则移动到相应文件夹
            if file_name in file:
                old_file_path = os.path.join(folder_path, file)
                new_file_path = os.path.join(new_folder_path, file)
                os.rename(old_file_path, new_file_path)