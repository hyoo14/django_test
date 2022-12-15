

from django import forms
from django.contrib.auth.forms import UserCreationForm
from charts.models import Chart


class RegisterForm(UserCreationForm):
    #raw_id = forms.CharField(required=False)#, max_length=30)
    CHART_CD = forms.CharField(required=False)
    CHART_TPCD = forms.CharField(required=False)
    COL_ITEM_TXT_EMPH_TLTIP_VL = forms.CharField(required=False)#, max_length=30)
    COL_AXISX_TTL_GNRL_VL = forms.CharField(required=False)#, max_length=30)
    COL_AXISX_TTL_EMPH_VL = forms.CharField(required=False)#, max_length=30)
    ITEM_SET_USYN = forms.CharField(required=False)#, max_length=30)
    ITEM_SET_MIN_VL = forms.FloatField(required=False)#, max_length=30)
    ITEM_SET_MAX_VL = forms.FloatField(required=False)#, max_length=30)
    AXISY_USYN = forms.CharField(required=False)#, max_length=30)
    AXISY_CNT_MIN_VL = forms.FloatField(required=False)#, max_length=30)
    AXISY_CNT_MAX_VL = forms.FloatField(required=False)#, max_length=30)
    AXISY_TTL_NMB_MIN_VL = forms.FloatField(required=False)#, max_length=30)
    AXISY_TTL_NMB_MAX_VL = forms.FloatField(required=False)#, max_length=30)
    AXISY_TTL_LET_CNT_MAX_VL = forms.FloatField(required=False)#, max_length=30)
    COL_AXISY_TTL_VL = forms.CharField(required=False)#, max_length=30)
    COL_AXISY_LINE_VL = forms.CharField(required=False)#, max_length=30)
    LEGD_USYN = forms.CharField(required=False)#, max_length=30)
    LEGD_NMB_MIN_VL = forms.FloatField(required=False)#, max_length=30)
    LEGD_NMB_MAX_VL = forms.FloatField(required=False)#, max_length=30)
    LEGD_TXT_LET_CNT_MAX_VL = forms.FloatField(required=False)#, max_length=30)
    COL_ITEM_EMPH_LEGD1_VL = forms.CharField(required=False)#, max_length=30)
    COL_ITEM_EMPH_LEGD2_VL = forms.CharField(required=False)#, max_length=30)
    COL_ITEM_EMPH_LEGD3_VL = forms.CharField(required=False)#, max_length=30)
    COL_ITEM_EMPH_LEGD4_VL = forms.CharField(required=False)#, max_length=30)
    COL_ITEM_EMPH_LEGD5_VL = forms.CharField(required=False)#, max_length=30)
    THRHLD_USYN = forms.CharField(required=False)#, max_length=30)
    THRHLD_RFLN_NMB_MIN_VL = forms.FloatField(required=False)#, max_length=30)
    THRHLD_RFLN_NMB_MAX_VL = forms.FloatField(required=False)#, max_length=30)
    THRHLD_TXT_LET_CNT_MAX_VL = forms.FloatField(required=False)#, max_length=30)
    COL_THRHLD_RFLN_VL = forms.CharField(required=False)#, max_length=30)
    COL_THRHLD_TXT_VL = forms.CharField(required=False)#, max_length=30)
    ASST_TXT_USYN = forms.CharField(required=False)#, max_length=30)
    ASST_TXT_NMB_MIN_VL = forms.FloatField(required=False)#, max_length=30)
    ASST_TXT_NMB_MAX_VL = forms.FloatField(required=False)#, max_length=30)
    ASST_TXT_LET_CNT = forms.FloatField(required=False)#, max_length=30)
    COL_ASST_TXT_VL = forms.CharField(required=False)#, max_length=30)
    MSG_USYN = forms.CharField(required=False)#, max_length=30)
    MSG_ROW_CNT_MAX_VL = forms.FloatField(required=False)#, max_length=30)
    MSG_ROW_CNT_MIN_VL = forms.FloatField(required=False)#, max_length=30)
    MSG_ROW_LET_CNT_MAX_VL = forms.FloatField(required=False)#, max_length=30)
    MSG_EMPH_CNT = forms.FloatField(required=False)#, max_length=30)
    MSG_CNT = forms.FloatField(required=False)#, max_length=30)
    MSG_IMPN_INDX_CNT = forms.FloatField(required=False)#, max_length=30)
    MSG_ASST_INDX_CNT = forms.FloatField(required=False)#, max_length=30)
    MSG_IMPN_INDX_LET_CNT_MAX_VL = forms.FloatField(required=False)#, max_length=30)
    MSG_ASST_INDX_TTL_LET_CNT_MAX_VL = forms.FloatField(required=False)#, max_length=30)
    MSG_ASST_INDX_LET_CNT_MAX_VL = forms.FloatField(required=False)#, max_length=30)
    MSG_STUS_ICON_CNT = forms.FloatField(required=False)#, max_length=30)
    MSG_BTN_CNT = forms.FloatField(required=False)#, max_length=30)
    COL_MSG_GNRL_VL = forms.CharField(required=False)#, max_length=30)
    COL_MSG_EMPH_VL = forms.CharField(required=False)#, max_length=30)
    COL_IMPN_INDX_VL = forms.CharField(required=False)#, max_length=30)
    COL_ASST_INDX_TTL_VL = forms.CharField(required=False)#, max_length=30)
    COL_ASST_INDX_VL = forms.CharField(required=False)#, max_length=30)
    ITEM_PART_ALL_USYN = forms.CharField(required=False)#, max_length=30)
    ITEM_TXT_NMB_PART_VL = forms.FloatField(required=False)#, max_length=30)
    ITEM_TXT_NMB_ALL_VL = forms.FloatField(required=False)#, max_length=30)
    COL_ITEM_GNRL_PART_VL = forms.CharField(required=False)#, max_length=30)
    COL_ITEM_GNRL_ALL_VL = forms.CharField(required=False)#, max_length=30)
    COL_ITEM_EMPH_PART_VL = forms.CharField(required=False)#, max_length=30)
    COL_ITEM_EMPH_ALL_VL = forms.CharField(required=False)#, max_length=30)
    COL_ITEM_TXT_EMPH_PART_VL = forms.CharField(required=False)#, max_length=30)
    COL_ITEM_TXT_EMPH_ALL_VL = forms.CharField(required=False)#, max_length=30)
    TBL_YN = forms.CharField(required=False)#, max_length=30)
    COL_TBL_TXT_VL = forms.CharField(required=False)#, max_length=30)
    COL_TBL_DSNC_LINE_VL = forms.CharField(required=False)#, max_length=30)
    COL_TBL_TTL_VL = forms.CharField(required=False)#, max_length=30)
    COL_TBL_TTL_BGD_VL = forms.CharField(required=False)#, max_length=30)
    USYN = forms.CharField(required=False)#, max_length=30)
    RGPR_ID = forms.CharField(required=False)#, max_length=30)
    RGDA = forms.CharField(required=False)#, max_length=30)
    MDPR_ID = forms.CharField(required=False)#, max_length=30)
    LAST_MDFC_DTTM = forms.CharField(required=False)#, max_length=30)

    class Meta:
        model = Chart
        fields = (
            "CHART_CD",
        "CHART_TPCD",
            "COL_ITEM_TXT_EMPH_TLTIP_VL",
"COL_AXISX_TTL_GNRL_VL",
"COL_AXISX_TTL_EMPH_VL",
"ITEM_SET_USYN",
"ITEM_SET_MIN_VL",
"ITEM_SET_MAX_VL",
"AXISY_USYN",
"AXISY_CNT_MIN_VL",
"AXISY_CNT_MAX_VL",
"AXISY_TTL_NMB_MIN_VL",
"AXISY_TTL_NMB_MAX_VL",
"AXISY_TTL_LET_CNT_MAX_VL",
"COL_AXISY_TTL_VL",
"COL_AXISY_LINE_VL",
"LEGD_USYN",
"LEGD_NMB_MIN_VL",
"LEGD_NMB_MAX_VL",
"LEGD_TXT_LET_CNT_MAX_VL",
"COL_ITEM_EMPH_LEGD1_VL",
"COL_ITEM_EMPH_LEGD2_VL",
"COL_ITEM_EMPH_LEGD3_VL",
"COL_ITEM_EMPH_LEGD4_VL",
"COL_ITEM_EMPH_LEGD5_VL",
"THRHLD_USYN",
"THRHLD_RFLN_NMB_MIN_VL",
"THRHLD_RFLN_NMB_MAX_VL",
"THRHLD_TXT_LET_CNT_MAX_VL",
"COL_THRHLD_RFLN_VL",
"COL_THRHLD_TXT_VL",
"ASST_TXT_USYN",
"ASST_TXT_NMB_MIN_VL",
"ASST_TXT_NMB_MAX_VL",
"ASST_TXT_LET_CNT",
"COL_ASST_TXT_VL",
"MSG_USYN",
"MSG_ROW_CNT_MAX_VL",
"MSG_ROW_CNT_MIN_VL",
"MSG_ROW_LET_CNT_MAX_VL",
"MSG_EMPH_CNT",
"MSG_CNT",
"MSG_IMPN_INDX_CNT",
"MSG_ASST_INDX_CNT",
"MSG_IMPN_INDX_LET_CNT_MAX_VL",
"MSG_ASST_INDX_TTL_LET_CNT_MAX_VL",
"MSG_ASST_INDX_LET_CNT_MAX_VL",
"MSG_STUS_ICON_CNT",
"MSG_BTN_CNT",
"COL_MSG_GNRL_VL",
"COL_MSG_EMPH_VL",
"COL_IMPN_INDX_VL",
"COL_ASST_INDX_TTL_VL",
"COL_ASST_INDX_VL",
"ITEM_PART_ALL_USYN",
"ITEM_TXT_NMB_PART_VL",
"ITEM_TXT_NMB_ALL_VL",
"COL_ITEM_GNRL_PART_VL",
"COL_ITEM_GNRL_ALL_VL",
"COL_ITEM_EMPH_PART_VL",
"COL_ITEM_EMPH_ALL_VL",
"COL_ITEM_TXT_EMPH_PART_VL",
"COL_ITEM_TXT_EMPH_ALL_VL",
"TBL_YN",
"COL_TBL_TXT_VL",
"COL_TBL_DSNC_LINE_VL",
"COL_TBL_TTL_VL",
"COL_TBL_TTL_BGD_VL",
"USYN",
"RGPR_ID",
"RGDA",
"MDPR_ID",
"LAST_MDFC_DTTM",
        )