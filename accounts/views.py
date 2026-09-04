from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash
)

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import StudentProfileForm

from academics.models import Result, Marksheet

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


# ==========================================
# STUDENT LOGIN
# ==========================================

def student_login(request):

    if request.user.is_authenticated:

        if hasattr(request.user, 'student_profile'):

            return redirect('student_dashboard')

        else:

            logout(request)

    if request.method == 'POST':

        student_id = request.POST.get('student_id')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=student_id,
            password=password
        )

        if user is not None:

            if hasattr(user, 'student_profile'):

                login(request, user)

                return redirect('student_dashboard')

        return render(
            request,
            'accounts/login.html',
            {
                'error': 'Invalid Student ID or Password'
            }
        )

    return render(
        request,
        'accounts/login.html'
    )


# ==========================================
# STUDENT DASHBOARD
# ==========================================

@login_required
def student_dashboard(request):

    student = request.user.student_profile

    return render(
        request,
        'accounts/dashboard.html',
        {
            'student': student
        }
    )


# ==========================================
# STUDENT PROFILE EDIT
# ==========================================

@login_required
def student_profile(request):

    student = request.user.student_profile

    if request.method == 'POST':

        form = StudentProfileForm(
            request.POST,
            request.FILES,
            instance=student,
            user=request.user
        )

        if form.is_valid():

            form.save()

            return redirect('student_profile')

    else:

        form = StudentProfileForm(
            instance=student,
            user=request.user
        )

    return render(
        request,
        'accounts/profile.html',
        {
            'student': student,
            'form': form
        }
    )


# ==========================================
# CHANGE PASSWORD
# ==========================================

@login_required
def change_password(request):

    if request.method == 'POST':

        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            # Password change ke baad student logout nahi hoga
            update_session_auth_hash(
                request,
                user
            )

            return render(
                request,
                'accounts/password_success.html'
            )

    else:

        form = PasswordChangeForm(
            request.user
        )

    return render(
        request,
        'accounts/change_password.html',
        {
            'form': form
        }
    )


# ==========================================
# STUDENT RESULTS
# ==========================================

@login_required
def student_results(request):

    student = request.user.student_profile

    results = Result.objects.filter(
        student=student
    ).order_by(
        'semester',
        'subject_code'
    )

    return render(
        request,
        'accounts/results.html',
        {
            'student': student,
            'results': results
        }
    )


# ==========================================
# STUDENT MARKSHEETS
# ==========================================

@login_required
def student_marksheets(request):

    student = request.user.student_profile

    marksheets = Marksheet.objects.filter(
        student=student,
        is_published=True
    ).order_by(
        '-semester'
    )

    return render(
        request,
        'accounts/marksheets.html',
        {
            'student': student,
            'marksheets': marksheets
        }
    )


# ==========================================
# DOWNLOAD MARKSHEET PDF
# ==========================================

# ==========================================
# DOWNLOAD MARKSHEET PDF
# ==========================================

