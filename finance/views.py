from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.units import mm

from .models import FeeVoucher


# ==========================================
# STUDENT FEE VOUCHERS
# ==========================================

@login_required
def student_fee_vouchers(request):

    student = request.user.student_profile

    vouchers = FeeVoucher.objects.filter(
        student=student
    ).order_by(
        '-issue_date'
    )

    return render(
        request,
        'finance/vouchers.html',
        {
            'student': student,
            'vouchers': vouchers
        }
    )


# ==========================================
# DOWNLOAD FEE VOUCHER PDF
# ==========================================

@login_required
def download_fee_voucher(request, voucher_id):

    student = request.user.student_profile

    # Student sirf apna voucher download kar sakta hai
    try:

        voucher = FeeVoucher.objects.get(
            id=voucher_id,
            student=student
        )

    except FeeVoucher.DoesNotExist:

        return HttpResponse(
            "Fee voucher not found or access denied.",
            status=404
        )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; '
        f'filename="Fee_Voucher_{voucher.voucher_number}.pdf"'
    )

    document = SimpleDocTemplate(

        response,

        pagesize=A4,

        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'VoucherTitle',
        parent=styles['Title'],
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        spaceAfter=8
    )

    center_style = ParagraphStyle(
        'VoucherCenter',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        alignment=TA_CENTER
    )

    heading_style = ParagraphStyle(
        'VoucherHeading',
        parent=styles['Heading2'],
        fontSize=13,
        spaceBefore=10,
        spaceAfter=8
    )

    story = []

    # ==========================================
    # HEADER
    # ==========================================

    story.append(
        Paragraph(
            "UNIVERSITY STUDENT PORTAL",
            title_style
        )
    )

    story.append(
        Paragraph(
            "FEE VOUCHER",
            center_style
        )
    )

    story.append(
        Spacer(1, 18)
    )

    # ==========================================
    # VOUCHER INFORMATION
    # ==========================================

    voucher_data = [

        [
            "Voucher Number",
            voucher.voucher_number
        ],

        [
            "Student Name",
            student.user.get_full_name()
        ],

        [
            "Student ID",
            student.student_id
        ],

        [
            "Registration No.",
            student.registration_no
        ],

        [
            "Father Name",
            student.father_name
        ],

        [
            "Department",
            student.department
        ],

        [
            "Program",
            student.program
        ],

        [
            "Semester",
            voucher.semester
        ],

        [
            "Issue Date",
            str(voucher.issue_date)
        ],

        [
            "Due Date",
            str(voucher.due_date)
        ],

        [
            "Fee Amount",
            f"Rs. {voucher.amount}"
        ],

        [
            "Status",
            voucher.get_status_display()
        ],

    ]

    voucher_table = Table(
        voucher_data,
        colWidths=[
            55 * mm,
            110 * mm
        ]
    )

    voucher_table.setStyle(

        TableStyle([

            (
                'BACKGROUND',
                (0, 0),
                (0, -1),
                colors.lightgrey
            ),

            (
                'FONTNAME',
                (0, 0),
                (0, -1),
                'Helvetica-Bold'
            ),

            (
                'GRID',
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                'VALIGN',
                (0, 0),
                (-1, -1),
                'MIDDLE'
            ),

            (
                'LEFTPADDING',
                (0, 0),
                (-1, -1),
                8
            ),

            (
                'RIGHTPADDING',
                (0, 0),
                (-1, -1),
                8
            ),

            (
                'TOPPADDING',
                (0, 0),
                (-1, -1),
                8
            ),

            (
                'BOTTOMPADDING',
                (0, 0),
                (-1, -1),
                8
            ),

        ])
    )

    story.append(voucher_table)

    story.append(
        Spacer(1, 18)
    )

    # ==========================================
    # DESCRIPTION
    # ==========================================

    if voucher.description:

        story.append(
            Paragraph(
                "Description",
                heading_style
            )
        )

        story.append(
            Paragraph(
                voucher.description,
                styles['Normal']
            )
        )

        story.append(
            Spacer(1, 15)
        )

    # ==========================================
    # PAYMENT INSTRUCTION
    # ==========================================

    story.append(
        Paragraph(
            "Please pay the fee before the due date.",
            center_style
        )
    )

    story.append(
        Spacer(1, 10)
    )

    story.append(
        Paragraph(
            "This is a system-generated fee voucher.",
            center_style
        )
    )

    story.append(
        Paragraph(
            "University Student Management Portal",
            center_style
        )
    )

    document.build(story)

    return response