from django.urls import path
from . import views


app_name = 'leaves'


urlpatterns = [
    path(
        '',
        views.leave_request_list,
        name='leave_request_list'
    ),

    path(
        'create/',
        views.create_leave_request,
        name='create_leave_request'
    ),

    path(
        '<int:leave_id>/',
        views.leave_request_detail,
        name='leave_request_detail'
    ),
]