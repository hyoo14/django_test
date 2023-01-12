# views.py
"""
필요한 데이터를 모델(혹은 연동될 bigquery, sharepoint와 같은 외부)에서 가져와서 가공, 웹 페이지 결과를 만들도록하는 컨트롤러

차트 모델 CRUD용 쿼리셋 클래스 포함
빅쿼리 관련 함수들은 추후 고도화 예정
sharepoint 연동 추가 예정

사용 가능 함수:
-
"""
import pandas as pd
from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from charts.forms import RegisterForm
from .serializers import ChartSerializer
from .models import Chart
from google.cloud import bigquery
import logging

logger = logging.getLogger("myLogger")  # 에러 로거

class ChartViewSet(viewsets.ModelViewSet):
    """
    Django에서 제공해주는 기본 crud로직 그룹화한 viewset으로 Chart용 CRUD 제공한다.

    create, update 메서드를 오버라이드해서 검증로직을 추가해주었다.
    """
    queryset = Chart.objects.all()
    serializer_class = ChartSerializer

    def validation_logic(self, serializer):
        """
        검증로직으로 오류인 경우를 찾아준다.

        chart_cd, chart_tpcd 네이밍, 차트 타입에 따라서 필수인 필드와 아닌 필드가 잘 쓰였는지 검사된다.

        Args:
            serializer: chart가 가진 모든 value들을 담은 serializer

        Returns:
            에러인 경우 "error" 반환하고 에러가 검출되지 않은 경우 "no error" 반환

        """

        if not serializer.is_valid():  # table 스키마 검증
            logger.error( ("테이블 스키마 오류") )
            return False
        chart_cd = serializer.initial_data.get('CHART_CD')
        chart_tpcd = serializer.initial_data.get('CHART_TPCD')
        chart_COL_ITEM_TXT_EMPH_TLTIP_VL = serializer.initial_data.get('COL_ITEM_TXT_EMPH_TLTIP_VL')

        logger.error("validation logic works")  # 검증 로직 작동 로그를 파일로 출력
        # logger.info(chart_cd, '  ', chart_tpcd, '   ', len(chart_COL_ITEM_TXT_EMPH_TLTIP_VL))


        if chart_cd is None or chart_tpcd is None:  # chart_cd, chart_tpcd 입력 검증
            logger.error("chart_cd, chart_tpcd 입력 오류")
            return False

        if str(chart_tpcd) + "_" not in str(chart_cd):  # chart_cd, chart_tpcd 네이밍 검증
            logger.error("chart_cd 명명 오류")
            return False

        if str(chart_tpcd) == "LINE" and len(chart_COL_ITEM_TXT_EMPH_TLTIP_VL) == 0:  # chart_tpcd에 따른 필수필드 검증
            logger.error("필수 필드 미입력 오류")
            return False

        return True

    def create(self, request):
        """
        chart info를 추가한다.

        Argus:
            request: 리퀘스트(에 포함된 데이터)

        Return:
            Response: 응답 반환(http status code 포함)

        """
        data = request.data
        serializer = ChartSerializer(data=data)
        is_valid = self.validation_logic(serializer) # 검증 로직
        # try/catch exception handling 형태로
        if is_valid is False:  # 검증 오류시 400반환
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)  # 검증 오류 발견되지 않을 경우 201 반환

    def update(self, request, *args, **kwargs): #pk=None):
        """
        chart info를 수정한다.

        The PUT method replaces all current representations of the target resource with the request payload.

        Argus:
            request: 리퀘스트(에 포함된 데이터)

        Return:
            Response: 응답 반환(http status code 포함)

        """
        data = request.data
        serializer = ChartSerializer(data=data)
        is_valid = self.validation_logic(serializer)

        if is_valid is False:   # 검증 오류시 400 http status code 반환
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        super().update(request, *args, **kwargs) #super().update(request)     # 오류 없을 경우 update 및 202 http status code 반환

        return Response(serializer.data, status=status.HTTP_200_OK)   # 202 코드 조사, 200번대 수정 때



    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


####### 패치(파셜 업데이트) 에러로그 500만 남. 왜 나는지, 어떻게 처리해야하는지도 알아볼 것
    # def partial_update(self, request, pk=None):
          # PATCH: The PATCH method is used to apply partial modifications to a resource.
    #     pass

    # def destroy(self, request, pk=None):
    #     pass


######################################## related to biquery test ########################################

