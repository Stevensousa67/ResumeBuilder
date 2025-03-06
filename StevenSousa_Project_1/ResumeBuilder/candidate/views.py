from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from formtools.wizard.views import SessionWizardView
from django.forms.widgets import Select
from .forms import SignupForm, UserForm, ProfileForm, ExperienceFormSet, ProjectFormSet, ReferenceFormSet
from .models import User, Profile, Experience, Project, Reference
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist


# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'candidate/login.html'

    def get_success_url(self):
        user = self.request.user
        if not user.first_name:
            return reverse('candidate:edit_user')
        return reverse('jobs:jobs_list')


# Signup View
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=email, email=email, password=password)
            login(request, user)
            return redirect('candidate:edit_user')
    else:
        form = SignupForm()
    return render(request, 'candidate/signup.html', {'form': form})


# Custom Logout View
def logout_view(request):
    logout(request)
    return redirect('jobs:index')


# Profile Create View (kept for standalone use if needed)
@login_required
def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('candidate:edit_user')
    else:
        form = ProfileForm()
    return render(request, 'candidate/edit_user.html', {'form': form})


# Edit User and Profile Wizard
class EditUserWizard(SessionWizardView):
    form_list = [
        ('user', UserForm),
        ('profile_select', ProfileForm),
        ('experience', ExperienceFormSet),
        ('projects', ProjectFormSet),
        ('references', ReferenceFormSet),
    ]
    template_name = 'candidate/edit_user.html'

    def get_form_prefix(self, step, form=None):
        prefixes = {
            'user': 'user',
            'profile_select': 'profile_select',
            'experience': 'experiences',
            'projects': 'projects',
            'references': 'references',
        }
        return prefixes[step]

    def get_form_instance(self, step):
        if step == 'user':
            return self.request.user
        return None

    def get_form_initial(self, step):
        if step == 'user':
            user = self.request.user
            return {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': user.phone,
                'website': user.website,
                'address': user.address,
                'education': user.education,
                'major': user.major,
                'skills': user.skills,
                'courses': user.courses,
            }
        return None

    def _get_formset_class(self, step):
        formset_map = {
            'experience': ExperienceFormSet,
            'projects': ProjectFormSet,
            'references': ReferenceFormSet,
        }
        return formset_map.get(step)

    def _get_formset(self, step, data, files, profile=None):
        formset_class = self._get_formset_class(step)
        if not formset_class:
            return None
        prefix = step if step != 'experience' else 'experiences'
        kwargs = {'data': data, 'files': files, 'prefix': prefix}
        if profile:
            kwargs['instance'] = profile
        return formset_class(**kwargs)

    def get_form(self, step=None, data=None, files=None):
        step = step or self.steps.current
        if step == 'profile_select':
            profiles = Profile.objects.filter(user=self.request.user)
            choices = [(p.id, p.profile_name) for p in profiles]
            form = ProfileForm(data=data, files=files)
            form.fields['profile_name'].widget = Select(
                choices=choices,
                attrs={'class': 'form-control', 'id': 'profile_select_dropdown'}
            )
            form.fields['profile_name'].label = "Select Profile"
            if data and 'new_profile_name' in data and data['new_profile_name']:
                new_profile = Profile(user=self.request.user, profile_name=data['new_profile_name'])
                new_profile.save()
                choices.append((new_profile.id, new_profile.profile_name))
                form.fields['profile_name'].widget.choices = choices
                form.fields['profile_name'].initial = new_profile.id
            elif not profiles and not data:
                profile_count = Profile.objects.filter(user=self.request.user).count()
                default_name = f"Profile {profile_count + 1}"
                new_profile = Profile(user=self.request.user, profile_name=default_name)
                new_profile.save()
                choices.append((new_profile.id, new_profile.profile_name))
                form.fields['profile_name'].widget.choices = choices
                form.fields['profile_name'].initial = new_profile.id
            return form
        elif step in ['experience', 'projects', 'references']:
            profile_id = self.get_cleaned_data_for_step('profile_select')
            if profile_id and profile_id['profile_name']:
                profile = Profile.objects.get(id=profile_id['profile_name'], user=self.request.user)
                return self._get_formset(step, data, files, profile)
            return self._get_formset(step, data, files)
        return super().get_form(step, data, files)

    def get_form_kwargs(self, step):
        kwargs = super().get_form_kwargs(step)
        if step in ['experience', 'projects', 'references']:
            profile_id = self.get_cleaned_data_for_step('profile_select')
            if profile_id and profile_id['profile_name']:
                profile = Profile.objects.get(id=profile_id['profile_name'], user=self.request.user)
                if step == 'experience':
                    kwargs['queryset'] = Experience.objects.filter(profile=profile)
                elif step == 'projects':
                    kwargs['queryset'] = Project.objects.filter(profile=profile)
                elif step == 'references':
                    kwargs['queryset'] = Reference.objects.filter(profile=profile)
        return kwargs

    def done(self, form_list, form_dict, **kwargs):
        user_form = form_dict['user']
        profile_select = form_dict['profile_select']
        formsets = {
            'experience': form_dict['experience'],
            'projects': form_dict['projects'],
            'references': form_dict['references'],
        }

        # Save User
        user = user_form.save(commit=False)
        user.email = self.request.user.email
        user.save()

        # Profile is always selected or created
        profile_id = profile_select.cleaned_data['profile_name']
        profile = Profile.objects.get(id=profile_id, user=self.request.user)

        # Save Formsets
        def save_formset_items(formset, profile):
            for form in formset:
                if form.has_changed():
                    if form.cleaned_data.get('DELETE', False) and form.instance.pk:
                        form.instance.delete()
                    else:
                        item = form.save(commit=False)
                        item.profile = profile
                        item.save()

        for formset in formsets.values():
            save_formset_items(formset, profile)

        messages.success(self.request, "Profile updated successfully!")
        return HttpResponseRedirect(reverse('jobs:jobs_list'))  # Changed redirect here

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context['step_name'] = self.steps.current
        return context


edit_user = login_required(EditUserWizard.as_view())