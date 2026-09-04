from django.urls import path
from . import views


app_name = 'examinations'


urlpatterns = [
    path(
        '',
        views.exam_form_list,
        name='exam_form_list'
    ),

    path(
        'create/',
        views.create_exam_form,
        name='create_exam_form'
    ),

    path(
        '<int:exam_form_id>/subjects/',
        views.select_subjects,
        name='select_subjects'
    ),

    path(
        '<int:exam_form_id>/',
        views.exam_form_detail,
        name='exam_form_detail'
    ),
]