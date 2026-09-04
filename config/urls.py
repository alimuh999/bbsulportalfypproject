from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        include('accounts.urls')
    ),

    path(
        'finance/',
        include('finance.urls')
    ),

    path(
    'examinations/',
    include('examinations.urls')
    ),

    path(
    'leaves/',
    include('leaves.urls')
    ),

    path('gatepasses/',
    include('gatepasses.urls')),

    path(
        'transport/',
        include('transport.urls')
    ),

    path(
    'degree-clearance/',
    include('degree_clearance.urls')
    ),

    path(
        "assistant/",
        include("assistant.urls")
    ),

]