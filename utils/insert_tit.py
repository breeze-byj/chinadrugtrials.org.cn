import os
import time
from utils.constants import TRIAL_INFO_PATH, TRIAL_PI_INFO_PATH, TRIAL_SITE_INFO_PATH, TRIAL_EC_INFO_PATH, TRIAL_ENDPOINT_INFO_PATH, TRIAL_RESULT_PATH, CFDI_SITE_PI_INFO_PATH, CFDI_SITE_CK_INFO_PATH, CFDI_SITE_INFO_PATH
from utils.encapsulation import wri_tit, csv_deduplication

cfdi_site_pi_title = ['companyId', 'pi_name', 'pi_title', 'pi_dep', 'dep_add_date']

cfdi_site_ck_title = ['companyId', 'ck_date', 'ck_type', 'ck_result', 'ck_disposal']

cfdi_site_info_title = ['companyId', 'address', 'areaName', 'compName', 'linkMan', 'linkTel', 'recordNo', 'recordStatus']

trial_ec_title = ['ctr_no', 'ec_name', 'ec_conclusion', 'ec_date']

trial_site_title = ['ctr_no', 'site_name', 'pi_name', 'country', 'province_state', 'city']

trial_pi_title = ['ctr_no', 'pi_name', 'pi_title', 'pi_phone', 'pi_mail', 'pi_postcode', 'pi_site_name']

trial_info_title = ['ctr_no', 'status', 'detail_status', 'requestor', 'sponsor','publication_date', 'related_trial_no', 'drug_name', 'drug_previous_name',
                    'drug_type', 'clinical_register_no', 'indication', 'phase', 'standard_phase','category', 'scope', 'age', 'gender', 'planned_size', 'actual_size',
                    'final_size', 'inclusion_criteria', 'exclusion_criteria', 'icf_date','fpi_Date', 'close_date', 'purpose', 'official_name', 'common_name',
                    'test_drugs', 'control_drugs', 'scheme_no','standard_scheme_no', 'scheme_version', 'version_date','drug_combination', 'design_type', 'randomization',
                    'blinding', 'healthy_volunteer','monitor_committee', 'injury_insurance', 'standard_scope']

trial_endpoint_title = ['ctr_no', 'type', 'content', 'evaluation_time', 'selection']

trial_result_title = ['ctr_no', 'version_no', 'version_date']


def write_all_tit():
    time.sleep(5)
    print('------------------- 写入表头')
    wri_tit(TRIAL_INFO_PATH, trial_info_title)
    wri_tit(TRIAL_PI_INFO_PATH, trial_pi_title)
    wri_tit(TRIAL_SITE_INFO_PATH, trial_site_title)
    wri_tit(TRIAL_EC_INFO_PATH, trial_ec_title)
    wri_tit(TRIAL_ENDPOINT_INFO_PATH, trial_endpoint_title)
    wri_tit(TRIAL_RESULT_PATH, trial_result_title)
    wri_tit(CFDI_SITE_PI_INFO_PATH, cfdi_site_pi_title)
    wri_tit(CFDI_SITE_CK_INFO_PATH, cfdi_site_ck_title)
    wri_tit(CFDI_SITE_INFO_PATH, cfdi_site_info_title)


# 对cde_export下所有文件并去重
def deduplication_all_csv():
    time.sleep(5)
    print('------------------- 去重')
    files = os.listdir('data_input/CDE/cde_export')
    for filename in files:
        csv_deduplication(f'./data_input/CDE/cde_export/{filename}')
        print(f'./data_input/CDE/cde_export/{filename}')