@login_required
def download_marksheet(request, marksheet_id):

    student = request.user.student_profile

    try:
        marksheet = Marksheet.objects.get(
            id=marksheet_id,
            student=student,
            is_published=True
        )

    except Marksheet.DoesNotExist:
        return HttpResponse(
            "Marksheet not found or access denied.",
            status=404
        )

    # Latest fee status check
    if student.current_fee_status != 'PAID':

        return HttpResponse(
            """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Fee Pending</title>

                <style>
                    body {
                        margin: 0;
                        padding: 0;
                        font-family: Arial, sans-serif;
                        background: #f4f6f9;
                    }

                    .box {
                        width: 90%;
                        max-width: 500px;
                        margin: 100px auto;
                        padding: 35px;
                        text-align: center;
                        background: white;
                        border-radius: 12px;
                        box-shadow: 0 4px 18px
                            rgba(0, 0, 0, 0.12);
                    }

                    h1 {
                        color: #d00000;
                    }

                    p {
                        color: #555;
                        line-height: 1.6;
                    }

                    a {
                        display: inline-block;
                        margin-top: 20px;
                        padding: 12px 22px;
                        color: white;
                        background: #1f4e79;
                        text-decoration: none;
                        border-radius: 7px;
                    }
                </style>
            </head>

            <body>
                <div class="box">

                    <h1>FEE PENDING</h1>

                    <p>
                        Your latest fee voucher is not marked as paid.
                        Please clear your fee dues before downloading
                        the marksheet.
                    </p>

                    <a href="/finance/vouchers/">
                        View Fee Vouchers
                    </a>

                </div>
            </body>
            </html>
            """,
            status=403
        )

    # Get only this marksheet semester results
    results = Result.objects.filter(
        student=student,
        semester=marksheet.semester
    ).order_by(
        'subject_code'
    )

    # PDF response
    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; '
        f'filename="Marksheet_{student.student_id}_'
        f'Semester_{marksheet.semester}.pdf"'
    )

    document = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'MarksheetTitle',
        parent=styles['Title'],
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        spaceAfter=8
    )

    center_style = ParagraphStyle(
        'MarksheetCenter',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        alignment=TA_CENTER
    )

    heading_style = ParagraphStyle(
        'MarksheetHeading',
        parent=styles['Heading2'],
        fontSize=13,
        spaceBefore=10,
        spaceAfter=8
    )

    story = []

    # University heading
    story.append(
        Paragraph(
            "UNIVERSITY STUDENT PORTAL",
            title_style
        )
    )

    story.append(
        Paragraph(
            "OFFICIAL ACADEMIC MARKSHEET",
            center_style
        )
    )

    story.append(
        Spacer(1, 12)
    )

    # Student information
    student_data = [
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
            "Program",
            student.program
        ],
        [
            "Department",
            student.department
        ],
        [
            "Semester",
            marksheet.get_semester_display()
        ],
        [
            "Issue Date",
            str(marksheet.issue_date)
        ],
    ]

    student_table = Table(
        student_data,
        colWidths=[
            45 * mm,
            120 * mm
        ]
    )

    student_table.setStyle(
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
                7
            ),
            (
                'RIGHTPADDING',
                (0, 0),
                (-1, -1),
                7
            ),
            (
                'TOPPADDING',
                (0, 0),
                (-1, -1),
                6
            ),
            (
                'BOTTOMPADDING',
                (0, 0),
                (-1, -1),
                6
            ),
        ])
    )

    story.append(student_table)

    story.append(
        Spacer(1, 15)
    )

    # Academic results heading
    story.append(
        Paragraph(
            "Academic Results",
            heading_style
        )
    )

    result_data = [
        [
            "Subject Code",
            "Subject",
            "Credit",
            "Obtained",
            "Total",
            "Percentage",
            "Grade"
        ]
    ]

    total_obtained = 0
    total_marks = 0

    for result in results:

        total_obtained += float(
            result.obtained_marks
        )

        total_marks += float(
            result.total_marks
        )

        result_data.append(
            [
                result.subject_code,
                result.subject_name,
                result.credit_hours,
                result.obtained_marks,
                result.total_marks,
                f"{result.percentage()}%",
                result.grade()
            ]
        )

    result_table = Table(
        result_data,
        repeatRows=1,
        colWidths=[
            25 * mm,
            48 * mm,
            18 * mm,
            22 * mm,
            22 * mm,
            25 * mm,
            18 * mm
        ]
    )

    result_table.setStyle(
        TableStyle([
            (
                'BACKGROUND',
                (0, 0),
                (-1, 0),
                colors.HexColor('#1e3a8a')
            ),
            (
                'TEXTCOLOR',
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                'FONTNAME',
                (0, 0),
                (-1, 0),
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
                'ALIGN',
                (2, 1),
                (-1, -1),
                'CENTER'
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
                5
            ),
            (
                'RIGHTPADDING',
                (0, 0),
                (-1, -1),
                5
            ),
            (
                'TOPPADDING',
                (0, 0),
                (-1, -1),
                6
            ),
            (
                'BOTTOMPADDING',
                (0, 0),
                (-1, -1),
                6
            ),
        ])
    )

    story.append(result_table)

    story.append(
        Spacer(1, 18)
    )

    # Summary
    if total_marks > 0:
        overall_percentage = round(
            (total_obtained / total_marks) * 100,
            2
        )
    else:
        overall_percentage = 0

    summary_data = [
        [
            "Total Obtained Marks",
            f"{total_obtained:g}"
        ],
        [
            "Total Marks",
            f"{total_marks:g}"
        ],
        [
            "Overall Percentage",
            f"{overall_percentage}%"
        ],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[
            65 * mm,
            48 * mm
        ]
    )

    summary_table.setStyle(
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
                'ALIGN',
                (1, 0),
                (1, -1),
                'CENTER'
            ),
            (
                'PADDING',
                (0, 0),
                (-1, -1),
                7
            ),
        ])
    )

    story.append(summary_table)

    story.append(
        Spacer(1, 25)
    )

    story.append(
        Paragraph(
            "This is a system-generated marksheet.",
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


# ==========================================
# STUDENT LOGOUT
# ==========================================

def student_logout(request):

    logout(request)

    return redirect('student_login')