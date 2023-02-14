import operator
import re
import time
import pandas as pd
from utils.constants import TRIAL_INFO_PATH
from utils.encapsulation import conf_eval_data


def format_phase(standard_phase_text):
    standard_phase_text = conf_eval_data('trial_info', 'standard_phase', standard_phase_text)
    if standard_phase_text.find("其它其他说明:") >= 0:
        temp_standard_phase = standard_phase_text \
            .replace("IV", "Four").replace("III", "Three").replace("II", "Two").replace("I", "One") \
            .replace("1", "One").replace("2", "Two").replace("3", "Three").replace("4", "IV")
        if re.match(".*One.*Two", temp_standard_phase):
            standard_phase_text = "I/II"
        elif re.match(".*Two.*Three", temp_standard_phase):
            standard_phase_text = "II/III"
        elif re.match(".*One", temp_standard_phase):
            standard_phase_text = "I"
        elif re.match(".*Two", temp_standard_phase):
            standard_phase_text = "II"
        elif re.match(".*Three", temp_standard_phase):
            standard_phase_text = "III"
        elif re.match(".*Four", temp_standard_phase):
            standard_phase_text = "IV"
    standard_phase_text = re.sub(re.compile(r"^其它其他说明:.+", re.S), "Other", standard_phase_text)
    # 调用conf_eval_data函数,读取配置文件并处理数据
    standard_phase_text = conf_eval_data('trial_info', 'phase', standard_phase_text)
    # 根据处理数据后的结果,如果结果不存在于eval_list则置为Other
    eval_list = ['I', 'II', 'III', 'IV', 'I/II', 'II/III']
    if (operator.contains(eval_list, standard_phase_text)):
        pass
    else:
        standard_phase_text = 'Other'
    return standard_phase_text


def standard_phase():
    time.sleep(5)
    pd.options.mode.chained_assignment = None   # 消除警告,不影响数据的处理
    phase_info = pd.read_csv(TRIAL_INFO_PATH,encoding='utf-8')
    for i in range(0, len(phase_info['phase'])):
        try:
            phase_info['phase'][i] = ''.join(str(phase_info['phase'][i]))
            phase_info['standard_phase'][i] = format_phase(phase_info['phase'][i])
        except TypeError as e:
            pass
    phase_info.to_csv(TRIAL_INFO_PATH, index=False)

    print('------------------- Phase 格式化')
