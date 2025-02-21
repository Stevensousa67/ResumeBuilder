# candidate/views.py
from django.shortcuts import render, redirect
from django.forms import formset_factory
from .forms import CandidateForm, ReferenceForm, ProjectForm, ExperienceForm, ClassesForm
from .models import Candidate


def signup(request):
    ReferenceFormSet = formset_factory(ReferenceForm, extra=1)
    ProjectFormSet = formset_factory(ProjectForm, extra=1)
    ExperienceFormSet = formset_factory(ExperienceForm, extra=1)  # Add Experience formset
    ClassesFormSet = formset_factory(ClassesForm, extra=1)

    if request.method == 'POST':
        candidate_form = CandidateForm(request.POST)
        reference_formset = ReferenceFormSet(request.POST, prefix='references')
        project_formset = ProjectFormSet(request.POST, prefix='projects')
        experience_formset = ExperienceFormSet(request.POST, prefix='experiences')
        classes_formset = ClassesFormSet(request.POST, prefix='classes')

        if (candidate_form.is_valid() and
                reference_formset.is_valid() and
                project_formset.is_valid() and
                experience_formset.is_valid() and
                classes_formset.is_valid()):

            candidate = candidate_form.save()

            for reference_form in reference_formset:
                if reference_form.cleaned_data:
                    reference = reference_form.save(commit=False)
                    reference.candidate = candidate
                    reference.save()

            for project_form in project_formset:
                if project_form.cleaned_data:
                    project = project_form.save(commit=False)
                    project.candidate = candidate
                    project.save()

            for experience_form in experience_formset:
                if experience_form.cleaned_data:
                    experience = experience_form.save(commit=False)
                    experience.candidate = candidate
                    experience.save()

            for classes_form in classes_formset:
                if classes_form.cleaned_data:
                    classes = classes_form.save(commit=False)
                    classes.candidate = candidate
                    classes.save()

            return redirect('job_list')

    else:
        candidate_form = CandidateForm()
        reference_formset = ReferenceFormSet(prefix='references')
        project_formset = ProjectFormSet(prefix='projects')
        experience_formset = ExperienceFormSet(prefix='experiences')
        classes_formset = ClassesFormSet(prefix='classes')

    context = {
        'candidate_form': candidate_form,
        'reference_formset': reference_formset,
        'project_formset': project_formset,
        'experience_formset': experience_formset,
        'classes_formset': classes_formset,
    }
    return render(request, 'candidate/signup.html', context)