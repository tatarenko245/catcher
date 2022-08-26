from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('manual_searching/', manual_searching),
    path('support/', support),
    path('x-operation-id/<uuid:x_operation_id>/', get_by_x_oper_id),
    path('ocid/<slug:ocid>/', get_by_ocid)
]
