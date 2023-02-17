import json
import re
import time
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from utils.constants import CFDI_SITE_PI_INFO_PATH, CFDI_SITE_CK_INFO_PATH, CFDI_SITE_INFO_PATH
from utils.encapsulation import write_csv


class CfdiSpider:
    def CFDI_Start(self):
        global content
        # 先获取数据长度
        cfdi_num_url = 'https://beian.cfdi.org.cn/**********************'
        num_resp = requests.get(cfdi_num_url).text
        cfdi_num_list = json.loads(num_resp)
        totalRows = int(cfdi_num_list['totalRows'])
        site_info_url = f'https://beian.cfdi.org.cn/*******************'
        print('------------------- | CFDI数据采集Start | -------------------')
        site_resp = requests.get(site_info_url).text
        cfdi_site_list = json.loads(site_resp)
        cfdi_site_list = cfdi_site_list['data']
        site_info_list = []
        for cfdi_site in tqdm(cfdi_site_list):
            companyid = cfdi_site['companyId']
            address = cfdi_site['address']
            areaname = cfdi_site['areaName']
            compname = cfdi_site['compName']
            compname = compname.strip()
            linkman = cfdi_site['linkMan']
            linktel = cfdi_site['linkTel']
            recordno = cfdi_site['recordNo']
            recordstatus = cfdi_site['recordStatus']
            cfdi_site_data = [companyid, address, areaname, compname, linkman, linktel, recordno, recordstatus]
            site_info_list.append(cfdi_site_data)

            site_pi_url = f"https://beian.cfdi.org.cn/*******************"

            resp = requests.get(site_pi_url, timeout=(3, 7)).text



            site_pi_list = self.get_cfdi_site_pi(resp, companyid)
            site_ck_list = self.get_cfdi_ck(resp, companyid)
            write_csv('pi.csv', site_pi_list)
            write_csv('ck.csv', site_ck_list)
        write_csv('site.csv', site_info_list)
        print('\n------------------- | CFDI数据采集End | -------------------')

    # 获取site_pi.csv函数
    def get_cfdi_site_pi(self, content, companyid):
        r = re.compile(r'<div class="tab-pane" id="tabContent2">([\s\S])*<div class="tab-pane" id="tabContent3">')
        pi_tableHtml = r.search(content).group()
        pi_soup = BeautifulSoup(pi_tableHtml, 'html.parser')
        site_pi_list = []
        for row in pi_soup.find_all('tr'):
            if len(row.findAll('td')) > 0:
                data_list = [companyid,
                             row.findAll('td')[1].get_text().replace(' ', '').replace('\xa0', ''),
                             row.findAll('td')[2].get_text().replace('\xa0', ''),
                             row.findAll('td')[0].get_text(),
                             row.findAll('td')[3].get_text()
                             ]
                site_pi_list.append(data_list)
        return site_pi_list

    # 获取cfdi_ck.csv函数
    def get_cfdi_ck(self, content, companyid):
        r = re.compile(r'<div class="tab-pane" id="tabContent3">([\s\S])*</table>')
        ck_tableHtml = r.search(content).group()
        ck_soup = BeautifulSoup(ck_tableHtml, 'html.parser')
        site_ck_list = []
        for row in ck_soup.find_all('tr'):
            if len(row.findAll('td')) > 0:
                data_list = [companyid,
                             row.findAll('td')[0].get_text(),
                             row.findAll('td')[1].get_text(),
                             row.findAll('td')[2].get_text(),
                             row.findAll('td')[3].get_text()
                             ]
                site_ck_list.append(data_list)
        return site_ck_list


if __name__ == '__main__':
    start = CfdiSpider()
    start.CFDI_Start()