# 서비스 계정 키 설정 맟 디비커넥션
import glob
from google.oauth2 import service_account
from google.cloud import bigquery
import psycopg2

# 서비스 계정 키 JSON 파일 경로
key_path = glob.glob("hlhl2-374201-1ba184d467da.json")[0]

# Credentials 객체 생성
credentials = service_account.Credentials.from_service_account_file(key_path)

# table 세팅
dataset_id = "hlhl2-374201.test_dataset_00"
dataset = bigquery.Dataset(dataset_id)
table_id = dataset_id + ".test_table_00"

schema = [
        bigquery.SchemaField("id", "STRING"),
        bigquery.SchemaField("COL_ITEM_TXT_EMPH_TLTIP_VL", "STRING"),
        bigquery.SchemaField("COL_AXISX_TTL_GNRL_VL", "STRING"),
        bigquery.SchemaField("COL_AXISX_TTL_EMPH_VL", "STRING"),
        bigquery.SchemaField("ITEM_SET_USYN", "STRING"),
        bigquery.SchemaField("ITEM_SET_MIN_VL", "FLOAT"),
        bigquery.SchemaField("ITEM_SET_MAX_VL", "FLOAT"),
        bigquery.SchemaField("AXISY_USYN", "STRING"),
        bigquery.SchemaField("AXISY_CNT_MIN_VL", "FLOAT"),
        bigquery.SchemaField("AXISY_CNT_MAX_VL", "FLOAT"),
        bigquery.SchemaField("AXISY_TTL_NMB_MIN_VL", "FLOAT"),
        bigquery.SchemaField("AXISY_TTL_NMB_MAX_VL", "FLOAT"),
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
        bigquery.SchemaField("COL_THRHLD_TXT_VL", "STRING"),
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
        bigquery.SchemaField("MSG_IMPN_INDX_LET_CNT_MAX_VL", "FLOAT"),
        bigquery.SchemaField("MSG_ASST_INDX_TTL_LET_CNT_MAX_VL", "FLOAT"),
        bigquery.SchemaField("MSG_ASST_INDX_LET_CNT_MAX_VL", "FLOAT"),
        bigquery.SchemaField("MSG_STUS_ICON_CNT", "FLOAT"),
        bigquery.SchemaField("MSG_BTN_CNT", "FLOAT"),
        bigquery.SchemaField("COL_MSG_GNRL_VL", "STRING"),
        bigquery.SchemaField("COL_MSG_EMPH_VL", "STRING"),
        bigquery.SchemaField("COL_IMPN_INDX_VL", "STRING"),
        bigquery.SchemaField("COL_ASST_INDX_TTL_VL", "STRING"),
        bigquery.SchemaField("COL_ASST_INDX_VL", "STRING"),
        bigquery.SchemaField("ITEM_PART_ALL_USYN", "STRING"),
        bigquery.SchemaField("ITEM_TXT_NMB_PART_VL", "FLOAT"),
        bigquery.SchemaField("ITEM_TXT_NMB_ALL_VL", "FLOAT"),
        bigquery.SchemaField("COL_ITEM_GNRL_PART_VL", "STRING"),
        bigquery.SchemaField("COL_ITEM_GNRL_ALL_VL", "STRING"),
        bigquery.SchemaField("COL_ITEM_EMPH_PART_VL", "STRING"),
        bigquery.SchemaField("COL_ITEM_EMPH_ALL_VL", "STRING"),
        bigquery.SchemaField("COL_ITEM_TXT_EMPH_PART_VL", "STRING"),
        bigquery.SchemaField("COL_ITEM_TXT_EMPH_ALL_VL", "STRING"),
        bigquery.SchemaField("TBL_YN", "STRING"),
        bigquery.SchemaField("COL_TBL_TXT_VL", "STRING"),
        bigquery.SchemaField("COL_TBL_DSNC_LINE_VL", "STRING"),
        bigquery.SchemaField("COL_TBL_TTL_VL", "STRING"),
        bigquery.SchemaField("COL_TBL_TTL_BGD_VL", "STRING"),
        bigquery.SchemaField("USYN", "STRING"),
        bigquery.SchemaField("RGPR_ID", "STRING"),
        bigquery.SchemaField("RGDA", "STRING"),
        bigquery.SchemaField("MDPR_ID", "STRING"),
        bigquery.SchemaField("LAST_MDFC_DTTM", "STRING"),
        bigquery.SchemaField("CHART_CD", "STRING"),
        bigquery.SchemaField("CHART_TPCD", "STRING"),
    ]


