import pandas as pd
from django.shortcuts import render, redirect

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response

from charts.forms import RegisterForm
from .serializers import ChartSerializer
from .models import Chart
from google.cloud import bigquery

#에러로그 추가
import logging
logger = logging.getLogger('my')

class ChartViewSet(viewsets.ModelViewSet):#기본 crud로직 그룹화한 viewset 사용
    queryset = Chart.objects.all() #그대로 쓰면 안 되는 상황(검증 추가)에 동작시키는 방안
    serializer_class = ChartSerializer
    #차트 타입에 따라서 필수인 필드와 아닌 필드 임의로 지정
    def validation_logic(self, serializer):

        # data = request.data
        # serializer = ChartSerializer(data=data)

        # chart_cd, chart_tpcd = request.POST.get('CHART_CD'), request.POST.get('CHART_TPCD')
        chart_cd, chart_tpcd = serializer.initial_data['CHART_CD'], serializer.initial_data['CHART_TPCD']
        # char_COL_ITEM_TXT_EMPH_TLTIP_VL = request.POST.get('COL_ITEM_TXT_EMPH_TLTIP_VL')
        chart_COL_ITEM_TXT_EMPH_TLTIP_VL = serializer.initial_data['COL_ITEM_TXT_EMPH_TLTIP_VL']

        # chart_cd와 chart_tpcd는 모두 있어야
        # if chart_cd is not None and chart_tpcd is not None:
        # 이 케이스 제외 제낌
        print("work")
        logger.info("validation logic works")  # 특정 로그를 파일로 출력
        if not serializer.is_valid():
            return "error"  # HttpResponseRedirect('admin/')

        if chart_cd is None or chart_tpcd is None:
            return "error"  # HttpResponseRedirect('admin/')

        if str(chart_tpcd) + "_" not in str(chart_cd):
            return "error"  # HttpResponseRedirect('admin/')

        if str(chart_tpcd) == "LINE" and len(chart_COL_ITEM_TXT_EMPH_TLTIP_VL) == 0:
            return "error"  # HttpResponseRedirect('admin/')

        print(chart_cd, '  ', chart_tpcd, '   ', len(chart_COL_ITEM_TXT_EMPH_TLTIP_VL))
        return "no error"

    def create(self, request):
        data = request.data
        serializer = ChartSerializer(data=data)
        isValid = self.validation_logic(serializer)
        print(isValid)
        if isValid == "error":
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # if serializer.is_valid():
        #     print("=========================",serializer.initial_data['COL_ITEM_TXT_EMPH_TLTIP_VL'])
        #     if serializer.initial_data['COL_ITEM_TXT_EMPH_TLTIP_VL'] == 'blue_black':
        #         serializer.save()  # save to DB
        #         return Response(serializer.data)
        # return Response(serializer.errors)


    #PUT: The PUT method replaces all current representations of the target resource with the request payload.
    def update(self, request, pk=None):
        data = request.data
        serializer = ChartSerializer(data=data)
        isValid = self.validation_logic(serializer)
        print(isValid)
        if isValid == "error":
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        super().update(request)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED) #

    #PATCH: The PATCH method is used to apply partial modifications to a resource.
    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass


import pandas as pd
def export_value():
    authors = pd.read_excel("맘스터치권한세팅.xlsx")
    print(authors)





def export_to_bq(request): #chart_info 과거에 만든 것도(필드 추가나 제거된 것도) ->스키마를 보고 자동생성하기
    GOOGLE_APPLICATION_CREDENTIALS = "iam.json"

    client = bigquery.Client()

    QUERY0 = (
        "SELECT * FROM `gcloud-hlhl.data_set.box1` "
        "WHERE name = '손오공' "
        "LIMIT 100")
    QUERY = (
        "INSERT INTO gcloud-hlhl.data_set.box1 "
        "VALUES('SAMSUNG2ndGen', 200, 'CFO')")

    query_job = client.query(QUERY)
    rows = query_job.result()
    for row in rows:
        print(row.name)
    return redirect('../admin/')



