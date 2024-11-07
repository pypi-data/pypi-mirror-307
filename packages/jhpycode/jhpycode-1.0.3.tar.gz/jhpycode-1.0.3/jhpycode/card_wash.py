import pandas as pd
import numpy as np
import wash_tool
import data_fenxi
from datetime import datetime


class BankData:
    def __init__(self,user_detail):
        self.detail = user_detail
        self.detail = self.qin_xi(self.detail,['主端卡号','主端账号'],True)
        self.detail,self.bad_line = self.wash_card_deal()
        self.columns = list(self.detail.columns)
        
    def qin_xi(self,df_wash,card_qin_xi=None,update_name=False):
        df_wash = df_wash.rename(columns=lambda x: x.replace('\t', ''))
        df_wash = df_wash.replace(r'\t\|', '', regex=True)
        df_wash = df_wash.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        df_wash = df_wash.loc[:, ~df_wash.columns.str.contains('^Unnamed')]
        
        if update_name:
            df_wash = self.unification_name_and_get_line(df_wash)
            
        if card_qin_xi:
            for l in card_qin_xi:
                df_wash[l] = df_wash[l].fillna('').str.split('_|-', expand=True)[0]
                df_wash[l] = df_wash[l].apply(lambda x: x[:-4] if x[-4:] == 'CNY0' else x)
                df_wash[l] = df_wash[l].apply(lambda x: x[:-6] if x[-6:] == '000156' and len(x) > 20 else x)

        return df_wash.drop_duplicates(keep='first').reset_index(drop=True)
        
    @staticmethod
    def unification_name_and_get_line(df_rename):
            must_line = ['主端卡号','主端账号','主端姓名','交易时间','交易金额','交易余额','收付标志','对端卡号','对端姓名','交易结果','交易摘要','交易网点']
            extra_line = ['对端银行','IP地址','MAC地址','商户名称','交易类型','备注']
            
            rename_dicts = {'主端卡号': ['交易卡号','查询卡号'],
                            '主端账号': ['交易账号','查询账号'],
                            '主端姓名': ['交易方户名','交易户名'],
                            '交易时间': ['交易时间'],
                            '收付标志': ['借贷标志'],
                            '对端卡号': ['对方账号卡号', '交易对手账卡号','对手卡号'],
                            '对端姓名': ['对方账号姓名', '对手户名'],
                            '交易金额': ['金额'],
                            '交易余额': ['余额'],
                            '交易结果': ['交易是否成功'],
                            '交易摘要': ['摘要说明'],
                            '对端银行': ['对手开户银行','交易开户行'],
                            '交易网点': ['交易网点名称']
            }
            
            for key, value in rename_dicts.items():
                df_rename = df_rename.rename(columns=lambda x: key if x in value else x)
            

            all_line = must_line + extra_line
            for line in all_line:
                if line not in df_rename.columns:
                    df_rename[line] = ''
                
            df_rename = df_rename[all_line]
            return df_rename
    
    def wash_card_deal(self):
        new_df = self.detail.copy()
        new_df = new_df.applymap(lambda x:x if pd.isnull(x) else str(x).replace('', '')) #去除非法字符
        new_df['收付标志'].replace(['C','贷','入'],'进', inplace=True)
        new_df['收付标志'].replace(['D','借'],'出', inplace=True)
        new_df = new_df[new_df['收付标志'].isin(['进','出'])]
        # df.drop(df[df[df.columns[0]] == df.columns[0]].index,inplace=True)
        new_df['交易结果'].replace(['01','1','','00','Y'],'成功', inplace=True)
        new_df['交易结果'].replace(['02','2','N'],'失败', inplace=True)
        new_df = new_df[new_df['交易结果'].isin(['成功','失败'])]
        new_df['交易结果'] = new_df.apply(lambda row: '成功' if row['交易网点'] == '梅州客商银行股份有限公司' else row['交易结果'], axis=1)
        
        # new_df['主端账号'] = new_df['主端账号'].astype(str)
        
        new_df['对端卡号'] = new_df['对端卡号'].fillna('').apply(lambda x: x.split('+')[1] if x.startswith('+') else x)
        
        new_df["交易余额"] = pd.to_numeric(new_df["交易余额"], errors='coerce').dropna()
        new_df["交易金额"] = pd.to_numeric(new_df["交易金额"], errors='coerce').dropna()
        new_df["交易金额"] = abs(new_df["交易金额"])
        

        new_df['交易时间'] = new_df['交易时间'].apply(wash_tool.format_time)
        new_df["交易时间"] = pd.to_datetime(new_df["交易时间"], errors='coerce', format='%Y-%m-%d %H:%M:%S')
        
        new_df = new_df.replace('',np.nan)
        new_df.dropna(subset=['交易金额', '收付标志', '交易时间', '交易结果'], how='any', inplace=True)
        
        # 对端判断
        # tqdm.pandas(desc='交易性质判断')
        # new_df['交易判断'] = new_df.progress_apply(data_fenxi.peer_quality, axis=1)
        # 时间戳
        new_df['时间戳'] = new_df['交易时间'].astype('int64') // 10**9 - 28800
        
        new_df['对端isCard'] = new_df['对端卡号'].apply(wash_tool.luhn_iscard)
        
        
        new_df = self.creat_key(new_df)
        new_df = new_df.sort_values(['主端卡号','交易时间','交易类型','交易摘要','备注'], ascending=False)
        new_df.drop_duplicates(subset=['交易标识'],keep='first',inplace=True)
        
        bad_lines = self.detail[~self.detail.index.isin(new_df.index.tolist())]
        bad_lines = bad_lines.applymap(lambda x:x if pd.isnull(x) else str(x).replace('', ''))
        
        return new_df.reset_index(drop=True),bad_lines.reset_index(drop=True)
    
    @staticmethod
    def creat_key(df_key):
        new_df = df_key
        new_df['交易标识'] = new_df.apply(wash_tool.calculate_hash, axis=1)
        return new_df
    
    
    def fenxi(self):
        tmp = data_fenxi.card_analyse(self.detail)
        return tmp

