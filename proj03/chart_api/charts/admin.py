import json

from django.contrib import admin
from django.contrib.admin.exceptions import DisallowedModelAdminToField
from django.db import transaction, router
from django.http import HttpResponseRedirect

from charts import models
from charts.models import Chart
#from chart_api import models
# Register your models here.
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from charts.serializers import ChartSerializer
@admin.register(models.Chart)
class ChartAdmin(admin.ModelAdmin):
    # list_per_page = 5
    # list_display = (
    #     'id', 'COL_ITEM_TXT_EMPH_TLTIP_VL', 'COL_AXISX_TTL_GNRL_VL', 'COL_AXISX_TTL_EMPH_VL',
    # )
    # list_editable = ('is_deleted',

    list_display = (
        'id','CHART_CD','CHART_TPCD', 'COL_ITEM_TXT_EMPH_TLTIP_VL', 'COL_AXISX_TTL_GNRL_VL', 'COL_AXISX_TTL_EMPH_VL',
    )

    def add_view(self, request, extra_content=None):#def add_view(self, request, form_url='', extra_context=None):
        #return super(ChartAdmin, self).add_view(request)
        print(request.method)
        if request.method == "GET":
            return self.changeform_view(request, None, '', None)
        return self.changeform_view2(request, None, '', None)

#외부함수로 검증 로직을 빼는 것 고
    def validation_logic(self, request):
        chart_cd, chart_tpcd = request.POST.get('CHART_CD'), request.POST.get('CHART_TPCD')
        char_COL_ITEM_TXT_EMPH_TLTIP_VL = request.POST.get('COL_ITEM_TXT_EMPH_TLTIP_VL')

        #chart_cd와 chart_tpcd는 모두 있어야
        #if chart_cd is not None and chart_tpcd is not None:
        #이 케이스 제외 제낌
        print("work")
        if chart_cd is None or chart_tpcd is None:
            return "error" #HttpResponseRedirect('admin/')

        if str(chart_tpcd) + "_" not in str(chart_cd):
            return "error" #HttpResponseRedirect('admin/')

        if str(chart_tpcd) == "LINE" and len(char_COL_ITEM_TXT_EMPH_TLTIP_VL) == 0:
            return "error" #HttpResponseRedirect('admin/')

        print(chart_cd, '  ', chart_tpcd, '   ', len(char_COL_ITEM_TXT_EMPH_TLTIP_VL))
        return "no error"
        # if chart_cd is not None and chart_tpcd is not None:  # 조건 추가
        #     print(chart_cd, '  ', chart_tpcd, '   ', len(char_COL_ITEM_TXT_EMPH_TLTIP_VL))
        #
        #     if str(chart_tpcd) + "_" in str(chart_cd):
        #         if str(chart_tpcd) == "LINE" and len(char_COL_ITEM_TXT_EMPH_TLTIP_VL) == 0:
        #             return HttpResponseRedirect('admin/')
        #
        #         with transaction.atomic(using=router.db_for_write(self.model)):
        #             return self._changeform_view(request, object_id, form_url, extra_context)
        #     return HttpResponseRedirect('admin/')

    def changeform_view2(self, request, object_id=None, form_url='', extra_context=None):
        print("#################################################")
        isValid = self.validation_logic(request)
        print(isValid)
        if isValid == "error":
            print("work?? error??")
            HttpResponseRedirect('admin/')
            print("??-----------")
            model = self.model
            opts = model._meta
            #return self._get_obj_does_not_exist_redirect(request, opts, object_id)
            raise DisallowedModelAdminToField("Your field has a problem.")

        #        else:##기존의 changeform_view 메서드
        else:
            with transaction.atomic(using=router.db_for_write(self.model)):
                return self._changeform_view(request, object_id, form_url, extra_context)






admin.site.unregister(User)
admin.site.unregister(Group)


admin.site.site_header = 'Chart Manager'
admin.site.site_title = 'Chart Manager'
admin.site.index_title = 'Chart Information Manager'
#admin.site.register(Chart)
