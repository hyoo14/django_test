import pandas as pd
from django.shortcuts import render, redirect

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response

#from charts.forms import RegisterForm
from .serializers import ChartSerializer
from .models import Chart
from google.cloud import bigquery

#에러로그 추가
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