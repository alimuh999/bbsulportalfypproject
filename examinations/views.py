from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone

from .models import ExamForm, ExamFormSubject
from .forms import ExamFormCreateForm
from academics.models import Result


@login_required
def exam_form_list(request):

    student = request.user.student_profile

    exam_forms = ExamForm.objects.filter(
        student=student
    ).order_by('-created_at')

    return render(
        request,
        'examinations/exam_form_list.html',
        {
            'student': student,
            'exam_forms': exam_forms,
        }
    )


@login_required
def create_exam_form(request):

    student = request.user.student_profile

    if request.method == 'POST':

        form = ExamFormCreateForm(request.POST)

        if form.is_valid():

            exam_form = form.save(commit=False)
            exam_form.student = student
            exam_form.status = 'DRAFT'
            exam_form.save()

            return redirect(
                'examinations:select_subjects',
                exam_form_id=exam_form.id
            )

    else:
        form = ExamFormCreateForm(
            initial={
                'semester': student.semester
            }
        )

    return render(
        request,
        'examinations/create_exam_form.html',
        {
            'student': student,
            'form': form,
        }
    )


@login_required
def select_subjects(request, exam_form_id):

    student = request.user.student_profile

    exam_form = get_object_or_404(
        ExamForm,
        id=exam_form_id,
        student=student
    )

    if exam_form.status not in ['DRAFT', 'REJECTED']:
        return HttpResponse(
            'This exam form cannot be edited.',
            status=403
        )

    results = Result.objects.filter(
        student=student,
        semester=exam_form.semester
    ).order_by('subject_code')

    if request.method == 'POST':

        selected_result_ids = request.POST.getlist(
            'selected_subjects'
        )

        if not selected_result_ids:
            return render(
                request,
                'examinations/select_subjects.html',
                {
                    'student': student,
                    'exam_form': exam_form,
                    'results': results,
                    'error': 'Please select at least one subject.'
                }
            )

        ExamFormSubject.objects.filter(
            exam_form=exam_form
        ).delete()

        for result_id in selected_result_ids:

            result = results.filter(
                id=result_id
            ).first()

            if result:
                ExamFormSubject.objects.create(
                    exam_form=exam_form,
                    result=result
                )

        exam_form.status = 'SUBMITTED'
        exam_form.submitted_at = timezone.now()
        exam_form.save()

        return redirect(
            'examinations:exam_form_detail',
            exam_form_id=exam_form.id
        )

    return render(
        request,
        'examinations/select_subjects.html',
        {
            'student': student,
            'exam_form': exam_form,
            'results': results,
        }
    )


@login_required
def exam_form_detail(request, exam_form_id):

    student = request.user.student_profile

    exam_form = get_object_or_404(
        ExamForm,
        id=exam_form_id,
        student=student
    )

    return render(
        request,
        'examinations/exam_form_detail.html',
        {
            'student': student,
            'exam_form': exam_form,
        }
    )