import random
import re
import time
import requests
from tqdm import tqdm
from lxml import etree
from utils.constants import *
from utils.encapsulation import conf_eval_data, write_csv, get_ele_number, str_sub, get_data_str, get_data_str2


class CdeSpider:
    Cookie = [
        "FSSBBIl1UgzbN7N80S=AmMA4i6RzjkRrd_3ufeSlQfRQhRevsPbmE06ayvNafw1d0Z8uUyGLpxfJn_V2ebb;token=C1hCSkY2yWAEzQ7TZ_qacMPu3A2z8eMGLcs-6SJsZlQGCQDLBMsWGNErug8; FSSBBIl1UgzbN7N80T=3YvgnQKQu_pAA8qIKo67lwh.qa_y7_crUjNjnT5VR2YSpI8r_9cVgrlo3GsrB_vQQWum7udZevXQMVm5n0zROwyQS0tANP60Pm.ESLc9grs6896Muycmt3uZqbhlHOFiREOpyFFciGCYfrhbn_tGJIziPqNnZPjrsYpxvfYNLgLQDawn.2ZY0juLQEWTGzrzzNim.qsWACT4zmz_HBOnt8btdT1Ob5D1ANc47rKOMrvP4_GUjkYtRoI3JJXoio_Byg2MwcR_zzM8E4lFeoxrmtuSMWqwSq7PITW1NxpkOweZXlXOr6OJbtCQRjSMC2kmFkCEUKxNLKDPULG297tAkzC4UE9jf6QXOc.O6rHLZbQm04a",
        "FSSBBIl1UgzbN7N80S=abzlbXYBClZ2j..TaoFIqXsxsPIzPnkd2yQcQJYdoDBYmuiSwoJGkWnYEwigAXOn; token=pGI_8-nLlVwVkCDGm8QoWAPnyGFxNHHbL7pV9pfqUe0OKSrc30oBxd7xxax; FSSBBIl1UgzbN7N80T=3Sti.vBvSLuygqOS3mp6F1AzPQnkr0YmXhX6Babb6tgH2t4RQfAvFPAScNt2EN0Bd6BgbMBg7.D35J7WyogM2sOO_6F62dAz8DXpJFpWCJdWDg4mgUcOcH_FXr_uGycd8SoP_.ty4VUe7sf26pwF7.utRUSezAvEnxXAsBtFhzkQxSHPy63.8bcY4iMpC3u8glpeCwsH4vq7IPyu.7qRBbDo_i1vaCRKPQV0ErZxkDtsaWlWoQ6MNRauPRJD2TOTJJ9MmMGvcx_lyiZ.nm767HG7P9gqg8aD8n7ASxAuy24kj.4vT7Lno7i_9AVJHy29qU2Sq5PiU3KtFNc_LZcP6N_RoVWwvaxksSZpTM9ZtDV6OqA",
        "FSSBBIl1UgzbN7N80S=1bX0_verWSIOyNyNO5vSIpgCTPVf3PRYdw8o6ycPup8rTtKSA.1KuYOKuxTCigqR; token=IT2u7dD41DYHwTm53EhtZ0T6c31iPHtVZyiABYgfZO0kvA9HqFvAh9pzXa6; FSSBBIl1UgzbN7N80T=31N9bM._lbA5BPgCwNWWNjcv9XgvTc9Q53CM1Q0__TPONXEzzwfZo0gn_ZhLt1UNHARf9AeDcLONa.06Bzhjvw6EftO3hJpJd2NKjYe92SORbd8XvLkrtH7OykMCXLx2zK3DhCazTBapyxdPja7OsJdPrT25HOcrOztYVEz2W2aEo3C_.7W8SEFIccDrBtj7n2Vt2XLBtSAGsi9dl0V190lA145EK5bIc1KhvKYtoQ.ynZS5Yk7XHyn_fXpwst8aUmDQ8c2qEHPqae2oi_Jf3NEUq6OICfm2bmk.fqF2WawujDVcYGvT992wpHIb35wfuI0si.SnGBKza_jC.wkpES.Bf8Y3295aOYTAD6974cMmAUq",
        "FSSBBIl1UgzbN7N80S=cos_YFbTV4cZxJxZk_xCPhAvwLqSOi9EMXphoGp9RTd.zxyW3t5sKh2Ir9K3Mtiq; token=2k96tlH-pp51MB0M3b3_nZe5qr_AJ4wswnmperMsV90x4uCYdkJHVk4aapQ; FSSBBIl1UgzbN7N80T=3G9p.p_lRnyk0YAG.Yfkh9Vk2m33WJTsZQuc1cQib2PFNg4WnghqwpiLk4IZBl5vv9JQXHtbH7JB0KDfqk2dW6T75.6XO8OfdeE_1JVqxbRVqRZ3H0FI0DZgi_kjFPi6zZ2pj_HwRMkpZT2lVxHioPDBJuiTts7KCtwXGMP45kV2Knl2mfYy18dS4iK3Fmm9TeVlo3DXX8a5AtG3lt60SkCmVKO605rpcu.wvqIhaY1Bk.qF4VV01FOM4cy4PjHNWjqMr7izEisJeo_8qXA9gcdqry926Pt4FzqeXYa4XTIod5A"
    ]
    UserAgent = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    ]
    headers = {
        'User-agent': random.choice(UserAgent),
        'Cookie': random.choice(Cookie),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'www.chinadrugtrials.org.cn',
        'Origin': 'http://www.chinadrugtrials.org.cn',
        'Referer': 'http://www.chinadrugtrials.org.cn/clinicaltrials.searchlist.dhtml',
        'Upgrade-Insecure-Requests': '1'
    }
    url = 'http://www.chinadrugtrials.org.cn/clinicaltrials.searchlistdetail.dhtml'
    get_number_url = 'http://www.chinadrugtrials.org.cn/clinicaltrials.searchlist.dhtml'

    # 1.开始,先获取数据总数及总页数
    def CDE_Start(self):
        resp = requests.post(self.get_number_url, headers=self.headers, timeout=(3, 7)).text
        html = etree.HTML(resp)
        page_count = int(html.xpath('//div[@class="pull-right pageInfo"]/i[2]')[0].text)
        data_count = int(html.xpath('//div[@class="pull-right pageInfo"]/i[3]')[0].text)
        # 调取翻页函数
        self.trun_page(page_count, data_count)

    # 2.翻页函数
    def trun_page(self, page_count, data_count):
        global html, resp
        print('------------------- | CDE   Start | -------------------')
        for page_number in tqdm(range(0, page_count)):
            '''
                # 遍历获取到的总页数
                # range(
                        0 : 若程序中途手动停止,再次运行时需手动修改为停止的页数-1实现续爬,不需要考虑重复问题
                        page_count : 总页数,自动获取
                        )
            '''
            # 计算当前页码第一条数据的序号
            first_number = page_number * 20 + 1
            last_number = first_number + 20
            # 根据序号循环请求
            for this_data_number in range(first_number, last_number):
                # 到达最后一条数据时跳出循环,程序结束
                if this_data_number > data_count:
                    # 判断，如果数据取到最后一条则跳出，等待数据处理
                    print('------------------- | CDE   End | -------------------')
                    break
                data = {
                    # 请求参数，如果需要增加筛选条件则在对应value处写入条件即可
                    'id': '',
                    'ckm_index': this_data_number,
                    'sort': 'desc',
                    'sort2': '',
                    'rule': 'CTR',
                    'secondLevel': '1',
                    'currentpage': first_number,
                    'keywords': '',
                    'reg_no': '',
                    'indication': '',
                    'case_no': '',
                    'drugs_name': '',
                    'drugs_type': '',
                    'appliers': '',
                    'communities': '',
                    'researchers': '',
                    'agencies': '',
                    'state': ''
                        }
                # 请求报错时等待0.5s并重试,每个请求都会重试10次，请求成功时break
                for i in range(10):
                    try:
                        resp = requests.post(self.url, headers=self.headers,data=data, timeout=(3, 7))
                        '''
                            try
                                页面原始数据的位置没有数据时会报索引越界,出现此异常时数据置空
                            except 
                        '''
                        html = etree.HTML(resp.text)
                        break
                    except Exception as e:
                        print(f'请求时出现异常,重新进行此次请求，异常信息如下：\t{e}')
                        time.sleep(0.5)
                # 1. 调用获取数据的函数并将结果保存
                trial_all_info = self.get_trial_info(html)
                # 2. 将保存的结果写入到csv文件中
                write_csv(TRIAL_INFO_PATH, trial_all_info)

                pi_data = self.get_trial_pi_info(html)
                write_csv(TRIAL_PI_INFO_PATH, pi_data)

                site_data = self.get_trial_site_info(html)
                write_csv(TRIAL_SITE_INFO_PATH, site_data)

                ec_data = self.get_trial_ec_info(html)
                write_csv(TRIAL_EC_INFO_PATH, ec_data)

                point_data = self.get_trial_endpoint_info(html)
                write_csv(TRIAL_ENDPOINT_INFO_PATH, point_data)

                results = self.get_trial_result_info(html)
                write_csv(TRIAL_RESULT_PATH, results)

    # 3.获取trial_info.csv数据
    def get_trial_info(self, html):
        # 登记号
        global drug_text
        ctr_no_text = get_data_str('.//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[1]/td', html)
        # 试验状态
        status_text = get_data_str('.//div[@id="collapseOne"]//table[@class="searchDetailTable"][1]//tr[1]/td[2]', html)
        # 六,试验状态
        detail_status_text = get_data_str2('.//div[text()="1、试验状态"]/following::text()[1]', html)
        # 申请人联系人
        requestor_text = get_data_str('.//div[@id="collapseOne"]//table[@class="searchDetailTable"][1]/tr[2]/td[1]', html)
        # 申请人名称
        try:
            sponsor_text = html.xpath('.//div[@id="collapseOne"]//table[@class="searchDetailTable"][1]/tr[3]/td[1]')[
                0].text.replace('								', ' ')
            sponsor_text = sponsor_text.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ').replace('   ', ' ').replace('         ', ' ').replace('   ', ' ')
            sponsor_text = sponsor_text.strip()
            # 统一处理无法识别的冗余符号，单独处进行处理replace
        except Exception as e:
            print(f'当前ctr_no（{ctr_no_text}）在CDE系统中没有sponsor数据，sponsor置为空')
            sponsor_text = ''
        # 首次公示信息日期
        publication_date_text = get_data_str(
            './/div[@id="collapseOne"]//table[@class="searchDetailTable"][1]/tr[2]/td[2]', html)
        # 相关登记号
        related_trial_no_text = get_data_str('.//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]/tr[2]/td', html)
        if related_trial_no_text == None:
            related_trial_no_text = ''
        # 药物名称&曾用名
        drug_text = html.xpath('//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[3]/td')[0].text
        if '（曾用名' in drug_text:
            drug_list=drug_text.split('（曾用名')
            drug_name_text = drug_list[0]
            drug_previous_name_text = drug_list[1].replace('）', '')
        elif '曾用名' in drug_text:
            drug_name_text, drug_previous_name_text = drug_text.split('曾用名:')
        elif drug_text=='':
            drug_name_text = ''
            drug_previous_name_text = ''
        else:
            drug_name_text=drug_text
            drug_previous_name_text=''

        # 药物类型
        drug_type_text = get_data_str('//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[4]/td', html)
        # 临床申请受理号
        clinical_register_no_text = get_data_str(
            '//*[@id="collapseTwo"]/div/table[1]//tr[5]/th[contains(text(),"临床申请受理号")]/following::td[1]', html)
        # 适应症
        indication_text = get_data_str('//table[@class="searchDetailTable"][1]//tr[6]/td', html)
        # 试验分期
        phase_text = get_data_str('//table[@class="searchDetailTable"][3]//tr[1]/td[2]', html)
        standard_phase = ''
        # 试验分类
        category_text = get_data_str('//table[@class="searchDetailTable"][3]//tr[1]/td[1]', html)
        # 试验范围
        try:
            scope_text = html.xpath('//table[@class="searchDetailTable"][3]//tr[2]/td[3]')[0].text. \
                replace('\r', '').replace('\n', '').replace('\t', '').replace('\"', '').replace(' ', '').replace('\xa0', '')
            standard_scope_text = scope_text
            if standard_scope_text not in ('国内试验', '国际多中心试验'):
                standard_scope_text = '其他'
        except:
            print(f'当前ctr_no（{ctr_no_text}）在CDE系统中没有scope数据，scope置为空')
            standard_scope_text = ''
            scope_text = ''
        # 年龄
        age_text = get_data_str('//*[@id="collapseTwo"]/div/table[4]//tr[1]/td', html)
        # 性别
        gender_text = get_data_str('//*[@id="collapseTwo"]/div/table[4]//tr[2]/td', html)
        # 目标入组人数
        planned_size_text = get_data_str('.//div[text()="2、试验人数"]/following::table[1]//tr[1]/td', html)
        # 已入组人数
        actual_size_text = get_data_str('.//div[text()="2、试验人数"]/following::table[1]//tr[2]/td', html)
        # 实际入组总人数
        final_size_text = get_data_str('.//div[text()="2、试验人数"]/following::table[1]//tr[3]/td', html)
        # 入选标准
        try:
            inclusion_criteria_text = html.xpath('.//th[text()="入选标准"]/following::table[1]//text()')
            inclusion_criteria_text = ''.join(str(i) for i in inclusion_criteria_text)
        except:
            print(f'当前ctr_no（{ctr_no_text}）在CDE系统中没有inclusion_criteria数据，inclusion_criteria置为空')
            inclusion_criteria_text = ''
        # 排除标准
        try:
            exclusion_criteria_text = html.xpath('.//th[text()="排除标准"]/following::table[1]//text()')
            exclusion_criteria_text = ''.join(str(i) for i in exclusion_criteria_text)
        except:
            print(f'当前ctr_no（{ctr_no_text}）在CDE系统中没有exclusion_criteria数据，exclusion_criteria置为空')
            exclusion_criteria_text = ''
        # 第一例受试者签署知情同意书日期
        icf_date_text = get_data_str('.//div[text()="2、试验人数"]/following::table[2]//tr[1]/td', html)
        # 第一例受试者入组日期
        fpi_Date_text = get_data_str('.//div[text()="2、试验人数"]/following::table[2]//tr[2]/td', html)
        # 试验完成日期
        close_date_text = get_data_str('.//div[text()="2、试验人数"]/following::table[2]//tr[3]/td', html)
        # 试验目的
        purpose_text = get_data_str2('.//div[text()="1、试验目的"]/following::text()[1]', html)
        # 试验专业题目
        official_name_text = get_data_str('//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[7]/td', html)
        official_name_text = conf_eval_data('trial_info', 'official_name', official_name_text)
        # 试验通俗题目
        common_name_text = get_data_str('//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[8]/td', html)
        common_name_text = conf_eval_data('trial_info', 'common_name', common_name_text)
        # 试验药
        try:
            test_drugs_text = html.xpath('//*[@id="collapseTwo"]/div/table[5]//tr[1]//table//text()')
            test_drugs_text = ''.join(str(i) for i in test_drugs_text)
            test_drugs_text = conf_eval_data('trial_info', 'test_drugs', test_drugs_text)
        except:
            print(f'当前ctr_no（{ctr_no_text}）在CDE系统中没有test_drugs数据，test_drugs置为空')
            test_drugs_text = ''
        # 对照药
        try:
            control_drugs_text = html.xpath('//*[@id="collapseTwo"]/div/table[5]//tr[2]//table//text()')
            control_drugs_text = ''.join(str(i) for i in control_drugs_text)
            control_drugs_text = conf_eval_data('trial_info', 'control_drugs', control_drugs_text)
        except:
            print(f'当前ctr_no（{ctr_no_text}）在CDE系统中没有control_drugs数据，control_drugs置为空')
            control_drugs_text = ''
        # 试验方案编号
        scheme_no_text = get_data_str('//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[9]/td[1]', html)
        standard_scheme_no=''
        #   方案最新版本号
        scheme_version_text = ('.//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[9]/td[2]', html)
        #   版本日期
        version_date_text = get_data_str(
            './/div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[10]/td[1]', html)
        #   方案是否为联合用药
        drug_combination_text = get_data_str(
            './/div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[10]/td[2]', html)
        #   设计类型
        design_type_text = get_data_str('//table[@class="searchDetailTable"][3]//tr[1]/td[3]', html)
        #   随机化
        randomization_text = get_data_str('//table[@class="searchDetailTable"][3]//tr[2]/td[1]', html)
        #   盲法
        blinding_text = get_data_str('//table[@class="searchDetailTable"][3]//tr[2]/td[2]', html)
        #   健康受试者
        healthy_volunteer_text = get_data_str('//*[@id="collapseTwo"]/div/table[4]//tr[3]/td', html)
        #   数据安全监查委员会(dmc)
        monitor_committee_text = get_data_str2('.//div[contains(text(), "数据安全监查委员会")]/following::text()[1]', html)
        #   为受试者购买试验伤害保险
        injury_insurance_text = get_data_str2('.//div[contains(text(), "为受试者购买试验伤害保险")]/following::text()[1]', html)
        trial = [
            ctr_no_text, status_text, detail_status_text, requestor_text,
            publication_date_text, related_trial_no_text, drug_name_text, drug_previous_name_text,
            drug_type_text, clinical_register_no_text, indication_text, phase_text, standard_phase,
            category_text, scope_text, age_text, gender_text, planned_size_text, actual_size_text,
            final_size_text, inclusion_criteria_text, exclusion_criteria_text, icf_date_text, fpi_Date_text,
            close_date_text, purpose_text, official_name_text, common_name_text, test_drugs_text,
            control_drugs_text, scheme_no_text, standard_scheme_no, scheme_version_text, version_date_text, drug_combination_text,
            design_type_text, randomization_text, blinding_text, healthy_volunteer_text, monitor_committee_text,
            injury_insurance_text, standard_scope_text
                 ]
        # 对数据进行统一处理,删除\r\n\t\&nbsp
        trial_all_info = []
        trial_info = []
        for data_columns in trial:
            try:
                trial = data_columns.replace('\r', '').replace('\n', '').replace('\t', '').replace('\"', '').replace(' ', '').replace('\xa0', '')
            except:
                time.sleep(0.1)
            trial_info.append(trial)
        trial_all_info.append(trial_info)
        trial_all_info[0].insert(4, sponsor_text)
        return trial_all_info

    # 4.获取trial_pi.csv数据
    def get_trial_pi_info(self, html):
        global tab_num
        pi_data = []
        for i in range(10):
            try:
                table = html.xpath(
                    './/table//th[@style="text-align: center;" and @rowspan="3"]/parent::tr/parent::table')
                tab_num = get_ele_number(table)
            except Exception as e:
                time.sleep(0.1)
        for i in range(1, tab_num + 1):
            # 1.
            ctr_no_text = get_data_str('.//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[1]/td',
                                       html)
            # 2.
            pi_name_text = get_data_str(
                f'.//table//th[@style="text-align: center;" and @rowspan="3" and text()="{i}"]/parent::tr/parent::table//tr[1]/td[1]',
                html)
            pi_name_text = str_sub(pi_name_text)
            pi_name_text = re.sub('[,|，|;|；|（|(|、|/|-|&|:|：].*', '', pi_name_text)
            pi_name_text = conf_eval_data('pi_name', 'pi_name', pi_name_text)
            # 3.
            pi_title_text = get_data_str(
                f'.//table//th[@style="text-align: center;" and @rowspan="3" and text()="{i}"]/parent::tr/parent::table//tr[1]/td[3]',
                html)
            # 4.
            pi_phone_text = get_data_str(
                f'.//table//th[@style="text-align: center;" and @rowspan="3" and text()="{i}"]/parent::tr/parent::table//tr[2]/td[1]',
                html)
            # 5.
            pi_mail_text = get_data_str(
                f'.//table//th[@style="text-align: center;" and @rowspan="3" and text()="{i}"]/parent::tr/parent::table//tr[2]/td[2]',
                html)
            # 6.
            pi_postcode_text = get_data_str(
                f'.//table//th[@style="text-align: center;" and @rowspan="3" and text()="{i}"]/parent::tr/parent::table//tr[3]/td[1]',
                html)
            # 7.
            try:
                pi_site_name_text = get_data_str(
                    f'.//table//th[@style="text-align: center;" and @rowspan="3" and text()="{i}"]/parent::tr/parent::table//tr[3]/td[2]',
                    html).strip()
            except:
                pi_site_name_text = get_data_str(
                    f'.//table//th[@style="text-align: center;" and @rowspan="3" and text()="{i}"]/parent::tr/parent::table//tr[3]/td[2]',
                    html)
            # LIST
            pi_info_list = [ctr_no_text, pi_name_text, pi_title_text, pi_phone_text, pi_mail_text, pi_postcode_text,pi_site_name_text]
            if pi_info_list[1] != '':
                pi_data.append(pi_info_list)
            else:
                pass
        return pi_data

    # 5.获取trial_site.csv数据
    def get_trial_site_info(self, html):
        global table_tr_num
        site_data = []
        for i in range(10):
            try:
                site_table = html.xpath('.//div[@class="sDPTit2" and text()="2、各参加机构信息"]/following::table[1]//tr')
                table_tr_num = get_ele_number(site_table)
                break
            except:
                time.sleep(0.1)
        for i in range(2, table_tr_num + 1):
            # 1.
            ctr_no_text = get_data_str('.//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[1]/td',
                                       html)
            # 2.
            try:
                site_name_text = get_data_str(f'.//div[text()="2、各参加机构信息"]/following::table[1]//tr[{i}]/td[2]',
                                                  html).strip()
            except:
                site_name_text = get_data_str(f'.//div[text()="2、各参加机构信息"]/following::table[1]//tr[{i}]/td[2]',
                                              html)
            # 3.
            try:
                pi_name_text = html.xpath(f'.//div[text()="2、各参加机构信息"]/following::table[1]//tr[{i}]/td[3]')[0].text
                pi_name_text = str_sub(pi_name_text)
                pi_name_text = re.sub('[,|，|;|（|；|、|/|(|-|&|:|：].*', '', pi_name_text)
                pi_name_text = conf_eval_data('pi_name', 'pi_name', pi_name_text)
            except:
                pi_name_text = ''
            # 4.
            country_text = get_data_str(f'.//div[text()="2、各参加机构信息"]/following::table[1]//tr[{i}]/td[4]', html)
            # 5.
            province_state_text = get_data_str(f'.//div[text()="2、各参加机构信息"]/following::table[1]//tr[{i}]/td[5]', html)
            # 6.
            city_text = get_data_str(f'.//div[text()="2、各参加机构信息"]/following::table[1]//tr[{i}]/td[6]', html)
            # LIST
            trial_site_info_list = [ctr_no_text, site_name_text, pi_name_text, country_text, province_state_text,city_text]
            if trial_site_info_list[1] != '':
                site_data.append(trial_site_info_list)
            else:
                pass
        return site_data

    # 6.获取trial_ec.csv数据
    def get_trial_ec_info(self, html):
        global table_tr_num
        ec_data = []
        for i in range(4):
            try:
                ec_table = html.xpath(
                    './/div[text()="五、伦理委员会信息"]/following::table[1]//tr')
                table_tr_num = get_ele_number(ec_table)
                break
            except:
                time.sleep(0.1)
        for i in range(2, table_tr_num + 1):
            # 1.
            ctr_no_text = get_data_str('.//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[1]/td',
                                       html)
            # 2.
            ec_name_text = get_data_str(f'.//div[text()="五、伦理委员会信息"]/following::table[1]//tr[{i}]/td[2]', html)
            # 3.
            ec_conclusion_text = get_data_str(f'.//div[text()="五、伦理委员会信息"]/following::table[1]//tr[{i}]/td[3]', html)
            ec_conclusion_text = conf_eval_data('trial_ec', 'ec_conclusion', ec_conclusion_text)
            # 4.
            ec_date_text = get_data_str(f'.//div[text()="五、伦理委员会信息"]/following::table[1]//tr[{i}]/td[4]', html)
            # LIST
            trial_ec_info_list = [ctr_no_text, ec_name_text, ec_conclusion_text, ec_date_text]
            if trial_ec_info_list[1] != '':
                ec_data.append(trial_ec_info_list)
            else:
                pass
        return ec_data

    # 7.获取trial_endpoint.csv数据
    def get_trial_endpoint_info(self, html):
        global tr_num
        point_data = []
        # 2.
        primary_endpoint_text = '主要终点指标及评价时间'
        Secondary_endpoints_text = '次要终点指标及评价时间'
        for j in range(1, 3):
            if j == 1:
                type = primary_endpoint_text
            else:
                type = Secondary_endpoints_text
            for i in range(4):
                try:
                    tr_ele = html.xpath(f'//*[@id="collapseTwo"]/div/table[6]/tr[{j}]//table//tr')
                    tr_num = get_ele_number(tr_ele)
                    break
                except:
                    time.sleep(0.1)
            for i in range(2, tr_num + 1):
                # 1.
                ctr_no_text = get_data_str('.//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[1]/td',
                                           html)
                # 3.
                content_text = get_data_str(f'//*[@id="collapseTwo"]/div/table[6]/tr[{j}]/td/table/tr[{i}]/td[2]', html)
                # 4.
                evaluation_time_text = get_data_str(
                    f'//*[@id="collapseTwo"]/div/table[6]/tr[{j}]/td/table/tr[{i}]/td[3]', html)
                # 5.
                selection_text = get_data_str(f'//*[@id="collapseTwo"]/div/table[6]/tr[{j}]/td/table/tr[{i}]/td[4]',
                                              html)
                selection_text = conf_eval_data('trial_endpoint', 'selection', selection_text)
                # LIST
                primary_info_list = [ctr_no_text, type, content_text, evaluation_time_text, selection_text]
                if primary_info_list[1] != '':
                    point_data.append(primary_info_list)
                else:
                    pass
        return point_data

    # 8.获取trial_result.csv数据
    def get_trial_result_info(self, html):
        global tr_num, texts
        results = []
        for i in range(4):
            try:
                tr_ele = html.xpath('.//div[text()="七、临床试验结果摘要"]/following::table[1]//tr')
                tr_num = get_ele_number(tr_ele)
                break
            except:
                time.sleep(0.1)
        for z in range(2, tr_num + 1):
            try:
                texts = html.xpath('.//div[text()="七、临床试验结果摘要"]/following::table[1]//tr[2]/td')[0].text
            except:
                pass
            if '暂未填写' in texts:
                pass
            else:
                # 1.
                ctr_no_text = get_data_str('.//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[1]/td',
                                           html)
                # 2.
                vesion_no_text = get_data_str(f'.//div[text()="七、临床试验结果摘要"]/following::table[1]//tr[{z}]/td[2]', html)
                # 3.
                version_date_text = get_data_str(f'.//div[text()="七、临床试验结果摘要"]/following::table[1]//tr[{z}]/td[3]',
                                                 html)
                # LIST
                test_results_list = [ctr_no_text, vesion_no_text, version_date_text]
                if test_results_list[1] != '':
                    results.append(test_results_list)
                else:
                    pass
        return results
