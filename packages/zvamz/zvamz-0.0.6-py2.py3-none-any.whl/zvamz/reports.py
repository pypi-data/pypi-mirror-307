import pandas as pd
import numpy as np
from datetime import datetime


def bgdeldup(dateName:str, minDate: datetime, client: str, bgTable:str):
    """
    Delete the data from the declared minDate to avoid duplicate in the database

    Parameters:
    - dateName: the name of the date column
    - minDate: the start date that will be deleted to avoid duplicate
    - client: the BigQuery client name
    - bgTable: the BigQuery Table address

    Returns:
    - delete the data to avoid duplicate
    """
    delDataQuery = f"""
    DELETE FROM
    `{bgTable}`
    WHERE
    {dateName} >= '{minDate}'
    """

    delData = client.query(delDataQuery)
    delData = delData.result()

    return delData

def bgdeldupf(dateName:str, minDate: datetime, client: str, bgTable:str):
    """
    Delete the data from the declared minDate to avoid duplicate in the database
    (free version of BigQuery)

    Parameters:
    - dateName: the name of the date column
    - minDate: the start date that will be deleted to avoid duplicate
    - client: the BigQuery client name
    - bgTable: the BigQuery Table address

    Returns:
    - delete the data to avoid duplicate
    """
    delDataQuery = f"""
    CREATE OR REPLACE TABLE `{bgTable}` AS

    SELECT *
    FROM `{bgTable}`
    WHERE
    {dateName} < '{minDate}'
    """

    delData = client.query(delDataQuery)
    delData = delData.result()

    return delData

def dfbgcolcheck(df: pd.DataFrame, client: str, bgTable: str):
    """
    This function compares the columns of DataFrame and existing BigQuery Table

    Paremeters:
    - df: Data frame to check
    - client: name of BigQuery client
    - bgTable: the address of BigQuery Table

    Returns:
    - True if it matches
    - ValueError if not
    """
    existingDataQuery = f"""
    SELECT
    *
    FROM
    `{bgTable}`
    LIMIT 10
    """

    existingData = client.query(existingDataQuery).to_dataframe()

    columnsCheck = existingData.columns.equals(df.columns)
    if columnsCheck:
        print("Column names and positions are the same.")
        return True
    else:
        raise ValueError("Error: Column names and positions are not the same.")

def lowfeereport(filePath:str):
    """
    This function process and clean the Amazon Economics Report.
    It extracts the low level inventory data

    Paremeters:
    - filePath: the path where the report is saved

    Returns:
    - DataFrame of the cleaned report
    - Flase if there is no data related to low level inventory fee
    """
    lowFeeDf = pd.read_csv(filePath)

    checkCol = [
        'Low-inventory-level fee per unit',
        'Low-inventory-level fee quantity',
        'Low-inventory-level fee total'
    ]

    colCheck = all(col in lowFeeDf.columns for col in checkCol)

    if colCheck:
        lowFeeDf = lowFeeDf[[
            'Start date',
            'End date',
            'ASIN',
            'MSKU',
            'Low-inventory-level fee per unit',
            'Low-inventory-level fee quantity',
            'Low-inventory-level fee total'
        ]]

        lowFeeDf = lowFeeDf.rename(columns=lambda x:x.replace('-','_').replace(' ','_').lower())
        lowFeeDf['start_date'] = pd.to_datetime(lowFeeDf['start_date'])
        lowFeeDf['end_date'] = pd.to_datetime(lowFeeDf['end_date'])

        schema = {
                'start_date': 'datetime64[ns]',
                'end_date': 'datetime64[ns]',
                'asin': str,
                'msku': str,
                'low_inventory_level_fee_per_unit': float,
                'low_inventory_level_fee_quantity': float,
                'low_inventory_level_fee_total': float
        }

        lowFeeDf = lowFeeDf.astype(schema)
        return lowFeeDf
    else:
        return False
    
def promoreport(filePath:str):
    """
    Clean the raw file downloaded in Amazon Seller Central Promotions Report

    Parameter:
    - filePath: the path where the downloaded Promotions Report is located

    Return:
    - DataFrame of the cleaned report
    """
    promoDf = pd.read_csv(filePath)
    promoDf = promoDf.rename(columns=lambda x:x.replace('?','').replace('"','').replace('-','_').lower())
    promoDf['shipment_date'] = pd.to_datetime(promoDf['shipment_date'], utc=True)

    schema = {
        'shipment_date': 'datetime64[ns, UTC]',
        'currency': str,
        'item_promotion_discount': float,
        'item_promotion_id': str,
        'description': str,
        'promotion_rule_value': str,
        'amazon_order_id': str,
        'shipment_id': str,
        'shipment_item_id': str
    }
    promoDf = promoDf.astype(schema)

    return promoDf

