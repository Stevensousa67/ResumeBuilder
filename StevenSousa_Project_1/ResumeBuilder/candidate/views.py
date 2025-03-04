from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from formtools.wizard.views import SessionWizardView
from .forms import SignupForm, CandidateForm, ReferenceFormSet, ProjectFormSet, ExperienceFormSet
from .models import Candidate, Experience, Project, Reference
from django.contrib.auth.views import LoginView


# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'candidate/login.html'

    def get_success_url(self):
        user = self.request.user
        try:
            candidate = Candidate.objects.get(user=user)
            if not candidate.first_name:
                return reverse('candidate:edit_user')
            return reverse('jobs:jobs_list')
        except Candidate.DoesNotExist:
            return reverse('candidate:edit_user')


# Signup View
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=email, email=email, password=password)
            candidate = Candidate(user=user, email=email)
            candidate.save()
            login(request, user)
            return redirect('candidate:edit_user')
    else:
        form = SignupForm()
    return render(request, 'candidate/signup.html', {'form': form})


# Custom Logout View (Optional)
def logout_view(request):
    logout(request)
    return redirect('jobs:index')


# Edit User Wizard
class EditUserWizard(SessionWizardView):
    form_list = [
        ('candidate', CandidateForm),
        ('experience', ExperienceFormSet),
        ('projects', ProjectFormSet),
        ('references', ReferenceFormSet),
    ]
    template_name = 'candidate/edit_user.html'

    def get_form_prefix(self, step, form=None):
        prefixes = {
            'candidate': 'candidate',
            'experience': 'experiences',
            'projects': 'projects',
            'references': 'references',
        }
        return prefixes[step]

    def get_form_instance(self, step):
        if step == 'candidate':
            try:
                return Candidate.objects.get(user=self.request.user)
            except Candidate.DoesNotExist:
                return None
        return None  # Formsets don’t need instance here; handled in get_form

    def get_form_initial(self, step):
        if step == 'candidate':
            try:
                candidate = Candidate.objects.get(user=self.request.user)
                return {
                    'first_name': candidate.first_name,
                    'last_name': candidate.last_name,
                    'email': candidate.email,
                    'phone': candidate.phone,
                    'website': candidate.website,
                    'address': candidate.address,
                    'education': candidate.education,
                    'major': candidate.major,
                    'skills': candidate.skills,
                    'courses': candidate.courses,
                }
            except Candidate.DoesNotExist:
                return {}
        return None  # No initial data needed for formsets; instances handle it

    def get_form(self, step=None, data=None, files=None):
        if step is None:
            step = self.steps.current

        # Get the base form or formset
        form = super().get_form(step, data, files)

        # Handle formsets
        if step in ['experience', 'projects', 'references']:
            try:
                candidate = Candidate.objects.get(user=self.request.user)
                if step == 'experience':
                    return ExperienceFormSet(data=data, files=files, instance=candidate, prefix='experiences')
                elif step == 'projects':
                    return ProjectFormSet(data=data, files=files, instance=candidate, prefix='projects')
                elif step == 'references':
                    return ReferenceFormSet(data=data, files=files, instance=candidate, prefix='references')
            except Candidate.DoesNotExist:
                # If no Candidate exists yet, return an empty formset (extra=0 means no forms)
                if step == 'experience':
                    return ExperienceFormSet(data=data, files=files, prefix='experiences')
                elif step == 'projects':
                    return ProjectFormSet(data=data, files=files, prefix='projects')
                elif step == 'references':
                    return ReferenceFormSet(data=data, files=files, prefix='references')

        return form

    def get_form_kwargs(self, step):
        kwargs = super().get_form_kwargs(step)
        if step in ['experience', 'projects', 'references']:
            try:
                candidate = Candidate.objects.get(user=self.request.user)
                if step == 'experience':
                    kwargs['queryset'] = Experience.objects.filter(candidate=candidate)
                elif step == 'projects':
                    kwargs['queryset'] = Project.objects.filter(candidate=candidate)
                elif step == 'references':
                    kwargs['queryset'] = Reference.objects.filter(candidate=candidate)
            except Candidate.DoesNotExist:
                kwargs['queryset'] = [].none()  # Empty queryset if no Candidate
        return kwargs

    def done(self, form_list, form_dict, **kwargs):
        candidate_form = form_dict['candidate']
        formsets = {
            'experience': form_dict['experience'],
            'projects': form_dict['projects'],
            'references': form_dict['references'],
        }

        # Save or update Candidate
        candidate = candidate_form.save(commit=False)
        candidate.user = self.request.user
        candidate.email = self.request.user.email
        candidate.save()

        def save_formset_items(formset, candidate):
            for form in formset:
                if form.has_changed():
                    if form.cleaned_data.get('DELETE', False) and form.instance.pk:
                        form.instance.delete()
                    else:
                        item = form.save(commit=False)
                        item.candidate = candidate
                        item.save()

        for formset in formsets.values():
            save_formset_items(formset, candidate)

        messages.success(self.request, "Profile updated successfully!")
        return HttpResponseRedirect(reverse('jobs:jobs_list'))

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context['step_name'] = self.steps.current
        return context


edit_user = login_required(EditUserWizard.as_view())
