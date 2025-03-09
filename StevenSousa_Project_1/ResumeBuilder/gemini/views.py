from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.base import ContentFile
from django.db.models import Max
from .models import GeneratedResume, GeneratedCoverLetter
from .forms import ProfileSelectionForm
from .services.gemini_api import generate_content
from .services.pdf_service import convert_markdown_to_pdf
from jobs.models import Job


@login_required
def generate_resume(request, job_id):
    """View to select a profile and generate a resume for a specific job"""
    job = get_object_or_404(Job, pk=job_id)
    existing_resume = GeneratedResume.objects.filter(user=request.user, job=job).order_by('-created_date').first()

    if request.method == 'POST':
        form = ProfileSelectionForm(request.user, request.POST)
        if form.is_valid():
            profile = form.cleaned_data['profile']
            latest_version = \
                GeneratedResume.objects.filter(user=request.user, job=job, profile=profile).aggregate(Max('version'))[
                    'version__max'] or 0
            next_version = latest_version + 1

            try:
                markdown_content = generate_content(profile, job, content_type="resume")
                if markdown_content is None:
                    raise ValueError("Gemini API returned no content")
                pdf_content = convert_markdown_to_pdf(markdown_content)
                resume = GeneratedResume(user=request.user, job=job, profile=profile, version=next_version,
                                         content=markdown_content)
                filename = (f"{request.user.first_name} {request.user.last_name} Resume - {profile.profile_name} - "
                            f"v{next_version}.pdf")
                resume.pdf_file.save(filename, ContentFile(pdf_content))
                resume.save()
                messages.success(request, 'Resume successfully generated')
                return redirect('gemini:view_resume', pk=resume.pk)
            except Exception as e:
                messages.error(request, f'Error generating resume: {e}')
    else:
        form = ProfileSelectionForm(request.user)
    return render(request, 'gemini/generate_resume.html',
                  {'form': form, 'job': job, 'existing_resume': existing_resume})


@login_required
def view_resume(request, pk):
    """View a specific resume"""
    resume = get_object_or_404(GeneratedResume, pk=pk, user=request.user)
    job = resume.job
    if not job:
        messages.error(request, "Associated job not found for this resume.")
        return redirect('gemini:resume_list')

    if request.method == 'POST':
        resume.delete()
        messages.success(request, "Resume deleted successfully.")
        return redirect('gemini:resume_list')

    return render(request, 'gemini/view_resume.html', {'resume': resume, 'job': job})


@login_required
def resume_list(request):
    """List all resumes for the logged-in user"""
    resumes = GeneratedResume.objects.filter(user=request.user).order_by('-created_date')
    return render(request, 'gemini/resume_list.html', {'resumes': resumes})


@login_required
def generate_cover_letter(request, job_id):
    """View to select a profile and generate a cover letter for a specific job"""
    job = get_object_or_404(Job, pk=job_id)
    existing_cover_letter = GeneratedCoverLetter.objects.filter(user=request.user, job=job).order_by(
        '-created_date').first()

    if request.method == 'POST':
        form = ProfileSelectionForm(request.user, request.POST)
        if form.is_valid():
            profile = form.cleaned_data['profile']
            latest_version = \
                GeneratedCoverLetter.objects.filter(user=request.user, job=job, profile=profile).aggregate(
                    Max('version'))[
                    'version__max'] or 0
            next_version = latest_version + 1

            try:
                markdown_content = generate_content(profile, job, content_type="cover_letter")
                if markdown_content is None:
                    raise ValueError("Gemini API returned no content")
                pdf_content = convert_markdown_to_pdf(markdown_content)
                cover_letter = GeneratedCoverLetter(user=request.user, job=job, profile=profile, version=next_version,
                                                    content=markdown_content)
                filename = (
                    f"{request.user.first_name} {request.user.last_name} Cover Letter - {profile.profile_name} -"
                    f" v{next_version}.pdf")
                cover_letter.pdf_file.save(filename, ContentFile(pdf_content))
                cover_letter.save()
                messages.success(request, 'Cover letter successfully generated')
                return redirect('gemini:cover_letter_detail', pk=cover_letter.pk)
            except Exception as e:
                messages.error(request, f'Error generating cover letter: {e}')
    else:
        form = ProfileSelectionForm(request.user)
    return render(request, 'gemini/generate_cover_letter.html',
                  {'form': form, 'job': job, 'existing_cover_letter': existing_cover_letter})


@login_required
def view_cover_letter(request, pk):
    """View a specific cover letter"""
    cover_letter = get_object_or_404(GeneratedCoverLetter, pk=pk, user=request.user)
    job = cover_letter.job  # Explicitly retrieve the job to avoid potential issues
    if not job:
        messages.error(request, "Associated job not found for this cover letter.")
        return redirect('gemini:cover_letter_list')

    if request.method == 'POST':
        cover_letter.delete()
        messages.success(request, "Cover letter deleted successfully.")
        return redirect('gemini:cover_letter_list')

    return render(request, 'gemini/view_cover_letter.html', {'cover_letter': cover_letter, 'job': job})


@login_required
def cover_letter_list(request):
    """List all cover letters for the logged-in user"""
    cover_letters = GeneratedCoverLetter.objects.filter(user=request.user).order_by('-created_date')
    return render(request, 'gemini/cover_letter_list.html', {'cover_letters': cover_letters})