def spstreport(filePath:str):
    spSearchTermDf = pd.read_excel(filePath)
    spSearchTermDf = spSearchTermDf.rename(columns=lambda X:X.replace('7','_7').replace('-','').replace('#','').replace('(','').replace(')','').replace(' ','_').lower())

    schema = {
        'date': 'datetime64[ns]',
        'portfolio_name': str,
        'currency': str,
        'campaign_name': str,
        'ad_group_name': str,
        'targeting': str,
        'match_type': str,
        'customer_search_term': str,
        'impressions': float,
        'clicks': float,
        'clickthru_rate_ctr': float,
        'cost_per_click_cpc': float,
        'spend': float,
        '_7_day_total_sales_': float,
        'total_advertising_cost_of_sales_acos_': float,
        'total_return_on_advertising_spend_roas': float,
        '_7_day_total_orders_': float,
        '_7_day_total_units_': float,
        '_7_day_conversion_rate': float,
        '_7_day_advertised_sku_units_': float,
        '_7_day_other_sku_units_': float,
        '_7_day_advertised_sku_sales_': float,
        '_7_day_other_sku_sales_': float
    }

    spSearchTermDf = spSearchTermDf.astype(schema)

    return spSearchTermDf

def sbstreport(filePath:str):
    sbSearchTermDf = pd.read_excel(filePath)
    sbSearchTermDf = sbSearchTermDf.rename(columns=lambda X:X.replace('14','_14').replace('-','').replace('#','').replace('(','').replace(')','').replace(',','').replace(' ','_').lower())

    schema = {
        'date': 'datetime64[ns]',
        'portfolio_name': str,
        'currency': str,
        'campaign_name': str,
        'ad_group_name': str,
        'targeting': str,
        'match_type': str,
        'customer_search_term': str,
        'cost_type': str,
        'impressions': float,
        'viewable_impressions': float,
        'clicks': float,
        'clickthru_rate_ctr': float,
        'spend': float,
        'cost_per_click_cpc': float,
        'cost_per_1000_viewable_impressions_vcpm': float,
        'total_advertising_cost_of_sales_acos_': float,
        'total_return_on_advertising_spend_roas': float,
        '_14_day_total_sales_': float,
        '_14_day_total_orders_': float,
        '_14_day_total_units_': float,
        '_14_day_conversion_rate': float,
        'total_advertising_cost_of_sales_acos__click': float,
        'total_return_on_advertising_spend_roas__click': float,
        '_14_day_total_sales__click': float,
        '_14_day_total_orders___click': float,
        '_14_day_total_units___click': float
    }

    sbSearchTermDf = sbSearchTermDf.astype(schema)

    return sbSearchTermDf

def sdtreport(filePath:str):
    sdTargetingDf = pd.read_excel(filePath)
    sdTargetingDf = sdTargetingDf.rename(columns=lambda X:X.replace('14','_14').replace('-','').replace('#','').replace('(','').replace(')','').replace(',','').replace(' ','_').lower())

    schema = {
        'date': 'datetime64[ns]',
        'currency': str,
        'campaign_name': str,
        'portfolio_name': str,
        'cost_type': str,
        'ad_group_name': str,
        'targeting': str,
        'bid_optimization': str,
        'impressions': float,
        'viewable_impressions': float,
        'clicks': float,
        'clickthru_rate_ctr': float,
        '_14_day_detail_page_views_dpv': float,
        'spend': float,
        'cost_per_click_cpc': float,
        'cost_per_1000_viewable_impressions_vcpm': float,
        'total_advertising_cost_of_sales_acos_': float,
        'total_return_on_advertising_spend_roas': float,
        '_14_day_total_orders_': float,
        '_14_day_total_units_': float,
        '_14_day_total_sales_': float,
        '_14_day_newtobrand_orders_': float,
        '_14_day_newtobrand_sales': float,
        '_14_day_newtobrand_units_': float,
        'total_advertising_cost_of_sales_acos__click': float,
        'total_return_on_advertising_spend_roas__click': float,
        '_14_day_total_orders___click': float,
        '_14_day_total_units___click': float,
        '_14_day_total_sales__click': float,
        '_14_day_newtobrand_orders___click': float,
        '_14_day_newtobrand_sales__click': float,
        '_14_day_newtobrand_units___click': float
    }

    sdTargetingDf = sdTargetingDf.astype(schema)

    return sdTargetingDf

