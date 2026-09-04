from django.urls import path

from . import views


urlpatterns = [

    path(
        'vouchers/',
        views.student_fee_vouchers,
        name='student_fee_vouchers'
    ),

    path(
        'vouchers/<int:voucher_id>/download/',
        views.download_fee_voucher,
        name='download_fee_voucher'
    ),

]