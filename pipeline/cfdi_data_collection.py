import json
import requests
from lxml import etree
from tqdm import tqdm
from utils.constants import CFDI_SITE_PI_INFO_PATH, CFDI_SITE_CK_INFO_PATH, CFDI_SITE_INFO_PATH
from utils.encapsulation import write_csv, get_ele_number


class CfdiSpider:
    def CFDI_Start(self):
        # 先获取数据长度
        cfdi_num_url = 'aHR0cHM6Ly9iZWlhbi5jZmRpLm9yZy5jbi9DVE1EUy9wdWIvUFVCMDEwMTAwLmRvP21ldGhvZD1oYW5kbGUwNg=='
        num_resp = requests.get(cfdi_num_url).text
        cfdi_num_list = json.loads(num_resp)
        totalRows = int(cfdi_num_list['totalRows'])
        site_info_url = f'aHR0cHM6Ly9iZWlhbi5jZmRpLm9yZy5jbi9DVE1EUy9wdWIvUFVCMDEwMTAwLmRvP21ldGhvZD1oYW5kbGUwNiZwYWdlU2l6ZT17dG90YWxSb3dzICsgMX0mY3VyUGFnZT0x'
        print('------------------- | CFDI   Start | -------------------')
        site_resp = requests.get(site_info_url).text
        cfdi_site_list = json.loads(site_resp)
        cfdi_site_list = cfdi_site_list['data']


        print(f'site_info-before-:{cfdi_site_list[0]}')
        print(len(cfdi_site_list))


        site_info_list = []
        comcompanyid_list = []
        for cfdi_site in cfdi_site_list:
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
            comcompanyid_list.append(companyid)
        # 写入cfdi_site_info
        print(f'site_info-after-:{site_info_list[0]}')
        print(len(site_info_list))
        write_csv(CFDI_SITE_INFO_PATH, site_info_list)

        # 循环comcompanyid_list获取cfdi_site_pi/cfdi_site_ck数据
        for companyid in tqdm(comcompanyid_list):
            site_pi_url = f"aHR0cHM6Ly9iZWlhbi5jZmRpLm9yZy5jbi9DVE1EUy9wdWIvUFVCMDEwMTAwLmRvP21ldGhvZD1oYW5kbGUwNyZjb21wSWQ9e2NvbXBhbnlpZH0="
            html = self.get_pi_ck_result(companyid, site_pi_url)

            site_pi_list = self.get_cfdi_site_pi(html, companyid)
            write_csv(CFDI_SITE_PI_INFO_PATH, site_pi_list)

            site_ck_list = self.get_cfdi_ck(html, companyid)
            write_csv(CFDI_SITE_CK_INFO_PATH, site_ck_list)

    def get_pi_ck_result(self, companyid, site_pi_url):
        global html, resp
        for i in range(10):
            # 如果请求超时,重新获取响应
            try:
                resp = requests.get(site_pi_url, timeout=(3, 7))
                break
            except:
                pass

        if resp.status_code == 200:
            resp = resp.text
            html = etree.HTML(resp)
            # 请求异常,重新获取响应
            if html.xpath('//*[@id="mesg_dialog"]/div[2]/table/tbody/tr/td/span'):
                self.get_pi_ck_result(companyid, site_pi_url)
                # 未获取pi_list,重新获取响应
            elif len(html.xpath('//*[@id="tabContent2"]/div/table/tbody/tr')) < 1:
                self.get_pi_ck_result(companyid, site_pi_url)
        else:
            # 状态码非200,重新获取响应
            self.get_pi_ck_result(companyid, site_pi_url)
        return html

    # 获取site_pi.csv函数
    def get_cfdi_site_pi(self, html, companyid):
        global site_pi_list, tr_num_xpath
        try:
            tr_num_xpath = html.xpath('//*[@id="tabContent2"]/div/table/tbody/tr')
            tr_num = len(tr_num_xpath)
            if tr_num == 0:
                for k in range(20):
                    if tr_num != 0:
                        tr_num = get_ele_number(tr_num_xpath)
                        print(tr_num)
                        break
        except:
            tr_num = get_ele_number(tr_num_xpath)
        # print(f'{companyid}''----'f'{tr_num}')
        site_pi_all_list = []
        for i in range(1, tr_num + 1):
            pi_dep = html.xpath(f'//*[@id="tabContent2"]/div/table/tbody/tr[{i}]/td[1]')[0].text.replace(' ', '').replace('\xa0', '')
            pi_name = html.xpath(f'//*[@id="tabContent2"]/div/table/tbody/tr[{i}]/td[2]')[0].text.replace('\xa0', '')
            pi_title = html.xpath(f'//*[@id="tabContent2"]/div/table/tbody/tr[{i}]/td[3]')[0].text
            dep_add_date = html.xpath(f'//*[@id="tabContent2"]/div/table/tbody/tr[{i}]/td[4]')[0].text
            site_pi_list = [companyid, pi_name, pi_title, pi_dep, dep_add_date]
            site_pi_all_list.append(site_pi_list)
        return site_pi_all_list

    # 获取cfdi_ck.csv函数
    def get_cfdi_ck(self, html, companyid):
        global site_ck_list
        tr_num_xpath = html.xpath('//*[@id="tabContent3"]/div/table/tbody/tr')
        tr_num = get_ele_number(tr_num_xpath)
        site_ck_all_list = []
        for i in range(1, tr_num + 1):
            ck_date = html.xpath(f'//*[@id="tabContent3"]/div/table/tbody/tr[{i}]/td[1]')[0].text
            ck_type = html.xpath(f'//*[@id="tabContent3"]/div/table/tbody/tr[{i}]/td[2]')[0].text
            ck_result = html.xpath(f'//*[@id="tabContent3"]/div/table/tbody/tr[{i}]/td[3]')[0].text
            ck_disposal = html.xpath(f'//*[@id="tabContent3"]/div/table/tbody/tr[{i}]/td[4]')[0].text
            site_ck_list = [companyid, ck_date, ck_type, ck_result, ck_disposal]
            site_ck_all_list.append(site_ck_list)
        return site_ck_all_list
