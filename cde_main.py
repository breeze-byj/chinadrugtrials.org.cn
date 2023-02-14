import datetime
from pipeline.cde_data_collection import CdeSpider
from pipeline.cfdi_data_collection import CfdiSpider
from pipeline.phase_std import standard_phase
from pipeline.sponsor_std import format_sponser
from pipeline.scheme_no_std import standard_janssen_scheme_no
from utils.encapsulation import zip_ya
from utils.insert_tit import write_all_tit, deduplication_all_csv
from threading import Thread


def run_cde():
    # 1.Cde运行
    CdeSpider().CDE_Start()
    # 2.去重
    deduplication_all_csv()
    # 3.写入title
    write_all_tit()
    # 4.sponser格式化
    format_sponser()
    # 5.phase格式化
    standard_phase()
    # 6.scheme_no格式化
    standard_janssen_scheme_no()
    # 7.打包到根目录
    zip_ya('./data_input/CDE/cde_export',
           f'./trial_viz_data{str(datetime.date.today().year) + "-" + str(datetime.date.today().month) + "-" + str(datetime.date.today().day)}.zip')


def run_cfdi():
    # 1.Cfdi运行
    CfdiSpider().CFDI_Start()


def thread_start():
    # 将cde/cfdi存入线程组
    threads_list = []
    threads_list.append(Thread(target=run_cde))
    threads_list.append(Thread(target=run_cfdi))
    for thread in threads_list:
        thread.start()


# 运行...
if __name__ == '__main__':
    '''
        根据需求,程序执行前是否对上一批次的csv文件进行删除
        delete_all_csv()
    '''
    thread_start()
