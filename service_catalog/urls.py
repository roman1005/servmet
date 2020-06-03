"""service_catalog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin
from .api import router
from app1 import views
from app1.api_views import StaffView, ServiceView, MetricView

urlpatterns = [

    url(r'^admin/', admin.site.urls),

    url(r'^idealweight/',views.IdealWeight),

    path(r'api/v1/', include(router.urls)),

    path('staff/', StaffView.as_view()),

    path('api/services/', ServiceView.as_view()),

    path('api/services/<uuid:pk>/', ServiceView.as_view()),

    path('api/metrics/', MetricView.as_view())
]
