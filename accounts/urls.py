from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.student_login,
        name='student_login'
    ),

    path(
        'dashboard/',
        views.student_dashboard,
        name='student_dashboard'
    ),

    path(
        'profile/',
        views.student_profile,
        name='student_profile'
    ),

    path(
        'change-password/',
        views.change_password,
        name='change_password'
    ),

    path(
        'results/',
        views.student_results,
        name='student_results'
    ),

    path(
        'marksheets/',
        views.student_marksheets,
        name='student_marksheets'
    ),

    path(
        'marksheets/<int:marksheet_id>/download/',
        views.download_marksheet,
        name='download_marksheet'
    ),

    path(
        'logout/',
        views.student_logout,
        name='student_logout'
    ),

]