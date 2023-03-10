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

    # 1.??????,?????????????????????????????????
    def CDE_Start(self):
        resp = requests.post(self.get_number_url, headers=self.headers, timeout=(3, 7)).text
        html = etree.HTML(resp)
        page_count = int(html.xpath('//div[@class="pull-right pageInfo"]/i[2]')[0].text)
        data_count = int(html.xpath('//div[@class="pull-right pageInfo"]/i[3]')[0].text)
        # ??????????????????
        self.trun_page(page_count, data_count)

    # 2.????????????
    def trun_page(self, page_count, data_count):
        global html, resp
        print('------------------- | CDE   Start | -------------------')
        for page_number in tqdm(range(0, page_count)):
            '''
                # ???????????????????????????
                # range(
                        0 : ???????????????????????????,????????????????????????????????????????????????-1????????????,???????????????????????????
                        page_count : ?????????,????????????
                        )
            '''
            # ??????????????????????????????????????????
            first_number = page_number * 20 + 1
            last_number = first_number + 20
            # ????????????????????????
            for this_data_number in range(first_number, last_number):
                # ???????????????????????????????????????,????????????
                if this_data_number > data_count:
                    # ?????????????????????????????????????????????????????????????????????
                    print('------------------- | CDE   End | -------------------')
                    break
                data = {
                    # ?????????????????????????????????????????????????????????value?????????????????????
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
                # ?????????????????????0.5s?????????,????????????????????????10?????????????????????break
                for i in range(10):
                    try:
                        resp = requests.post(self.url, headers=self.headers,data=data, timeout=(3, 7))
                        '''
                            try
                                ????????????????????????????????????????????????????????????,??????????????????????????????
                            except 
                        '''
                        html = etree.HTML(resp.text)
                        break
                    except Exception as e:
                        print(f'?????????????????????,????????????????????????????????????????????????\t{e}')
                        time.sleep(0.5)
                # 1. ?????????????????????????????????????????????
                trial_all_info = self.get_trial_info(html)
                # 2. ???????????????????????????csv?????????
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

    # 3.??????trial_info.csv??????
    def get_trial_info(self, html):
        # ?????????
        global drug_text
        ctr_no_text = get_data_str('.//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[1]/td', html)
        # ????????????
        status_text = get_data_str('.//div[@id="collapseOne"]//table[@class="searchDetailTable"][1]//tr[1]/td[2]', html)
        # ???,????????????
        detail_status_text = get_data_str2('.//div[text()="1???????????????"]/following::text()[1]', html)
        # ??????????????????
        requestor_text = get_data_str('.//div[@id="collapseOne"]//table[@class="searchDetailTable"][1]/tr[2]/td[1]', html)
        # ???????????????
        try:
            sponsor_text = html.xpath('.//div[@id="collapseOne"]//table[@class="searchDetailTable"][1]/tr[3]/td[1]')[
                0].text.replace('								', ' ')
            sponsor_text = sponsor_text.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ').replace('   ', ' ').replace('         ', ' ').replace('   ', ' ')
            sponsor_text = sponsor_text.strip()
            # ???????????????????????????????????????????????????????????????replace
        except Exception as e:
            print(f'??????ctr_no???{ctr_no_text}??????CDE???????????????sponsor?????????sponsor?????????')
            sponsor_text = ''
        # ????????????????????????
        publication_date_text = get_data_str(
            './/div[@id="collapseOne"]//table[@class="searchDetailTable"][1]/tr[2]/td[2]', html)
        # ???????????????
        related_trial_no_text = get_data_str('.//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]/tr[2]/td', html)
        if related_trial_no_text == None:
            related_trial_no_text = ''
        # ????????????&?????????
        drug_text = html.xpath('//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[3]/td')[0].text
        if '????????????' in drug_text:
            drug_list=drug_text.split('????????????')
            drug_name_text = drug_list[0]
            drug_previous_name_text = drug_list[1].replace('???', '')
        elif '?????????' in drug_text:
            drug_name_text, drug_previous_name_text = drug_text.split('?????????:')
        elif drug_text=='':
            drug_name_text = ''
            drug_previous_name_text = ''
        else:
            drug_name_text=drug_text
            drug_previous_name_text=''

        # ????????????
        drug_type_text = get_data_str('//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[4]/td', html)
        # ?????????????????????
        clinical_register_no_text = get_data_str(
            '//*[@id="collapseTwo"]/div/table[1]//tr[5]/th[contains(text(),"?????????????????????")]/following::td[1]', html)
        # ?????????
        indication_text = get_data_str('//table[@class="searchDetailTable"][1]//tr[6]/td', html)
        # ????????????
        phase_text = get_data_str('//table[@class="searchDetailTable"][3]//tr[1]/td[2]', html)
        standard_phase = ''
        # ????????????
        category_text = get_data_str('//table[@class="searchDetailTable"][3]//tr[1]/td[1]', html)
        # ????????????
        try:
            scope_text = html.xpath('//table[@class="searchDetailTable"][3]//tr[2]/td[3]')[0].text. \
                replace('\r', '').replace('\n', '').replace('\t', '').replace('\"', '').replace(' ', '').replace('\xa0', '')
            standard_scope_text = scope_text
            if standard_scope_text not in ('????????????', '?????????????????????'):
                standard_scope_text = '??????'
        except:
            print(f'??????ctr_no???{ctr_no_text}??????CDE???????????????scope?????????scope?????????')
            standard_scope_text = ''
            scope_text = ''
        # ??????
        age_text = get_data_str('//*[@id="collapseTwo"]/div/table[4]//tr[1]/td', html)
        # ??????
        gender_text = get_data_str('//*[@id="collapseTwo"]/div/table[4]//tr[2]/td', html)
        # ??????????????????
        planned_size_text = get_data_str('.//div[text()="2???????????????"]/following::table[1]//tr[1]/td', html)
        # ???????????????
        actual_size_text = get_data_str('.//div[text()="2???????????????"]/following::table[1]//tr[2]/td', html)
        # ?????????????????????
        final_size_text = get_data_str('.//div[text()="2???????????????"]/following::table[1]//tr[3]/td', html)
        # ????????????
        try:
            inclusion_criteria_text = html.xpath('.//th[text()="????????????"]/following::table[1]//text()')
            inclusion_criteria_text = ''.join(str(i) for i in inclusion_criteria_text)
        except:
            print(f'??????ctr_no???{ctr_no_text}??????CDE???????????????inclusion_criteria?????????inclusion_criteria?????????')
            inclusion_criteria_text = ''
        # ????????????
        try:
            exclusion_criteria_text = html.xpath('.//th[text()="????????????"]/following::table[1]//text()')
            exclusion_criteria_text = ''.join(str(i) for i in exclusion_criteria_text)
        except:
            print(f'??????ctr_no???{ctr_no_text}??????CDE???????????????exclusion_criteria?????????exclusion_criteria?????????')
            exclusion_criteria_text = ''
        # ?????????????????????????????????????????????
        icf_date_text = get_data_str('.//div[text()="2???????????????"]/following::table[2]//tr[1]/td', html)
        # ??????????????????????????????
        fpi_Date_text = get_data_str('.//div[text()="2???????????????"]/following::table[2]//tr[2]/td', html)
        # ??????????????????
        close_date_text = get_data_str('.//div[text()="2???????????????"]/following::table[2]//tr[3]/td', html)
        # ????????????
        purpose_text = get_data_str2('.//div[text()="1???????????????"]/following::text()[1]', html)
        # ??????????????????
        official_name_text = get_data_str('//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[7]/td', html)
        official_name_text = conf_eval_data('trial_info', 'official_name', official_name_text)
        # ??????????????????
        common_name_text = get_data_str('//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[8]/td', html)
        common_name_text = conf_eval_data('trial_info', 'common_name', common_name_text)
        # ?????????
        try:
            test_drugs_text = html.xpath('//*[@id="collapseTwo"]/div/table[5]//tr[1]//table//text()')
            test_drugs_text = ''.join(str(i) for i in test_drugs_text)
            test_drugs_text = conf_eval_data('trial_info', 'test_drugs', test_drugs_text)
        except:
            print(f'??????ctr_no???{ctr_no_text}??????CDE???????????????test_drugs?????????test_drugs?????????')
            test_drugs_text = ''
        # ?????????
        try:
            control_drugs_text = html.xpath('//*[@id="collapseTwo"]/div/table[5]//tr[2]//table//text()')
            control_drugs_text = ''.join(str(i) for i in control_drugs_text)
            control_drugs_text = conf_eval_data('trial_info', 'control_drugs', control_drugs_text)
        except:
            print(f'??????ctr_no???{ctr_no_text}??????CDE???????????????control_drugs?????????control_drugs?????????')
            control_drugs_text = ''
        # ??????????????????
        scheme_no_text = get_data_str('//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[9]/td[1]', html)
        standard_scheme_no=''
        #   ?????????????????????
        scheme_version_text = ('.//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[9]/td[2]', html)
        #   ????????????
        version_date_text = get_data_str(
            './/div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[10]/td[1]', html)
        #   ???????????????????????????
        drug_combination_text = get_data_str(
            './/div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[10]/td[2]', html)
        #   ????????????
        design_type_text = get_data_str('//table[@class="searchDetailTable"][3]//tr[1]/td[3]', html)
        #   ?????????
        randomization_text = get_data_str('//table[@class="searchDetailTable"][3]//tr[2]/td[1]', html)
        #   ??????
        blinding_text = get_data_str('//table[@class="searchDetailTable"][3]//tr[2]/td[2]', html)
        #   ???????????????
        healthy_volunteer_text = get_data_str('//*[@id="collapseTwo"]/div/table[4]//tr[3]/td', html)
        #   ???????????????????????????(dmc)
        monitor_committee_text = get_data_str2('.//div[contains(text(), "???????????????????????????")]/following::text()[1]', html)
        #   ????????????????????????????????????
        injury_insurance_text = get_data_str2('.//div[contains(text(), "????????????????????????????????????")]/following::text()[1]', html)
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
        # ???????????????????????????,??????\r\n\t\&nbsp
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

    # 4.??????trial_pi.csv??????
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
            pi_name_text = re.sub('[,|???|;|???|???|(|???|/|-|&|:|???].*', '', pi_name_text)
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

    # 5.??????trial_site.csv??????
    def get_trial_site_info(self, html):
        global table_tr_num
        site_data = []
        for i in range(10):
            try:
                site_table = html.xpath('.//div[@class="sDPTit2" and text()="2????????????????????????"]/following::table[1]//tr')
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
                site_name_text = get_data_str(f'.//div[text()="2????????????????????????"]/following::table[1]//tr[{i}]/td[2]',
                                                  html).strip()
            except:
                site_name_text = get_data_str(f'.//div[text()="2????????????????????????"]/following::table[1]//tr[{i}]/td[2]',
                                              html)
            # 3.
            try:
                pi_name_text = html.xpath(f'.//div[text()="2????????????????????????"]/following::table[1]//tr[{i}]/td[3]')[0].text
                pi_name_text = str_sub(pi_name_text)
                pi_name_text = re.sub('[,|???|;|???|???|???|/|(|-|&|:|???].*', '', pi_name_text)
                pi_name_text = conf_eval_data('pi_name', 'pi_name', pi_name_text)
            except:
                pi_name_text = ''
            # 4.
            country_text = get_data_str(f'.//div[text()="2????????????????????????"]/following::table[1]//tr[{i}]/td[4]', html)
            # 5.
            province_state_text = get_data_str(f'.//div[text()="2????????????????????????"]/following::table[1]//tr[{i}]/td[5]', html)
            # 6.
            city_text = get_data_str(f'.//div[text()="2????????????????????????"]/following::table[1]//tr[{i}]/td[6]', html)
            # LIST
            trial_site_info_list = [ctr_no_text, site_name_text, pi_name_text, country_text, province_state_text,city_text]
            if trial_site_info_list[1] != '':
                site_data.append(trial_site_info_list)
            else:
                pass
        return site_data

    # 6.??????trial_ec.csv??????
    def get_trial_ec_info(self, html):
        global table_tr_num
        ec_data = []
        for i in range(4):
            try:
                ec_table = html.xpath(
                    './/div[text()="???????????????????????????"]/following::table[1]//tr')
                table_tr_num = get_ele_number(ec_table)
                break
            except:
                time.sleep(0.1)
        for i in range(2, table_tr_num + 1):
            # 1.
            ctr_no_text = get_data_str('.//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[1]/td',
                                       html)
            # 2.
            ec_name_text = get_data_str(f'.//div[text()="???????????????????????????"]/following::table[1]//tr[{i}]/td[2]', html)
            # 3.
            ec_conclusion_text = get_data_str(f'.//div[text()="???????????????????????????"]/following::table[1]//tr[{i}]/td[3]', html)
            ec_conclusion_text = conf_eval_data('trial_ec', 'ec_conclusion', ec_conclusion_text)
            # 4.
            ec_date_text = get_data_str(f'.//div[text()="???????????????????????????"]/following::table[1]//tr[{i}]/td[4]', html)
            # LIST
            trial_ec_info_list = [ctr_no_text, ec_name_text, ec_conclusion_text, ec_date_text]
            if trial_ec_info_list[1] != '':
                ec_data.append(trial_ec_info_list)
            else:
                pass
        return ec_data

    # 7.??????trial_endpoint.csv??????
    def get_trial_endpoint_info(self, html):
        global tr_num
        point_data = []
        # 2.
        primary_endpoint_text = '?????????????????????????????????'
        Secondary_endpoints_text = '?????????????????????????????????'
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

    # 8.??????trial_result.csv??????
    def get_trial_result_info(self, html):
        global tr_num, texts
        results = []
        for i in range(4):
            try:
                tr_ele = html.xpath('.//div[text()="??????????????????????????????"]/following::table[1]//tr')
                tr_num = get_ele_number(tr_ele)
                break
            except:
                time.sleep(0.1)
        for z in range(2, tr_num + 1):
            try:
                texts = html.xpath('.//div[text()="??????????????????????????????"]/following::table[1]//tr[2]/td')[0].text
            except:
                pass
            if '????????????' in texts:
                pass
            else:
                # 1.
                ctr_no_text = get_data_str('.//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[1]/td',
                                           html)
                # 2.
                vesion_no_text = get_data_str(f'.//div[text()="??????????????????????????????"]/following::table[1]//tr[{z}]/td[2]', html)
                # 3.
                version_date_text = get_data_str(f'.//div[text()="??????????????????????????????"]/following::table[1]//tr[{z}]/td[3]',
                                                 html)
                # LIST
                test_results_list = [ctr_no_text, vesion_no_text, version_date_text]
                if test_results_list[1] != '':
                    results.append(test_results_list)
                else:
                    pass
        return results
