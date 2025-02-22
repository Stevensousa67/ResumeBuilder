from django import forms
from .models import Candidate, Reference, Project, Experience

# Candidate Form
class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'education', 'major', 'minor', 'gpa',
                  'skills', 'courses']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'education': forms.Select(attrs={'class': 'form-select'}),
            'major': forms.TextInput(attrs={'class': 'form-control'}),
            'minor': forms.TextInput(attrs={'class': 'form-control'}),
            'gpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '4.0'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'courses': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
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