def to_bq(request):
    # GCP 클라이언트 객체 생성
    client = bigquery.Client(credentials=credentials,
                             project=credentials.project_id)

    connection = psycopg2.connect(host="127.0.0.1", dbname="chart", user="hl", password="hl", port=5432)
    cur = connection.cursor()
    cur.execute("SELECT * FROM charts_chart;")
    datum = cur.fetchall()

    rows_to_insert = []
    for data in datum:
        # print(len(data),'  ',data)
        form = {}
        i = 0
        for value in data:
            # print(value, i)
            if value is not None:
                form[schema[i].name] = value
            i += 1
        rows_to_insert.append(form)

    # API 리퀘스트
    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))

    return redirect('../admin/')
def val_return(strval, scr):
    #1234567
    #3210123
    scr_num = '3210123'
    if scr < 4: return strval[0], int(scr_num[scr-1])
    elif scr > 4: return strval[1], int(scr_num[scr-1])
    else: return False



def bq_connection(req, val):
    client = bigquery.Client(credentials=credentials,
                             project=credentials.project_id)
    an = ""
    #1
    d, l = {}, 'RTCFJMAN' #rtcfjman'
    connection = psycopg2.connect(host="127.0.0.1", dbname="chart", user="hl", password="hl", port=5432)
    for v in l: d[v] = 0
    cur = connection.cursor()
    for i in range(len(req)):
        val_ret = val_return(req[i], val[i])
        if val_ret: d[ val_ret[0] ] += val_ret[1]
    cur.execute("SELECT * FROM charts_chart;")
    if d[l[0]] >= d[l[1]]: an += l[0]
    else: an += l[1]
    if d[l[2]] >= d[l[3]]: an += l[2]
    else: an += l[3]
    if d[l[4]] >= d[l[5]]: an += l[4]
    else: an += l[5]
    if d[l[6]] >= d[l[7]]: an += l[6]
    else: an += l[7]


    datum = cur.fetchall()

    print(an)

    return client

def from_bq(request):
    # GCP 클라이언트 객체 생성
    client = bigquery.Client(credentials=credentials,
                             project=credentials.project_id)

    connection = psycopg2.connect(host="127.0.0.1", dbname="chart", user="hl", password="hl", port=5432)
    cur = connection.cursor()
    cur.execute("SELECT * FROM charts_chart;")
    datum = cur.fetchall()

    rows_to_insert = []
    for data in datum:
        # print(len(data),'  ',data)
        form = {}
        i = 0
        for value in data:
            # print(value, i)
            if value is not None:
                form[schema[i].name] = value
            i += 1
        rows_to_insert.append(form)
        #1rt 2cf 3jm 4an = 16ways, nq7ans( n3/2/1/0/1/2/3a )

    # API 리퀘스트
    errors = client.insert_rows_json(table_id, rows_to_insert)
    #'tcma' ['an','cf','mj','rt','na'] [5,3,2,7,5]
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))
    print( bq_connection( ['AN','CF','MJ','RT','NA'] , [5,3,2,7,5]) )

    return redirect('../admin/')


def delete_table_bq(request):
    # GCP 클라이언트 객체 생성
    client = bigquery.Client(credentials=credentials,
                             project=credentials.project_id)
    # API 리퀘스트
    client.delete_table(table_id, not_found_ok=True)
    print("Deleted table '{}'.".format(table_id))

    return redirect('../admin/')


def create_table_bq(request):
    client = bigquery.Client(credentials=credentials,
                             project=credentials.project_id)

    # table_id = bigquery.Table.from_string("gcloud-hlhl.data_set.chart_info")
    # schema = [
    #     bigquery.SchemaField("id", "STRING"),
    # ]
    # 테이블 아이디, 스키마 전역변수로 설정해놓음.. 테스트 이후 파라미터로 바꿀 것

    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)
    print(
            "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )

    return redirect('../admin/')








######################################## 다른 곳에 구현 또는 테스트의 테스트용 ########################################


import pandas as pd


def export_value():
    authors = pd.read_excel("맘스터치권한세팅.xlsx")
    print(authors)


def export_to_bq(request):  # chart_info 과거에 만든 것도(필드 추가나 제거된 것도) ->스키마를 보고 자동생성하기
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