def spcreport(filePath:str):
    spCampaignDf = pd.read_csv(filePath)
    spCampaignDf = spCampaignDf.rename(columns=lambda X:X.replace('7','_7').replace('-','').replace('#','').replace('(','').replace(')','').replace(',','').replace(' ','_').lower())

    colRange = spCampaignDf.columns[7:]
    spCampaignDf[colRange] = spCampaignDf[colRange].replace({'%':'','\$':'',',':''}, regex=True)
    spCampaignDf['date'] = pd.to_datetime(spCampaignDf['date'])

    schema = {
        'date': 'datetime64[ns]',
        'portfolio_name': str,
        'campaign_type': str,
        'campaign_name': str,
        'country': str,
        'status': str,
        'currency': str,
        'budget': float,
        'targeting_type': str,
        'bidding_strategy': str,
        'impressions': float,
        'last_year_impressions': float,
        'clicks': float,
        'last_year_clicks': float,
        'clickthru_rate_ctr': float,
        'spend': float,
        'last_year_spend': float,
        'cost_per_click_cpc': float,
        'last_year_cost_per_click_cpc': float,
        '_7_day_total_orders_': float,
        'total_advertising_cost_of_sales_acos_': float,
        'total_return_on_advertising_spend_roas': float,
        '_7_day_total_sales_': float
    }

    spCampaignDf = spCampaignDf.astype(schema)

    return spCampaignDf

def sbcreport(filePath:str):
    sbCampaignDf = pd.read_excel(filePath)
    sbCampaignDf = sbCampaignDf.rename(columns=lambda X:X.replace('14','_14').replace('5','_5').replace('-','').replace('#','').replace('(','').replace(')','').replace(',','').replace(' ','_').lower())

    colRange = sbCampaignDf.columns[6:]
    sbCampaignDf[colRange] = sbCampaignDf[colRange].replace({'%':'','\$':'',',':''}, regex=True)
    sbCampaignDf['date'] = pd.to_datetime(sbCampaignDf['date'])

    schema = {
        'date': 'datetime64[ns]',
        'portfolio_name': str,
        'currency': str,
        'campaign_name': str,
        'cost_type': str,
        'country': str,
        'impressions': float,
        'clicks': float,
        'clickthru_rate_ctr': float,
        'cost_per_click_cpc': float,
        'spend': float,
        'total_advertising_cost_of_sales_acos_': float,
        'total_return_on_advertising_spend_roas': float,
        '_14_day_total_sales_': float,
        '_14_day_total_orders_': float,
        '_14_day_total_units_': float,
        '_14_day_conversion_rate': float,
        'viewable_impressions': float,
        'cost_per_1000_viewable_impressions_vcpm': float,
        'viewthrough_rate_vtr': float,
        'clickthrough_rate_for_views_vctr': float,
        'video_first_quartile_views': float,
        'video_midpoint_views': float,
        'video_third_quartile_views': float,
        'video_complete_views': float,
        'video_unmutes': float,
        '_5_second_views': float,
        '_5_second_view_rate': float,
        '_14_day_branded_searches': float,
        '_14_day_detail_page_views_dpv': float,
        '_14_day_newtobrand_orders_': float,
        '_14_day_%_of_orders_newtobrand': float,
        '_14_day_newtobrand_sales': float,
        '_14_day_%_of_sales_newtobrand': float,
        '_14_day_newtobrand_units_': float,
        '_14_day_%_of_units_newtobrand': float,
        '_14_day_newtobrand_order_rate': float,
        'total_advertising_cost_of_sales_acos__click': float,
        'total_return_on_advertising_spend_roas__click': float,
        '_14_day_total_sales__click': float,
        '_14_day_total_orders___click': float,
        '_14_day_total_units___click': float,
        'newtobrand_detail_page_views': float,
        'newtobrand_detail_page_view_clickthrough_conversions': float,
        'newtobrand_detail_page_view_rate': float,
        'effective_cost_per_newtobrand_detail_page_view': float,
        '_14_day_atc': float,
        '_14_day_atc_clicks': float,
        '_14_day_atcr': float,
        'effective_cost_per_add_to_cart_ecpatc': float,
        'branded_searches_clickthrough_conversions': float,
        'branded_searches_rate': float,
        'effective_cost_per_branded_search': float
    }

    sbCampaignDf = sbCampaignDf.astype(schema)
    
    return sbCampaignDf

