from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import LeaveRequest
from .forms import LeaveRequestForm


@login_required
def leave_request_list(request):

    student = request.user.student_profile

    leave_requests = LeaveRequest.objects.filter(
        student=student
    ).order_by('-submitted_at')

    return render(
        request,
        'leaves/leave_request_list.html',
        {
            'student': student,
            'leave_requests': leave_requests,
        }
    )


@login_required
def create_leave_request(request):

    student = request.user.student_profile

    if request.method == 'POST':

        form = LeaveRequestForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            leave_request = form.save(commit=False)
            leave_request.student = student
            leave_request.status = 'PENDING'
            leave_request.save()

            return redirect(
                'leaves:leave_request_list'
            )

    else:
        form = LeaveRequestForm()

    return render(
        request,
        'leaves/create_leave_request.html',
        {
            'student': student,
            'form': form,
        }
    )


@login_required
def leave_request_detail(request, leave_id):

    student = request.user.student_profile

    leave_request = get_object_or_404(
        LeaveRequest,
        id=leave_id,
        student=student
    )

    return render(
        request,
        'leaves/leave_request_detail.html',
        {
            'student': student,
            'leave_request': leave_request,
        }
    )