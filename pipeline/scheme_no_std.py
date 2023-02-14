import csv
import re
import pandas as pd
from utils.constants import TRIAL_INFO_PATH


def standard_janssen_scheme_no():
    pd.options.mode.chained_assignment = None
    phase_info = pd.read_csv(TRIAL_INFO_PATH, encoding='utf-8')
    for i in range(0, len(phase_info['scheme_no'])):
        phase_info['scheme_no'][i] = ''.join(str(phase_info['scheme_no'][i]))
        # 格式化 杨森 scheme_no 的代码
        sp_data = re.sub('[;|；|修|，|,].*', '', phase_info['scheme_no'][i])
        sp_data = re.sub('-INT.*', '', sp_data)
        phase_info['standard_scheme_no'][i] = sp_data
    phase_info.to_csv(TRIAL_INFO_PATH, index=False)
    print('------------------- Janssen_Scheme_no 格式化')


def standard_all_scheme_no():
    pd.options.mode.chained_assignment = None
    # phase_info = pd.read_csv(TRIAL_INFO_PATH, encoding='utf-8')
    phase_info = pd.read_csv('./trial_info.csv', encoding='utf-8')
    for i in range(0, len(phase_info['scheme_no'])):
        phase_info['scheme_no'][i] = ''.join(str(phase_info['scheme_no'][i]))
        sp_data = re.sub('^[\u4e00-\u9fa5].*[：|:]', '', phase_info['scheme_no'][i])
        sp_data = re.sub('[\u4e00-\u9fa5](\-|\+)?\d+(\.\d+)?[\u4e00-\u9fa5]', '', sp_data)
        sp_data = re.sub('[\u4e00-\u9fa5]|;|；|，|,|:|：|.{4}年.{1,2}月.{1,2}日', '♢', sp_data)
        sp_data = re.sub('^♢*', '', sp_data)
        sp_data = re.sub('♢.*|（.*|\(.*', '', sp_data)
        sp_data = re.sub('[V|v][0-9]\.[0-9]*.*', '', sp_data)
        sp_data = re.sub('[0-9]\.[0-9]*.*', '', sp_data)
        sp_data = re.sub('.{4}年.{1,2}月.{1,2}日版', '', sp_data)
        sp_data = re.sub('[0-9][0-9]版', '', sp_data)
        sp_data = re.sub('[\u4e00-\u9fa5]+\D', '', sp_data)
        sp_data = re.sub('[\u4e00-\u9fa5].*', '', sp_data)
        print(f'{phase_info["scheme_no"][i]}' + '------------' + f'{sp_data}')
    print('------------------- scheme_no 格式化')


def standard_test_scheme_no():
    pd.options.mode.chained_assignment = None
    # phase_info = pd.read_csv(TRIAL_INFO_PATH, encoding='utf-8')
    phase_info = pd.read_csv('./trial_info.csv', encoding='utf-8')
    for i in range(0, len(phase_info['scheme_no'])):
        phase_info['scheme_no'][i] = ''.join(str(phase_info['scheme_no'][i]))
        # 格式化 杨森 scheme_no 的代码
        sp_data = re.sub('[;|；|修|，|,].*', '', phase_info['scheme_no'][i])
        sp_data = re.sub('-INT.*', '', sp_data)
        phase_info['standard_scheme_no'][i] = sp_data
    phase_info.to_csv('./dd/trial_info.csv', index=False)
    print('------------------- Janssen_scheme_no 格式化')

# standard_test_scheme_no()
