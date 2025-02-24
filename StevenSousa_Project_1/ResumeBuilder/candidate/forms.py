from django import forms
from django.contrib.auth.models import User
from .models import Candidate, Reference, Project, Experience


# Sign Up Form
class SignupForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                       label="Confirm Password")

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


# Candidate Form
class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['first_name', 'last_name', 'email', 'phone', 'website', 'address', 'education', 'major',
                  'skills', 'courses']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'education': forms.Select(attrs={'class': 'form-select'}),
            'major': forms.TextInput(attrs={'class': 'form-control'}),
            'courses': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '').isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone

    def clean_email(self):
        email = self.cleaned_data['email']
        return email.lower()


# Reference Form
class ReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = ['first_name', 'last_name', 'phone', 'email', 'relationship']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'relationship': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone and not phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '').isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone

    def clean_email(self):
        email = self.cleaned_data['email']
        return email.lower() if email else email


# Project Form
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# Experience Form
class ExperienceForm(forms.ModelForm):
    present = forms.BooleanField(
        required=False,
        label="I currently work here",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Experience
        fields = ['title', 'company', 'start_date', 'end_date', 'description', 'present']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        present = cleaned_data.get('present')

        if present and end_date:
            raise forms.ValidationError("You cannot have both an end date and mark the job as present.")

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date cannot be earlier than start date.")

        return cleaned_data


# Formsets
ExperienceFormSet = forms.inlineformset_factory(
    Candidate,
    Experience,
    form=ExperienceForm,
    fields=['title', 'company', 'start_date', 'end_date', 'description', 'present'],
    extra=1,
    can_delete=True
)
ProjectFormSet = forms.inlineformset_factory(
    Candidate,
    Project,
    form=ProjectForm,
    fields=['title', 'description'],
    extra=1,
    can_delete=True
)
ReferenceFormSet = forms.inlineformset_factory(
    Candidate,
    Reference,
    form=ReferenceForm,
    fields=['first_name', 'last_name', 'phone', 'email', 'relationship'],
    extra=1,
    can_delete=True
)
