from django import forms
from .models import User, Profile, Reference, Project, Experience


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


# User Form
class UserForm(forms.ModelForm):
    class Meta:
        model = User
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


# Profile Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_name']
        widgets = {
            'profile_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProfileSelectForm(forms.Form):
    profile_option = forms.ChoiceField(
        choices=[('existing', 'Select Existing Profile'), ('new', 'Create New Profile')],
        widget=forms.RadioSelect,
        initial='existing'
    )
    existing_profile = forms.ModelChoiceField(
        queryset=Profile.objects.none(),  # This is dynamically updated based on user
        widget=forms.Select,
        required=False,
        empty_label="Choose an existing profile"
    )
    new_profile_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter a new profile name'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['existing_profile'].queryset = Profile.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        profile_option = cleaned_data.get('profile_option')
        existing_profile = cleaned_data.get('existing_profile')
        new_profile_name = cleaned_data.get('new_profile_name')

        if profile_option == 'existing' and not existing_profile:
            raise forms.ValidationError("You must select an existing profile.")
        elif profile_option == 'new' and not new_profile_name:
            raise forms.ValidationError("You must enter a new profile name.")

        return cleaned_data


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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pass current user from view
        super().__init__(*args, **kwargs)
        if user:
            self.fields['profile'].queryset = Profile.objects.filter(user=user)  # Limit to user's profiles

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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['profile'].queryset = Profile.objects.filter(user=user)


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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['profile'].queryset = Profile.objects.filter(user=user)

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
    Profile,
    Experience,
    form=ExperienceForm,
    fields=['title', 'company', 'start_date', 'end_date', 'description', 'present'],
    extra=0,
    can_delete=True
)
ProjectFormSet = forms.inlineformset_factory(
    Profile,
    Project,
    form=ProjectForm,
    fields=['title', 'description'],
    extra=0,
    can_delete=True
)
ReferenceFormSet = forms.inlineformset_factory(
    Profile,
    Reference,
    form=ReferenceForm,
    fields=['first_name', 'last_name', 'phone', 'email', 'relationship'],
    extra=0,
    can_delete=True
)
