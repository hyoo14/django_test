"""chart_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from django.contrib import admin
from django.conf.urls import include  #url deprecated
from rest_framework import routers
from charts.views import ChartViewSet, export_to_bq, create_table_bq

router = routers.DefaultRouter()
router.register('charts', ChartViewSet)#라우터가 viewset과 url 자동매핑

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('export/', export_to_bq, name="export_to_bq"),
    path('create/', create_table_bq, name="create_table_bq"),
]
