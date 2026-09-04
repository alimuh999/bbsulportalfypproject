from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import DegreeClearance
from .forms import DegreeClearanceForm

from academics.models import Result, Marksheet


# =========================================================
# CHECK DEGREE CLEARANCE ELIGIBILITY
# =========================================================

def check_degree_clearance_eligibility(student):

    reasons = []

    # -----------------------------------------------------
    # Student must have completed semester 8
    # -----------------------------------------------------

    if student.semester < 8:
        reasons.append(
            "You have not completed the 8th semester yet."
        )

    # -----------------------------------------------------
    # Semester 8 marksheet must exist and be published
    # -----------------------------------------------------

    semester_8_marksheet_exists = Marksheet.objects.filter(
        student=student,
        semester=8,
        is_published=True
    ).exists()

    if not semester_8_marksheet_exists:
        reasons.append(
            "Your 8th semester marksheet has not been published yet."
        )

    # -----------------------------------------------------
    # Get semester 8 results
    # -----------------------------------------------------

    results = Result.objects.filter(
        student=student,
        semester=8
    )

    if not results.exists():
        reasons.append(
            "Your 8th semester results are not available yet."
        )
    else:

        # -------------------------------------------------
        # Check failed subjects
        # -------------------------------------------------

        failed_subjects = []

        for result in results:
            if result.grade() == 'F':
                failed_subjects.append(
                    result.subject_name
                )

        if failed_subjects:
            reasons.append(
                "You have failed subject(s) in the 8th semester."
            )

    return len(reasons) == 0, reasons


# =========================================================
# DEGREE CLEARANCE HOME
# =========================================================

@login_required
def degree_clearance(request):

    student = request.user.student_profile

    eligible, reasons = check_degree_clearance_eligibility(
        student
    )

    application = DegreeClearance.objects.filter(
        student=student
    ).first()

    return render(
        request,
        'degree_clearance/degree_clearance.html',
        {
            'student': student,
            'eligible': eligible,
            'reasons': reasons,
            'application': application,
        }
    )


# =========================================================
# APPLY FOR DEGREE CLEARANCE
# =========================================================

@login_required
def apply_degree_clearance(request):

    student = request.user.student_profile

    # -----------------------------------------------------
    # Check eligibility
    # -----------------------------------------------------

    eligible, reasons = check_degree_clearance_eligibility(
        student
    )

    if not eligible:

        return render(
            request,
            'degree_clearance/not_eligible.html',
            {
                'student': student,
                'reasons': reasons,
            }
        )

    # -----------------------------------------------------
    # Prevent duplicate application
    # -----------------------------------------------------

    existing_application = DegreeClearance.objects.filter(
        student=student
    ).first()

    if existing_application:

        messages.info(
            request,
            'You have already submitted a degree clearance application.'
        )

        return redirect(
            'degree_clearance:degree_clearance'
        )

    # -----------------------------------------------------
    # POST
    # -----------------------------------------------------

    if request.method == 'POST':

        form = DegreeClearanceForm(
            request.POST
        )

        if form.is_valid():

            application = form.save(
                commit=False
            )

            application.student = student
            application.status = 'PENDING'

            application.save()

            messages.success(
                request,
                (
                    'Your degree clearance application has '
                    'been submitted successfully.'
                )
            )

            return redirect(
                'degree_clearance:degree_clearance'
            )

    else:

        form = DegreeClearanceForm()

    return render(
        request,
        'degree_clearance/apply.html',
        {
            'student': student,
            'form': form,
        }
    )


# =========================================================
# DEGREE CLEARANCE DETAIL
# =========================================================

@login_required
def degree_clearance_detail(request, application_id):

    student = request.user.student_profile

    application = get_object_or_404(
        DegreeClearance,
        id=application_id,
        student=student
    )

    return render(
        request,
        'degree_clearance/detail.html',
        {
            'student': student,
            'application': application,
        }
    )