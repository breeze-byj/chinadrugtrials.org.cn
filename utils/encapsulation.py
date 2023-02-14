import csv
import ast
import configparser
import hashlib
import random
import time
from datetime import datetime
from string import ascii_letters
import pandas as pd
import os
import zipfile
import win32file as w

from utils.constants import CFDI_SITE_INFO_PATH


def get_data_str2_rnt(xpath, html):
    try:
        text = html.xpath(f'normalize-space({xpath})')[0]
    except:
        text = ''
    return text


def get_data_str_rnt(xpath, html):
    # normalize-space({xpath}) :xpath内部函数，获取到的数据忽略\r\n\t
    try:
        text = html.xpath(f'normalize-space({xpath})')[0].text
    except:
        text = ''
    return text


def get_data_str2(xpath, html):
    try:
        text = html.xpath(xpath)[0]
    except:
        text = ''
    return text


def get_data_str(xpath, html):
    try:
        text = html.xpath(xpath)[0].text
    except:
        text = ''
    return text


def wri_tit(csv_name, tit_list):
    '''
    Args: 在csv文件中写入title
        csv_name: 文件名称
        tit_list: 写入的title_lisy[1,2,3]
    '''
    if os.access(csv_name, os.F_OK):
        df = pd.read_csv(csv_name, header=None, names=tit_list)
        df.to_csv(csv_name, index=False)


# 如果字符串的第一个空格无法删除则调用此方法
def str_sub(string):
    new = []
    for s in string:
        new.append(s)
    try:
        if new[1] == ' ':
            del new[1]
    except:
        pass
    return ''.join(new)


def csv_deduplication(file):
    '''
    Args: csv文件去重
        file: 文件名称
    '''
    df = pd.read_csv(file, header=0, encoding='utf-8')
    datalist = df.drop_duplicates()
    datalist.to_csv(file, encoding='utf-8', header=None, index=None)


def zip_ya(startdir, file_news):
    '''
    Args: 压缩文件夹
        startdir: 需要压缩的文件夹
        file_news: 压缩包的位置/名称
    '''
    time.sleep(2)
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir, '')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath + filename)
    print('------------------- 打包')
    z.close()


def str_del_index(str, index):
    '''
    Args: 根据下标删除字符
        str:进行操作的字符串
        index:要删除的位置
    Returns:
        _str:删除完成后的字符串
    '''
    _str = ''
    if index < 0:
        str = str[::-1]
        index = 0 - index - 1
        for i in range(len(str)):
            if i == index:
                continue
            _str += str[i]
        _str = _str[::-1]
    else:
        for i in range(len(str)):
            if i == index:
                continue
            _str += str[i]
    return _str


def write_csv(file_name, data_list_name):
    '''
    Args:写入csv
        file_name: 文件位置
        data_list_name: 写入的数据[[1,2,3]]
    '''
    with open(file_name, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if file_name==CFDI_SITE_INFO_PATH:
            print(data_list_name[0])
            print(len(data_list_name))
        for row in data_list_name:
            writer.writerow(row)


def delete_all_csv():
    '''
    Args:删除文件
    '''
    print('------------------- 删除')
    files = os.listdir('./data_input/CDE/cde_export')
    for filename in files:
        os.remove(f'./data_input/CDE/cde_export/{filename}')


def conf_eval_data(group_name, value_name, text):
    '''
    Args: 读取配置文件并处理数据,循环遍历value_name,将value_name[i][0]中的数据替换为value_name[i][1]
        group_name: 组名称
        value_name: 项名称
        text: 需要格式化的文本
    Returns:
        处理后数据
    '''
    cf = configparser.ConfigParser()
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    config = configparser.ConfigParser()
    filePath = config.read(parent_dir + "\\replace.ini", encoding='utf-8')
    cf.read(filePath, encoding='utf-8')
    value = cf.get(group_name, value_name)
    cof_list = ast.literal_eval(value)
    for i in cof_list:
        this_text = text.replace(f'{i[0]}', f'{i[1]}').strip('\n').strip('\t')
        text = this_text
    return text


# 返回元素个数
def get_ele_number(ele):
    '''
    Args:
        ele: xpath元素
    Returns: int
    '''
    num = len(ele)
    return num


# 判断文件资源是否被占用
def is_open(filename):
    if not os.access(filename, os.F_OK):
        return False
    try:
        handle = w.CreateFile(filename, w.GENERIC_WRITE, 0, None, w.OPEN_EXISTING, w.FILE_ATTRIBUTE_NORMAL, None)
        if int(handle) == w.INVALID_HANDLE_VALUE:
            return True
        w.CloseHandle(handle)
    except Exception:
        return True
    return False


# 自动生成UA
# def get_random_ua():
#     ua = UserAgent(use_cache_server=False).random
#     return ua


# 获取当前时间
def get_curr_time():
    curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return curr_time
