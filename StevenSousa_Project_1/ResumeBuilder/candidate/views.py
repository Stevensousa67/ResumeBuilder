from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.contrib import messages
from .forms import CandidateForm, ReferenceForm, ProjectForm, ExperienceForm, CourseForm
from .models import Candidate


def signup(request):
    # Define formsets
    ReferenceFormSet = formset_factory(ReferenceForm, extra=0)
    ProjectFormSet = formset_factory(ProjectForm, extra=0)
    ExperienceFormSet = formset_factory(ExperienceForm, extra=0)
    CourseFormSet = formset_factory(CourseForm, extra=0)

    if request.method == 'POST':
        candidate_form = CandidateForm(request.POST)
        reference_formset = ReferenceFormSet(request.POST, prefix='references')
        project_formset = ProjectFormSet(request.POST, prefix='projects')
        experience_formset = ExperienceFormSet(request.POST, prefix='experiences')
        course_formset = CourseFormSet(request.POST, prefix='courses')

        # Validate all forms and formsets
        if (candidate_form.is_valid() and
                reference_formset.is_valid() and
                project_formset.is_valid() and
                experience_formset.is_valid() and
                course_formset.is_valid()):

            # Save the candidate
            candidate = candidate_form.save()

            # Save references
            for reference_form in reference_formset:
                if reference_form.cleaned_data:  # Check if form has data
                    reference = reference_form.save(commit=False)
                    reference.candidate = candidate
                    reference.save()

            # Save projects
            for project_form in project_formset:
                if project_form.cleaned_data:
                    project = project_form.save(commit=False)
                    project.candidate = candidate
                    project.save()

            # Save experiences
            for experience_form in experience_formset:
                if experience_form.cleaned_data:
                    experience = experience_form.save(commit=False)
                    experience.candidate = candidate
                    experience.save()

            # Save courses (fixed variable name)
            for course_form in course_formset:
                if course_form.cleaned_data:
                    course = course_form.save(commit=False)
                    course.candidate = candidate
                    course.save()

            # Success message (optional)
            messages.success(request, "Signup successful! Your profile has been created.")
            return redirect('job_list')
        else:
            # Error feedback
            messages.error(request, "There was an error in your submission. Please check the form and try again.")

    else:
        # Empty forms for GET request
        candidate_form = CandidateForm()
        reference_formset = ReferenceFormSet(prefix='references')
        project_formset = ProjectFormSet(prefix='projects')
        experience_formset = ExperienceFormSet(prefix='experiences')
        course_formset = CourseFormSet(prefix='courses')

    context = {
        'candidate_form': candidate_form,
        'reference_formset': reference_formset,
        'project_formset': project_formset,
        'experience_formset': experience_formset,
        'course_formset': course_formset,
    }
    return render(request, 'candidate/signup.html', context)