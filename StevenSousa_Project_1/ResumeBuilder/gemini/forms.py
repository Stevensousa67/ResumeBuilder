from django import forms
from candidate.models import Profile


class ProfileSelectionForm(forms.Form):
    profile = forms.ModelChoiceField(
        queryset=None,
        empty_label=None,
        widget=forms.RadioSelect,
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter profiles to those owned by the current user
        self.fields['profile'].queryset = Profile.objects.filter(user=user)

        # If no profiles exist, provide helpful message
        if not self.fields['profile'].queryset.exists():
            self.fields['profile'].help_text = "You have not created any profiles yet. Please create a new profile."
