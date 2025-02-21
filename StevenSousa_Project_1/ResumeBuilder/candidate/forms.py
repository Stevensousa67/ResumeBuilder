from django import forms
from .models import Candidate, Reference, Project, Experience, Classes

# Candidate Form
class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'education', 'major', 'minor', 'gpa', 'skills']
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
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '').isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone

    def clean_email(self):
        email = self.cleaned_data['email']
        if '@' not in email:
            raise forms.ValidationError("Email must contain an '@' symbol.")
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
            'relationship': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '').isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone

    def clean_email(self):
        email = self.cleaned_data['email']
        if '@' not in email:
            raise forms.ValidationError("Email must contain an '@' symbol.")
        return email.lower()

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
    class Meta:
        model = Experience
        fields = ['title', 'company', 'start_date', 'end_date', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# Classes Form
class ClassesForm(forms.ModelForm):
    class Meta:
        model = Classes
        fields = ['class_name']
        widgets = {
            'class_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