def sdcreport(filePath:str):
    sdCampaignDf = pd.read_excel(filePath)
    sdCampaignDf = sdCampaignDf.rename(columns=lambda X:X.replace('14','_14').replace('-','').replace('#','').replace('(','').replace(')','').replace(',','').replace(' ','_').lower())

    colRange = sdCampaignDf.columns[4:]
    sdCampaignDf[colRange] = sdCampaignDf[colRange].replace({'%':'','\$':'',',':''}, regex=True)
    sdCampaignDf['date'] = pd.to_datetime(sdCampaignDf['date'])

    schema = {
        'date': 'datetime64[ns]',
        'country': str,
        'status': str,
        'currency': str,
        'budget': float,
        'campaign_name': str,
        'portfolio_name': str,
        'cost_type': str,
        'impressions': float,
        'viewable_impressions': float,
        'clicks': float,
        'clickthru_rate_ctr': float,
        '_14_day_detail_page_views_dpv': float,
        'spend': float,
        'cost_per_click_cpc': float,
        'cost_per_1000_viewable_impressions_vcpm': float,
        'total_advertising_cost_of_sales_acos_': float,
        'total_return_on_advertising_spend_roas': float,
        '_14_day_total_orders_': float,
        '_14_day_total_units_': float,
        '_14_day_total_sales_': float,
        '_14_day_newtobrand_orders_': float,
        '_14_day_newtobrand_sales': float,
        '_14_day_newtobrand_units_': float,
        'total_advertising_cost_of_sales_acos__click': float,
        'total_return_on_advertising_spend_roas__click': float,
        '_14_day_total_orders___click': float,
        '_14_day_total_units___click': float,
        '_14_day_total_sales__click': float,
        '_14_day_newtobrand_orders___click': float,
        '_14_day_newtobrand_sales__click': float,
        '_14_day_newtobrand_units___click': float,
        'newtobrand_detail_page_views': float,
        'newtobrand_detail_page_view_viewthrough_conversions': float,
        'newtobrand_detail_page_view_clickthrough_conversions': float,
        'newtobrand_detail_page_view_rate': float,
        'effective_cost_per_newtobrand_detail_page_view': float,
        '_14_day_atc': float,
        '_14_day_atc_views': float,
        '_14_day_atc_clicks': float,
        '_14_day_atcr': float,
        'effective_cost_per_add_to_cart_ecpatc': float,
        '_14_day_branded_searches': float,
        'branded_searches_viewthrough_conversions': float,
        'branded_searches_clickthrough_conversions': float,
        'branded_searches_rate': float,
        'effective_cost_per_branded_search': float
    }

    sdCampaignDf = sdCampaignDf.astype(schema)

    return sdCampaignDf

def unifiedRepo(filePath:str):
    unifiedDf = pd.read_csv(filePath, skiprows=7)
    unifiedDf = unifiedDf.rename(columns=lambda x:x.replace(' ','_').replace('-','_').replace('(','').replace(')','').replace('/','_'))

    unifiedDf['quantity'] = unifiedDf['quantity'].replace({np.nan:0},regex=True)
    colmChange = unifiedDf.columns[14:]
    unifiedDf[colmChange] = unifiedDf[colmChange].replace({',':''},regex=True)

    unifiedDf['date_time'] = pd.to_datetime(unifiedDf['date_time'].replace({' PDT':'', ' PST':''}, regex=True))
    unifiedDf['date_time'] = unifiedDf['date_time'].dt.tz_localize('America/Los_Angeles', ambiguous=True)

    req_columns = [
        'date_time',
        'settlement_id',
        'type',
        'order_id',
        'sku',
        'description',
        'quantity',
        'marketplace',
        'account_type',
        'fulfillment',
        'order_city',
        'order_state',
        'order_postal',
        'tax_collection_model',
        'product_sales',
        'product_sales_tax',
        'shipping_credits',
        'shipping_credits_tax',
        'gift_wrap_credits',
        'giftwrap_credits_tax',
        'Regulatory_Fee',
        'Tax_On_Regulatory_Fee',
        'promotional_rebates',
        'promotional_rebates_tax',
        'marketplace_withheld_tax',
        'selling_fees',
        'fba_fees',
        'other_transaction_fees',
        'other',
        'total'    
    ]

    for col in req_columns:
        if col not in unifiedDf.columns:
            unifiedDf[col] = np.nan

    unifiedDf = unifiedDf[req_columns]

    schema = {
        'date_time': 'datetime64[ns, America/Los_Angeles]',
        'settlement_id': str,
        'type': str,
        'order_id': str,
        'sku': str,
        'description': str,
        'quantity': int,
        'marketplace': str,
        'account_type': str,
        'fulfillment': str,
        'order_city': str,
        'order_state': str,
        'order_postal': str,
        'tax_collection_model': str,
        'product_sales': float,
        'product_sales_tax': float,
        'shipping_credits': float,
        'shipping_credits_tax': float,
        'gift_wrap_credits': float,
        'giftwrap_credits_tax': float,
        'Regulatory_Fee': float,
        'Tax_On_Regulatory_Fee': float,
        'promotional_rebates': float,
        'promotional_rebates_tax': float,
        'marketplace_withheld_tax': float,
        'selling_fees': float,
        'fba_fees': float,
        'other_transaction_fees': float,
        'other': float,
        'total': float
    }

    unifiedDf = unifiedDf.astype(schema)

    return unifiedDf

