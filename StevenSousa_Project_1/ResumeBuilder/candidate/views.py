from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from formtools.wizard.views import SessionWizardView
from .forms import CandidateForm, ReferenceFormSet, ProjectFormSet, ExperienceFormSet
from .models import Candidate

class SignupWizard(SessionWizardView):
    form_list = [
        ('candidate', CandidateForm),
        ('experience', ExperienceFormSet),
        ('projects', ProjectFormSet),
        ('references', ReferenceFormSet),
    ]
    template_name = 'candidate/signup.html'

    def get_form_prefix(self, step, form=None):  # Add form=None to accept the extra argument
        prefixes = {
            'candidate': 'candidate',
            'experience': 'experiences',
            'projects': 'projects',
            'references': 'references',
        }
        return prefixes[step]

    def done(self, form_list, form_dict, **kwargs):
        candidate_form = form_dict['candidate']
        experience_formset = form_dict['experience']
        project_formset = form_dict['projects']
        reference_formset = form_dict['references']

        candidate = candidate_form.save()

        for experience_form in experience_formset:
            if experience_form.has_changed() and not experience_form.cleaned_data.get('DELETE', False):
                experience = experience_form.save(commit=False)
                experience.candidate = candidate
                experience.save()

        for project_form in project_formset:
            if project_form.has_changed() and not project_form.cleaned_data.get('DELETE', False):
                project = project_form.save(commit=False)
                project.candidate = candidate
                project.save()

        for reference_form in reference_formset:
            if reference_form.has_changed() and not reference_form.cleaned_data.get('DELETE', False):
                reference = reference_form.save(commit=False)
                reference.candidate = candidate
                reference.save()

        messages.success(self.request, "Signup successful! Your profile has been created.")
        return HttpResponseRedirect(reverse('jobs:index'))

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context['step_name'] = self.steps.current
        return context

# def signup(request):
#     ReferenceFormSet = formset_factory(ReferenceForm, extra=1)
#     ProjectFormSet = formset_factory(ProjectForm, extra=1)
#     ExperienceFormSet = formset_factory(ExperienceForm, extra=1)
#
#     if request.method == 'POST':
#         candidate_form = CandidateForm(request.POST)
#         reference_formset = ReferenceFormSet(request.POST, prefix='references')
#         project_formset = ProjectFormSet(request.POST, prefix='projects')
#         experience_formset = ExperienceFormSet(request.POST, prefix='experiences')
#
#         # Debugging: Print POST data and formset counts
#         print("POST Data:", request.POST)
#         print("Experience TOTAL_FORMS:", request.POST.get('experiences-TOTAL_FORMS'))
#         print("Project TOTAL_FORMS:", request.POST.get('projects-TOTAL_FORMS'))
#         print("Reference TOTAL_FORMS:", request.POST.get('references-TOTAL_FORMS'))
#
#         if (candidate_form.is_valid() and
#                 reference_formset.is_valid() and
#                 project_formset.is_valid() and
#                 experience_formset.is_valid()):
#
#             candidate = candidate_form.save()
#
#             # Save references
#             for reference_form in reference_formset:
#                 if reference_form.has_changed():  # Check if form has been modified
#                     reference = reference_form.save(commit=False)
#                     reference.candidate = candidate
#                     reference.save()
#
#             # Save projects
#             for project_form in project_formset:
#                 if project_form.has_changed():
#                     project = project_form.save(commit=False)
#                     project.candidate = candidate
#                     project.save()
#
#             # Save experiences
#             for experience_form in experience_formset:
#                 if experience_form.has_changed():
#                     experience = experience_form.save(commit=False)
#                     experience.candidate = candidate
#                     experience.save()
#
#             messages.success(request, "Signup successful! Your profile has been created.")
#             return redirect('jobs:index')
#         else:
#             # Log errors for debugging
#             print("Candidate Errors:", candidate_form.errors)
#             print("Reference Errors:", reference_formset.errors)
#             print("Project Errors:", project_formset.errors)
#             print("Experience Errors:", experience_formset.errors)
#             messages.error(request, "There was an error in your submission. Please check the form and try again.")
#
#     else:
#         candidate_form = CandidateForm()
#         reference_formset = ReferenceFormSet(prefix='references')
#         project_formset = ProjectFormSet(prefix='projects')
#         experience_formset = ExperienceFormSet(prefix='experiences')
#
#     context = {
#         'candidate_form': candidate_form,
#         'reference_formset': reference_formset,
#         'project_formset': project_formset,
#         'experience_formset': experience_formset,
#     }
#     return render(request, 'candidate/signup.html', context)
