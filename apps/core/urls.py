from django.urls import path

from .views import *


urlpatterns = [
    path('index', index, name='index'),
    path('vc', vc_index, name='vc'),
    path('add', business_create, name='add'),
    path('report_detail/<int:id>/', report_detail, name='report_detail'),
    path('report_detail/<int:id>/income_create/', income_create, name='income_create'),
    path('report_detail/<int:id>/outcome_create/', outcome_create, name='outcome_create'),
    # path('business/<int:id>/', products_videos),
    # path('businesscreate/', contacts),
    # path('outcomecreate/', productdetail),
    # path('incomecreate/', servicedetail),
]