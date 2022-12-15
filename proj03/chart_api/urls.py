
from django.conf.urls import url,include
from django.contrib import admin
from rest_framework import routers
from charts.views import ChartViewSet

router = routers.DefaultRouter() 
router.register('chartscharts',ChartViewSet) # prefix = charts , viewset = ChartViewSet

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^',include(router.urls)),
]