class JZBankData(BankData):
    def __init__(self,user_detail,user_msg=None,task_msg=None,freeze_msg=None,people_msg=None,diao=pd.DataFrame(),duke=pd.DataFrame()):
        super().__init__(user_detail)
        self.user_all = None
        self.user = user_msg
        self.task = task_msg
        self.freeze = freeze_msg
        self.people = people_msg
        self.diao = diao
        self.duke_card = duke
        self.others_msg_clean()
        # self.detail = self.creat_key(self.detail)
        self.final_step()
    
    def final_step(self):
        if not self.diao.empty:
            self.useless = self.detail[~self.detail['主端卡号'].isin(self.diao['调取卡号'])]
            self.detail = self.detail[self.detail['主端卡号'].isin(self.diao['调取卡号'])]
            print('清洗后数据:',len(self.detail),'行','  清洗掉数据:',len(self.bad_line),'行','  反馈外数据:',len(self.useless),'行')
        else:
            print('清洗后数据:',len(self.detail),'行','  清洗掉数据:',len(self.bad_line))
    
    @staticmethod  
    def adjust_card(x):
        if not wash_tool.luhn_iscard(x['主端卡号']):
            if wash_tool.luhn_iscard(x['交易卡号']):
                return x['交易卡号']
        return x['主端卡号']
    
    def others_msg_clean(self):
        zh = self.qin_xi(self.user,['交易账号','交易卡号'])
        zh = zh.rename(columns={'交易账号':'主端账号'})
        zh.insert(0, '交易卡号', zh.pop('交易卡号'))
        
        zh_name =zh.query('交易卡号 != "" and 账户开户名称 != ""')
        self.name = zh[['交易卡号','账户开户名称']].drop_duplicates(keep='first')
        self.name.rename(columns={'交易卡号':'主端卡号'},inplace=True)
        
        zh_name =zh.query('主端账号 != "" and 账户开户名称 != ""')
        self.name_z = zh[['主端账号','账户开户名称']].drop_duplicates(keep='first')
        
        zh = zh.query('主端账号 != "" and 交易卡号 != ""')
        self.user_all = zh.dropna(subset=['主端账号', '交易卡号'], how='all')
        self.user_all = self.user_all.applymap(lambda x:x if pd.isnull(x) else str(x).replace('', ''))

        
        tmp_zh = zh[['主端账号','交易卡号']].drop_duplicates(keep='first')
        value_counts = tmp_zh['主端账号'].value_counts()   # 选取一对一的账户匹配避免重复数据
        tmp_zh = tmp_zh[tmp_zh['主端账号'].isin(value_counts[value_counts == 1].index)]
        card_counts = tmp_zh['交易卡号'].value_counts()
        tmp_zh = tmp_zh[tmp_zh['交易卡号'].isin(card_counts[card_counts == 1].index)]
        self.user = tmp_zh

        #人员信息
        pe = self.qin_xi(self.people)
        # pe['户籍地'] = pe['证照号码'].apply(parseIdCard.parseIdCard).apply(lambda x : x['area'])
        # pe['年龄'] = pe['证照号码'].apply(parseIdCard.parseIdCard).apply(lambda x : x['age'])
        # pe.insert(3, '户籍地', pe.pop('户籍地'))
        # pe.insert(4, '年龄', pe.pop('年龄'))
        self.people = pe
        
        # 冻结信息清洗
        dj = self.qin_xi(self.freeze,['账号'])
        dj = dj.rename(columns={'账号':'主端卡号'})
        dj = dj[(dj['主端卡号'] != ' ') & (dj['主端卡号'].notna()) & (dj['主端卡号'] != '')]
        dj = pd.merge(dj,self.user,left_on='主端卡号',right_on='主端账号',how='left')
        dj['主端卡号'] = dj.apply(lambda x: x['交易卡号'] if pd.notnull(x['交易卡号']) else x['主端卡号'],axis=1)
        dj.drop(['主端账号','交易卡号'],axis=1,inplace=True)
        self.freeze = data_fenxi.location_extract(dj,'冻结机关') # 标准化公安地址
        self.freeze = self.freeze.applymap(lambda x:x if pd.isnull(x) else str(x).replace('', ''))

        #任务反馈清洗
        if not self.task.empty:
            rw = self.qin_xi(self.task)
            rw = rw[['账卡号','反馈结果']].rename(columns={'账卡号':'主端卡号'}).drop_duplicates(keep='first')
            rw['反馈结果'] = rw['反馈结果'].astype(str)
            rw = pd.pivot_table(rw, values='反馈结果', index='主端卡号', aggfunc=' $$ '.join).reset_index()
            rw = pd.merge(rw,self.user,left_on='主端卡号',right_on='主端账号',how='left')
            rw['主端卡号'] = rw.apply(lambda x: x['交易卡号'] if pd.notnull(x['交易卡号']) else x['主端卡号'],axis=1)
            rw.drop(['主端账号','交易卡号'],axis=1,inplace=True)
            self.task = rw.replace({'反馈结果':{'':'无信息'}})
        
        # 信息补全
        # 替换账号为卡号
        new_df = pd.merge(self.detail,self.user, on='主端账号',how='left')
        new_df['主端卡号'] = new_df['主端卡号'].fillna(new_df['交易卡号'])
        new_df['主端卡号'] = new_df['主端卡号'].fillna(new_df['主端账号'])
        new_df['主端卡号']= new_df.apply(self.adjust_card,axis=1)
        new_df.drop(['交易卡号'], axis=1,inplace=True)
        
        new_df = pd.merge(new_df,self.name, on='主端卡号',how='left')
        new_df['主端姓名'] = new_df['主端姓名'].fillna(new_df['账户开户名称'])
        new_df.drop(['账户开户名称'], axis=1,inplace=True)
        
        new_df = pd.merge(new_df,self.name_z, on='主端账号',how='left')
        new_df['主端姓名'] = new_df['主端姓名'].fillna(new_df['账户开户名称'])
        new_df.drop(['账户开户名称'], axis=1,inplace=True)
        
        if not self.diao.empty:
            d_name = self.diao[['调取卡号','姓名']].rename(columns={'调取卡号':'主端卡号'})
            new_df = pd.merge(new_df,d_name, on='主端卡号',how='left')
            new_df['主端姓名'] = new_df['主端姓名'].fillna(new_df['姓名'])
            new_df.drop(['姓名'], axis=1,inplace=True)
        
        # 新增列
        # 对端赌客匹配
        if not self.duke_card.empty:
            dk = self.duke_card[['赌客卡号']].drop_duplicates(keep='first')
            new_df['对端isDuke'] = new_df['对端卡号'].isin(dk['赌客卡号'])
            
        self.detail = new_df   
        
        # 冻结情况匹配
        # dj_card = dj[['主端卡号']]
        # dj_card = dj_card['主端卡号'].value_counts().reset_index().rename(columns={'count':'冻结次数'})
        # self.detail = pd.merge(df,dj_card,how='left',on='主端卡号')
    
    def fenxi(self):
        tmp = data_fenxi.card_analyse(self.detail,self.user_all)
        return tmp

    def report(self):
        
        alldata = self.detail.copy()

        data_sum = (pd.pivot_table(alldata[['主端卡号','主端姓名','交易金额']],index=["主端卡号",'主端姓名'],values='交易金额',aggfunc=['sum','count']).reset_index())
        data_sum.columns = ['_'.join(col) for col in data_sum.columns.values]
        data_sum.rename(columns={'sum_交易金额':'交易流水','count_交易金额':'数据量','主端卡号_':'主端卡号','主端姓名_':'主端姓名'}, inplace=True)
        data_sum = data_sum[data_sum['主端卡号'] != '']
        
        dj_card = self.freeze[['主端卡号']]
        
        rows = ' '
        if not self.diao.empty:
            dj_card = dj_card[dj_card['主端卡号'].isin(self.diao['调取卡号'])]
            rows, columns = self.diao.shape
            
        dj_card = dj_card['主端卡号'].value_counts().reset_index().rename(columns={'count':'冻结次数'})
        
        alldata_paixu = alldata.sort_values(by=['时间戳'],ascending=False).reset_index(drop=True)
        first_file_mtime = alldata_paixu.loc[0,'时间戳']
        datatime = datetime.fromtimestamp(first_file_mtime).strftime('%Y-%m-%d') 
        
        presently_money = alldata_paixu.groupby('主端卡号').first()
        all_presently_money = int(presently_money['交易余额'].sum())
        money_water = int(alldata['交易金额'].sum())
        
        fankui_table = pd.merge(data_sum,dj_card,how='outer',on='主端卡号') # 添加数据量信息
        fankui_table = pd.merge(fankui_table,presently_money.reset_index()[['主端卡号','交易时间','交易余额']],how='outer',on='主端卡号')
        fankui_table.rename(columns={'交易时间':'最后交易时间'},inplace=True)
        
        if not self.diao.empty:
            fankui_table = pd.merge(self.diao,fankui_table,how='outer',left_on='调取卡号',right_on='主端卡号')
            
        freeze_presently_money = fankui_table[fankui_table['冻结次数'].isnull()]['交易余额'].sum()
            
        dongjie_card = fankui_table['冻结次数'].count()
        fankuishui = fankui_table['主端卡号'].count()
        
        djga = self.freeze.groupby('冻结机关').agg({'主端卡号': 'nunique'}).reset_index().sort_values(by=['主端卡号'],ascending=False)
        djquyushi = self.freeze.groupby('市').agg({'主端卡号': 'nunique'}).reset_index().sort_values(by=['主端卡号'],ascending=False)
        djquyu = self.freeze.groupby('省').agg({'主端卡号': 'nunique'}).reset_index().sort_values(by=['主端卡号'],ascending=False)
        ga_num = djga['冻结机关'].count()
        
        # 停用情况
        day30 = 0
        day180 = 0
        day90 = 0
        for index,row in presently_money.iterrows():
            if 2592000 <= first_file_mtime - row['时间戳']:
                day30 = day30 + 1
            if 7776000 <= first_file_mtime - row['时间戳']:
                day90 = day90 + 1
            if 15552000 <= first_file_mtime - row['时间戳']:
                day180 = day180 + 1
        
        # 余额占比     
        DESC_presently_money = presently_money.sort_values(by=['交易余额'],ascending=False).reset_index()
        
        # 余额占比方案二
        DESC_presently_money['CumSum'] = DESC_presently_money['交易余额'].cumsum()
        threshold_value = DESC_presently_money['交易余额'].sum() * 0.6
        threshold_value_2 = DESC_presently_money['交易余额'].sum() * 0.8
        result1 = DESC_presently_money[DESC_presently_money['CumSum'] < threshold_value]['交易余额'].count() + 1
        result2 = DESC_presently_money[DESC_presently_money['CumSum'] < threshold_value_2]['交易余额'].count() + 1
        
        useful_presently_money = all_presently_money-freeze_presently_money
        
        fankui = {"处理日期": f'处理日期：{datetime.now().strftime("%Y-%m-%d")}',
                  '数据时间': f'数据时间：{datatime}',
                  # '调取批次': f'调取批次：{批次}',
                  '调取情况': f'调取情况：调取银行卡{rows}张',
                  '本次反馈': f'本次反馈：反馈{fankuishui}张',
                  "冻结情况": f'冻结情况：被冻{dongjie_card}张,公安{ga_num}个',
                  '冻结公安': f'冻结公安：{djquyu.iloc[0, 0]}{djquyu.iloc[0, 1]}张,{djquyu.iloc[1, 0]}{djquyu.iloc[1, 1]}张,{djquyu.iloc[2, 0]}{djquyu.iloc[2, 1]}张',
                  "流水情况": f'流水情况：总流水 {wash_tool.str_of_num(money_water)}元',
                  "余额情况": f'余额情况：总余额 {wash_tool.str_of_num(all_presently_money)}元,未冻余额 {wash_tool.str_of_num(useful_presently_money)}元',
                  '余额分布': f'余额分布：前{result2}个账户余额占80%,前{result1}个账户余额占60%',
                  "停用情况": f"停用情况：超1个月{day30}张,超过3个月{day90}张,超过6个月{day180}张"}
        
        fankuimessage = pd.DataFrame(list(fankui.items()),columns=['标题', '情况'])
        fankui_table = pd.concat([fankui_table, fankuimessage[['情况']]], axis=1)  
        return fankui_table.rename(columns={'主端卡号': '反馈卡号'})

