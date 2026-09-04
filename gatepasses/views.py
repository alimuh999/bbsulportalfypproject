from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .models import GatePass
from .forms import GatePassForm


@login_required
def gate_pass_list(request):
    student = request.user.student_profile

    # Gate Pass sirf female students ke liye
    if student.gender != 'Female':
        return redirect('dashboard')

    gate_passes = GatePass.objects.filter(
        student=student
    ).order_by('-created_at')

    return render(request, 'gatepasses/gate_pass_list.html', {
        'student': student,
        'gate_passes': gate_passes,
    })


@login_required
def create_gate_pass(request):
    student = request.user.student_profile

    # Boys Gate Pass create nahi kar sakte
    if student.gender != 'Female':
        return redirect('dashboard')

    if request.method == 'POST':
        form = GatePassForm(request.POST)

        if form.is_valid():
            gate_pass = form.save(commit=False)
            gate_pass.student = student
            gate_pass.status = 'PENDING'
            gate_pass.save()

            return redirect('gatepasses:gate_pass_list')

    else:
        form = GatePassForm()

    return render(request, 'gatepasses/create_gate_pass.html', {
        'student': student,
        'form': form,
    })


@login_required
def gate_pass_detail(request, gate_pass_id):
    student = request.user.student_profile

    # Boys direct URL se bhi access nahi kar sakte
    if student.gender != 'Female':
        return redirect('dashboard')

    gate_pass = get_object_or_404(
        GatePass,
        id=gate_pass_id,
        student=student
    )

    return render(request, 'gatepasses/gate_pass_detail.html', {
        'student': student,
        'gate_pass': gate_pass,
    })


@login_required
def download_gate_pass_pdf(request, gate_pass_id):
    student = request.user.student_profile

    # PDF sirf female students ke liye
    if student.gender != 'Female':
        return redirect('dashboard')

    gate_pass = get_object_or_404(
        GatePass,
        id=gate_pass_id,
        student=student
    )

    # Sirf approved gate pass ka PDF download hoga
    if gate_pass.status != 'APPROVED':
        return redirect(
            'gatepasses:gate_pass_detail',
            gate_pass_id=gate_pass.id
        )

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = (
        f'attachment; filename="gate_pass_{gate_pass.id}.pdf"'
    )

    pdf = canvas.Canvas(response, pagesize=A4)

    width, height = A4

    # Main heading
    pdf.setFont('Helvetica-Bold', 20)
    pdf.drawCentredString(
        width / 2,
        height - 70,
        'UNIVERSITY GATE PASS'
    )

    pdf.setFont('Helvetica', 11)
    pdf.drawCentredString(
        width / 2,
        height - 95,
        'Official Student Gate Pass'
    )

    pdf.line(50, height - 115, width - 50, height - 115)

    # Student Information
    y = height - 160

    pdf.setFont('Helvetica-Bold', 13)
    pdf.drawString(60, y, 'Student Information')

    y -= 30
    pdf.setFont('Helvetica', 11)

    pdf.drawString(
        60,
        y,
        f'Student Name: {student.user.get_full_name()}'
    )

    y -= 22

    pdf.drawString(
        60,
        y,
        f'Student ID: {student.student_id}'
    )

    y -= 22

    pdf.drawString(
        60,
        y,
        f'Registration No: {student.registration_no}'
    )

    y -= 22

    pdf.drawString(
        60,
        y,
        f'Department: {student.department}'
    )

    y -= 22

    pdf.drawString(
        60,
        y,
        f'Program: {student.program}'
    )

    y -= 45

    # Gate Pass Details
    pdf.setFont('Helvetica-Bold', 13)
    pdf.drawString(60, y, 'Gate Pass Details')

    y -= 30
    pdf.setFont('Helvetica', 11)

    pdf.drawString(
        60,
        y,
        f'Reason: {gate_pass.reason}'
    )

    y -= 22

    pdf.drawString(
        60,
        y,
        f'Departure Date: {gate_pass.departure_date}'
    )

    y -= 22

    pdf.drawString(
        60,
        y,
        f'Departure Time: {gate_pass.departure_time}'
    )

    y -= 22

    pdf.drawString(
        60,
        y,
        f'Return Date: {gate_pass.return_date}'
    )

    y -= 22

    pdf.drawString(
        60,
        y,
        f'Return Time: {gate_pass.return_time}'
    )

    y -= 22

    pdf.drawString(
        60,
        y,
        'Status: APPROVED'
    )

    y -= 60

    # Signature lines
    pdf.line(60, y, 220, y)
    pdf.drawString(60, y - 20, 'Student Signature')

    pdf.line(width - 220, y, width - 60, y)
    pdf.drawString(width - 220, y - 20, 'Authorized Signature')

    y -= 80

    pdf.setFont('Helvetica-Oblique', 9)
    pdf.drawCentredString(
        width / 2,
        y,
        'This gate pass is valid only for the dates and times mentioned above.'
    )

    pdf.save()

    return response