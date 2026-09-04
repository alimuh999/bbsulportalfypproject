from django.urls import path

from . import views


app_name = 'degree_clearance'


urlpatterns = [

    path(
        '',
        views.degree_clearance,
        name='degree_clearance'
    ),

    path(
        'apply/',
        views.apply_degree_clearance,
        name='apply'
    ),

    path(
        'detail/<int:application_id>/',
        views.degree_clearance_detail,
        name='detail'
    ),
]