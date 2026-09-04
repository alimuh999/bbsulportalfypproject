from django.urls import path
from . import views

app_name = 'gatepasses'

urlpatterns = [
    path(
        '',
        views.gate_pass_list,
        name='gate_pass_list'
    ),

    path(
        'create/',
        views.create_gate_pass,
        name='create_gate_pass'
    ),

    path(
        '<int:gate_pass_id>/',
        views.gate_pass_detail,
        name='gate_pass_detail'
    ),

    path(
        '<int:gate_pass_id>/download/',
        views.download_gate_pass_pdf,
        name='download_gate_pass_pdf'
    ),
]