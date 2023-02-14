"""
This is script is to curation sponsors for project trialviz

Input:
    Curated trial list that has CTR_No, Sponsors and Phase

Returns:
    The Sponsor Type of each trial: Industry, Academy, Collaboration
    The curated sponsors
"""
import ast
import time

import pandas as pd
import os
import re
from utils import constants
from utils.constants import TRIAL_INFO_PATH


class Sponsor_Curation:
    """
    This Class is used to curate sponsors.

    Steps:
        step 1 - Split the sponsor str by '/'
        step 2 - Identify the sponsor type
            "Industry", only contains "公司"
            "Academy", only contains "大学"，"研究院"， "研究所"
            "Collaboration", contains both in each CTR
        step 3 - Transform the sponsor str to short names using mapping list
        step 4 - Remove the duplicates in each CTR
        step 5 - remove province and city name in company name
        step 6 - remove (.*) in company name
        step 7 - remove the duplicates in each CTR and generate sponsor_std
        step 8 - remove the cro sponsors and generate sponsor_std_remove_cro

    Returns:
        The Sponsor Type of each trial: Industry, Academy, Collaboration
        The standardized sponsors
    """

    def __init__(self, trial_list):

        # # Load the data
        # sponsor_mapping_list_path = './data_input/CDE/sponsor_std/sponsor_mapping_list.csv'
        # special_sponsor_list_path = './data_input/CDE/sponsor_std/special_sponsor_list.xlsx'
        # cro_list_path = './data_input/CDE/sponsor_std/cro_list.xlsx'
        # province_list_path = './data_input/CDE/sponsor_std/province.xlsx'
        # city_list_path = './data_input/CDE/sponsor_std/city.xlsx'

        trial_list['sponsor'] = trial_list['sponsor'].fillna('')
        self.input_sponsors = trial_list
        self.sponsor_mapping_list = pd.read_csv(constants.SPONSOR_MAPPING_LIST_PATH)
        self.special_sponsor_list = pd.read_excel(constants.SPECIAL_SPONSOR_LIST_PATH)
        self.cro_list = pd.read_excel(constants.CRO_LIST_PATH)
        self.province_list = pd.read_excel(constants.PROVINCE_LIST_PATH)
        self.city_list = pd.read_excel(constants.CITY_LIST_PATH)

    @staticmethod
    def _deep_to_splited_list(splited_list, fun):
        """
        this function is used to apply function to each element in nest list
        :param splited_list:
        :param fun:
        :return nested_list:
        """
        list_item = []
        for item in splited_list:
            list_sponsor = []
            for sponsor in item:
                sponsor_short = fun(sponsor)
                list_sponsor = list_sponsor + [sponsor_short]
            list_item = list_item + [list_sponsor]

        return list_item

    @staticmethod
    def _sponsor_type_identifier(sponsor_str_list, academy_keywords=None):
        """
        此函数用于识别SPONSER类型
        :param sponsor_str_list:
        :param academy_keywords:
        :return sponsor type:
        """
        if academy_keywords is None:
            academy_keywords = ['大学', '研究院', '研究所']

        def is_academy(sponsor_str):
            is_academy = [keyword in sponsor_str for keyword in academy_keywords]
            is_industry = '公司' in sponsor_str
            is_academy = any(is_academy) and not is_industry
            return is_academy

        are_academies = [is_academy(sponsor_str) for sponsor_str in sponsor_str_list]
        are_academies = list(set(are_academies))

        if len(are_academies) == 2:
            sponsor_type = 'Collaboration'
        elif len(are_academies) == 1 and are_academies[0]:
            sponsor_type = 'Academic'
        else:
            sponsor_type = 'Industry'
        return sponsor_type

    def _sponsor_mapping(self, sponsor_str):
        """
        此函数用于将sponsor str 转换为短名称
        using mapping list
        :param sponsor_str:
        :return short sponsor name:
        """
        sponsor_str_l = sponsor_str.lower()
        sponsor_mapping_list = self.sponsor_mapping_list
        mapping_item = (sponsor_mapping_list.loc[sponsor_mapping_list.Col1.apply(lambda x: x.lower() in sponsor_str_l)])

        if mapping_item.shape[0] == 0:
            mapping_item = (
                sponsor_mapping_list.loc[sponsor_mapping_list.Col2.apply(lambda x: x.lower() in sponsor_str_l)])
        if mapping_item.shape[0] == 0:
            return sponsor_str
        else:
            return mapping_item.iloc[0, 1]

    def _remove_pro_city(self, sponsor_name):
        """
        此功能用于去除公司名称中的省市名称
        :param sponsor_name:
        :return standardized company name:
        """
        province_list = [i.strip() for i in self.province_list.province]
        city_list = [i.strip() for i in self.city_list.city]

        if '公司' not in sponsor_name or any([i in sponsor_name for i in self.special_sponsor_list.iloc[:, 0]]):
            return sponsor_name
        else:
            # remove province + sheng
            province_list_sheng = [i + '省' for i in province_list]
            sheng_in_sponsor = [i for i in province_list_sheng if i in sponsor_name]
            for i in sheng_in_sponsor:
                sponsor_name = sponsor_name.replace(i, '')

            # remove province
            pro_in_sponsor = [i for i in province_list if i in sponsor_name]
            for i in pro_in_sponsor:
                sponsor_name = sponsor_name.replace(i, '')

            # remove city + shi
            city_list_shi = [i + '市' for i in city_list]
            shi_in_sponsor = [i for i in city_list_shi if i in sponsor_name]
            for i in shi_in_sponsor:
                sponsor_name = sponsor_name.replace(i, '')

            # remove city
            city_in_sponsor = [i for i in city_list if i in sponsor_name]
            for i in city_in_sponsor:
                sponsor_name = sponsor_name.replace(i, '')

            return sponsor_name.strip()

    @staticmethod
    def _remove_brackets(sponsor_name):
        """
        此功能用于删除公司名称中的括号
        :param sponsor_name:
        :return standardized company name:
        """
        sponsor_name_std = re.sub('（.*）|\(.*\)', '', sponsor_name)
        return sponsor_name_std

    def _is_cro(self, sponsor_name):
        """
        此功能用于删除公司名称中的括号
        :param sponsor_name:
        :return if the sponsor is CRO:
        """
        is_cro = any([i in sponsor_name for i in self.cro_list.iloc[:, 0]])
        if is_cro:
            result = 'cro_sponsor'
        else:
            result = sponsor_name
        return result

    # remove "is_cro" from the list
    @staticmethod
    def remove_cro_sponsor(l):
        temp_array = []
        for sponsor in l:
            if sponsor == 'cro_sponsor' or sponsor in '不适用':
                continue
            temp_array.append(sponsor.strip())
        return temp_array

    # def _count_top_sponsors(self, phase):
    #     """
    #     this function is used to count the top sponsors
    #     :param phase:Trial phase
    #     :return top sponsors:
    #     """
    #     if phase == 'all':
    #         sponsor_df = self.input_sponsors
    #     else:
    #         sponsor_df = self.input_sponsors[self.input_sponsors.Phase == phase]
    #
    #     phase_n_trial_sponsors = sponsor_df.Sponsor_Std.tolist()
    #     all_sponsors = [sponsor
    #                     for item in phase_n_trial_sponsors
    #                     for sponsor in item]
    #
    #     sponsor_count_df = pd.DataFrame(
    #             np.transpose(
    #                     np.unique(all_sponsors, return_counts=True)),
    #             columns=[f'Sponsor_Phase {phase}', 'Count'])
    #
    #     sponsor_count_df['Count'] = sponsor_count_df.Count.apply(int)
    #     sponsor_count_df = sponsor_count_df.sort_values(['Count'],
    #                                                     ascending=False)
    #     return sponsor_count_df

    def curate_sponsors(self):
        """
        This function is to curate the sponsors
        :return:
        """
        # Step 1 : 切割sponsor str by '/'
        sponsor_split2 = []
        sponsor_split = [sponsor.split(r'/ ') for sponsor in self.input_sponsors.sponsor]
        # Step 2 : 确定 sponsor type
        sponsor_type = [self._sponsor_type_identifier(sponsor_str_list) for sponsor_str_list in sponsor_split]

        self.input_sponsors['sponsor_type'] = sponsor_type

        # Step 3 : 使用映射列表将sponsor str 转换为短名称
        sponsor_list_short = self._deep_to_splited_list(sponsor_split, fun=self._sponsor_mapping)

        # Step 4 : 删除每个 CTR 中的重复项
        sponsor_list_short_no_dup = [list(set(item)) for item in sponsor_list_short]

        # Step 5 : 去除公司名称中的省市名称
        sponsor_list_short_no_pro_city = self._deep_to_splited_list(sponsor_list_short_no_dup,
                                                                    fun=self._remove_pro_city)

        # Step 6 : 删除公司名称中的括号
        sponsor_list_short_no_brackets = self._deep_to_splited_list(sponsor_list_short_no_pro_city,
                                                                    fun=self._remove_brackets)
        # Step 7 : 再次删除每个 CTR 中的重复项
        sponsor_list_short_no_dup2 = [list(set(item)) for item in sponsor_list_short_no_brackets]

        self.input_sponsors['sponsor_std'] = sponsor_list_short_no_dup2

        # Step 8 : Remove CRO
        check_cro = self._deep_to_splited_list(self.input_sponsors.sponsor_std.tolist(), fun=self._is_cro)
        list_removed_cro = [self.remove_cro_sponsor(item) for item in check_cro]


        self.input_sponsors['sponsor_std_removed_cro'] = list_removed_cro

        # # step 8 : 计算所有试验和每个阶段的顶级sponsors
        # phases = ['III', 'II', 'I', 'I/II', 'II/III']
        # top_sponsors = [self._count_top_sponsors('all')]

        # for phase in phases:
        #     top_sponsors = top_sponsors + [self._count_top_sponsors(phase)]
        #
        # self.top_sponsors = top_sponsors
        #
        # # step 9 : Count sponsor type in each phase
        # sponsor_type_count = self.input_sponsors.\
        #     groupby(['Sponsor_Type', 'Phase'])['CTR_No'].count().reset_index()
        #
        # self.sponsor_type_count = sponsor_type_count

        print('------------------- Sponsor 格式化')


# 插入Sponser...三列
def format_sponser():
    time.sleep(2)
    pd.options.mode.chained_assignment = None   # 消除警告,不影响数据的处理
    trial_info = pd.read_csv(TRIAL_INFO_PATH)
    curator = Sponsor_Curation(trial_info)
    curator.curate_sponsors()
    trial_info_data = curator.input_sponsors
    for i in range(0, len(trial_info_data['sponsor_std'])):
        trial_info_data['sponsor_std'][i] = ','.join(trial_info_data['sponsor_std'][i])
    for i in range(0, len(trial_info_data['sponsor_std_removed_cro'])):
        trial_info_data['sponsor_std_removed_cro'][i] = '|'.join(trial_info_data['sponsor_std_removed_cro'][i])
    trial_info_data.to_csv(TRIAL_INFO_PATH, index=False)