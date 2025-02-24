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
        return HttpResponseRedirect(reverse('jobs:jobs_list'))

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context['step_name'] = self.steps.current
        return context