def create_table_bq(request):

    client = bigquery.Client()
    table_id = bigquery.Table.from_string("gcloud-hlhl.data_set.chart_info")
    schema = [
            bigquery.SchemaField("COL_ITEM_TXT_EMPH_TLTIP_VL", "STRING"),
            bigquery.SchemaField("COL_AXISX_TTL_GNRL_VL", "STRING"),
            bigquery.SchemaField("COL_AXISX_TTL_EMPH_VL", "STRING"),
            bigquery.SchemaField("ITEM_SET_USYN", "STRING"),
            bigquery.SchemaField("ITEM_SET_MIN_VL","FLOAT"),
            bigquery.SchemaField("ITEM_SET_MAX_VL", "FLOAT"),
            bigquery.SchemaField("AXISY_USYN", "STRING"),
            bigquery.SchemaField("AXISY_CNT_MIN_VL", "FLOAT"),
            bigquery.SchemaField("AXISY_CNT_MAX_VL", "FLOAT"),
            bigquery.SchemaField("AXISY_TTL_NMB_MIN_VL", "FLOAT"),
            bigquery.SchemaField("AXISY_TTL_NMB_MAX_VL",  "FLOAT"),
            bigquery.SchemaField("AXISY_TTL_LET_CNT_MAX_VL", "FLOAT"),
            bigquery.SchemaField("COL_AXISY_TTL_VL", "STRING"),
            bigquery.SchemaField("COL_AXISY_LINE_VL", "STRING"),
            bigquery.SchemaField("LEGD_USYN", "STRING"),
            bigquery.SchemaField("LEGD_NMB_MIN_VL", "FLOAT"),
            bigquery.SchemaField("LEGD_NMB_MAX_VL", "FLOAT"),
            bigquery.SchemaField("LEGD_TXT_LET_CNT_MAX_VL", "FLOAT"),
            bigquery.SchemaField("COL_ITEM_EMPH_LEGD1_VL", "STRING"),
            bigquery.SchemaField("COL_ITEM_EMPH_LEGD2_VL", "STRING"),
            bigquery.SchemaField("COL_ITEM_EMPH_LEGD3_VL", "STRING"),
            bigquery.SchemaField("COL_ITEM_EMPH_LEGD4_VL", "STRING"),
            bigquery.SchemaField("COL_ITEM_EMPH_LEGD5_VL", "STRING"),
            bigquery.SchemaField("THRHLD_USYN", "STRING"),
            bigquery.SchemaField("THRHLD_RFLN_NMB_MIN_VL", "FLOAT"),
            bigquery.SchemaField("THRHLD_RFLN_NMB_MAX_VL", "FLOAT"),
            bigquery.SchemaField("THRHLD_TXT_LET_CNT_MAX_VL", "FLOAT"),
            bigquery.SchemaField("COL_THRHLD_RFLN_VL", "STRING"),
            bigquery.SchemaField("ASST_TXT_USYN", "STRING"),
            bigquery.SchemaField("ASST_TXT_NMB_MIN_VL", "FLOAT"),
            bigquery.SchemaField("ASST_TXT_NMB_MAX_VL", "FLOAT"),
            bigquery.SchemaField("ASST_TXT_LET_CNT", "FLOAT"),
            bigquery.SchemaField("COL_ASST_TXT_VL", "STRING"),
            bigquery.SchemaField("MSG_USYN", "STRING"),
            bigquery.SchemaField("MSG_ROW_CNT_MAX_VL", "FLOAT"),
            bigquery.SchemaField("MSG_ROW_CNT_MIN_VL", "FLOAT"),
            bigquery.SchemaField("MSG_ROW_LET_CNT_MAX_VL", "FLOAT"),
            bigquery.SchemaField("MSG_EMPH_CNT", "FLOAT"),
            bigquery.SchemaField("MSG_CNT", "FLOAT"),
            bigquery.SchemaField("MSG_IMPN_INDX_CNT", "FLOAT"),
            bigquery.SchemaField("MSG_ASST_INDX_CNT", "FLOAT"),
            bigquery.SchemaField("MSG_IMPN_INDX_LET_CNT_MAX_VL",        "FLOAT"),
            bigquery.SchemaField("MSG_ASST_INDX_TTL_LET_CNT_MAX_VL", "FLOAT"),
            bigquery.SchemaField("MSG_ASST_INDX_LET_CNT_MAX_VL", "FLOAT"),
            bigquery.SchemaField("MSG_STUS_ICON_CNT", "FLOAT"),
            bigquery.SchemaField("MSG_BTN_CNT", "FLOAT"),
            bigquery.SchemaField("COL_MSG_GNRL_VL",          "STRING"),
            bigquery.SchemaField("COL_MSG_EMPH_VL", "STRING"),
            bigquery.SchemaField("COL_IMPN_INDX_VL", "STRING"),
            bigquery.SchemaField("COL_ASST_INDX_TTL_VL", "STRING"),
            bigquery.SchemaField("COL_ASST_INDX_VL", "STRING"),
            bigquery.SchemaField("ITEM_PART_ALL_USYN",          "STRING"),
            bigquery.SchemaField("ITEM_TXT_NMB_PART_VL", "FLOAT"),
            bigquery.SchemaField("ITEM_TXT_NMB_ALL_VL", "FLOAT"),
            bigquery.SchemaField("COL_ITEM_GNRL_PART_VL", "STRING"),
            bigquery.SchemaField("COL_ITEM_GNRL_ALL_VL", "STRING"),
            bigquery.SchemaField("COL_ITEM_EMPH_PART_VL",             "STRING"),
            bigquery.SchemaField("COL_ITEM_EMPH_ALL_VL", "STRING"),
            bigquery.SchemaField("COL_ITEM_TXT_EMPH_PART_VL", "STRING"),
            bigquery.SchemaField("COL_ITEM_TXT_EMPH_ALL_VL", "STRING"),
            bigquery.SchemaField("TBL_YN", "STRING"),
            bigquery.SchemaField("COL_TBL_TXT_VL",            "STRING"),
            bigquery.SchemaField("COL_TBL_DSNC_LINE_VL", "STRING"),
            bigquery.SchemaField("COL_TBL_TTL_VL", "STRING"),
            bigquery.SchemaField("COL_TBL_TTL_BGD_VL", "STRING"),
            bigquery.SchemaField("USYN", "STRING"),
            bigquery.SchemaField("RGPR_ID", "STRING"),
            bigquery.SchemaField("RGDA", "STRING"),
            bigquery.SchemaField("MDPR_ID", "STRING"),
            bigquery.SchemaField("LAST_MDFC_DTTM",            "STRING"),
        ]
    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)
    print(
            "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )
    return redirect('../admin/')