class ZABankData(BankData):
    def __init__(self,user_detail,diao=pd.DataFrame(),duke=pd.DataFrame()):
        super().__init__(user_detail)
        self.diao = diao
        self.duke_card = duke
        self.others_clean()
        self.final_step()
    
    def final_step(self):
        if not self.diao.empty:
            self.useless = self.detail[~self.detail['主端卡号'].isin(self.diao['调取卡号'])]
            self.detail = self.detail[self.detail['主端卡号'].isin(self.diao['调取卡号'])]
            print('清洗后数据:',len(self.detail),'行','  清洗掉数据:',len(self.bad_line),'行','  反馈外数据:',len(self.useless),'行')
        else:
            print('清洗后数据:',len(self.detail),'行','  清洗掉数据:',len(self.bad_line))
        
    def others_clean(self):
        new_df = self.detail.copy()
        if not self.diao.empty:
            d_name = self.diao[['调取卡号','姓名']].rename(columns={'调取卡号':'主端卡号'})
            new_df = pd.merge(new_df,d_name, on='主端卡号',how='left')
            new_df['主端姓名'] = new_df['主端姓名'].fillna(new_df['姓名'])
            new_df.drop(['姓名'], axis=1,inplace=True)
        if not self.duke_card.empty:
            dk = self.duke_card[['赌客卡号']].drop_duplicates(keep='first')
            new_df['对端isDuke'] = new_df['对端卡号'].isin(dk['赌客卡号'])
        self.detail = new_df 

    def report(self):
        alldata = self.detail.copy()

        data_sum = (pd.pivot_table(alldata[['主端卡号','交易金额']],index=["主端卡号"],values='交易金额',aggfunc=['sum','count']).reset_index())
        data_sum.columns = ['_'.join(col) for col in data_sum.columns.values]
        data_sum.rename(columns={'sum_交易金额':'交易流水','count_交易金额':'数据量','主端卡号_':'主端卡号'}, inplace=True)
        data_sum = data_sum[data_sum['主端卡号'] != '']
        
        rows = ' '
        if not self.diao.empty:
            rows, columns = self.diao.shape
            
        alldata_paixu = alldata.sort_values(by=['时间戳'],ascending=False).reset_index(drop=True)
        first_file_mtime = alldata_paixu.loc[0,'时间戳']
        datatime = datetime.fromtimestamp(first_file_mtime).strftime('%Y-%m-%d') 
        
        presently_money = alldata_paixu.groupby('主端卡号').first()
        all_presently_money = int(presently_money['交易余额'].sum())
        money_water = int(alldata['交易金额'].sum())
        
        fankui_table = pd.merge(data_sum,presently_money.reset_index()[['主端卡号','交易时间','交易余额']],how='outer',on='主端卡号')
        fankui_table.rename(columns={'交易时间':'最后交易时间'},inplace=True)
        
        if not self.diao.empty:
            fankui_table = pd.merge(self.diao,fankui_table,how='outer',left_on='调取卡号',right_on='主端卡号')
            
        fankuishui = fankui_table['主端卡号'].count()
        
        # 停用情况
        day30 = 0
        day180 = 0
        day90 = 0
        for index,row in presently_money.iterrows():
            if 2592000 <= first_file_mtime - row['时间戳']:
                day30 = day30 + 1
            if 7776000 <= first_file_mtime - row['时间戳']:
                day90 = day90 + 1
            if 15552000 <= first_file_mtime - row['时间戳']:
                day180 = day180 + 1
        
        # 余额占比     
        DESC_presently_money = presently_money.sort_values(by=['交易余额'],ascending=False).reset_index()
        
        # 余额占比方案二
        DESC_presently_money['CumSum'] = DESC_presently_money['交易余额'].cumsum()
        threshold_value = DESC_presently_money['交易余额'].sum() * 0.6
        threshold_value_2 = DESC_presently_money['交易余额'].sum() * 0.8
        result1 = DESC_presently_money[DESC_presently_money['CumSum'] < threshold_value]['交易余额'].count() + 1
        result2 = DESC_presently_money[DESC_presently_money['CumSum'] < threshold_value_2]['交易余额'].count() + 1
        
        
        fankui = {"处理日期": f'处理日期：{datetime.now().strftime("%Y-%m-%d")}',
                  '数据时间': f'数据时间：{datatime}',
                  # '调取批次': f'调取批次：{批次}',
                  '调取情况': f'调取情况：调取银行卡{rows}张',
                  '本次反馈': f'本次反馈：反馈{fankuishui}张',
                  "流水情况": f'流水情况：总流水 {wash_tool.str_of_num(money_water)}元',
                  "余额情况": f'余额情况：总余额 {wash_tool.str_of_num(all_presently_money)}元',
                  '余额分布': f'余额分布：前{result2}个账户余额占80%,前{result1}个账户余额占60%',
                  "停用情况": f"停用情况：超1个月{day30}张,超过3个月{day90}张,超过6个月{day180}张"}
        
        fankuimessage = pd.DataFrame(list(fankui.items()),columns=['标题', '情况'])
        fankui_table = pd.concat([fankui_table, fankuimessage[['情况']]], axis=1) 

        return fankui_table.rename(columns={'主端卡号': '反馈卡号'}) 