from django import forms
from django.utils import timezone
from django.core.validators import validate_email
from .models import Sweep, SweepEntry

class SweepEntryForm(forms.Form):

    email = forms.CharField(required=True)
    date_of_birth = forms.DateField(required=True, widget=forms.TextInput(attrs={'placeholder': 'mm/dd/yyyy'}))
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    gender = forms.ChoiceField(choices=[(0, 'Choose your gender')] + SweepEntry.GENDER_CHOICES)
    zip_code = forms.CharField(max_length=10, required=True)
    receive_email = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        """
        Notice how we need to call __init__ from superclass first, if we don't do this
        then we won't be able to access attributes such as fields and instance.
        """
        super(SweepEntryForm, self).__init__(*args, **kwargs)
        if self.initial:
            self.sweep = self.initial['sweep']

    def save(self):
        sweepentry = SweepEntry(
                        sweep=self.sweep,
                        first_name=self.cleaned_data['first_name'],
                        last_name=self.cleaned_data['last_name'],
                        email=self.cleaned_data['email'],
                        date_of_birth=self.cleaned_data['date_of_birth'],
                        zip_code=self.cleaned_data['zip_code'],
                        gender=self.cleaned_data['gender'],
                        receive_email=self.cleaned_data['receive_email'],
                     )

        sweepentry.save()
        return sweepentry

    def clean_gender(self):
        value = self.cleaned_data["gender"]
        if value == '0':
            raise forms.ValidationError("Please choose your gender")
        return value

    def clean(self):
        today = timezone.now()
        cleaned_data = super(SweepEntryForm, self).clean()
        if 'email' in cleaned_data:
            validate_email(cleaned_data['email'])
            sweepentries = SweepEntry.objects.filter(
                                                        email=cleaned_data['email'],
                                                        created__day=today.day, 
                                                        created__month=today.month, 
                                                        created__year=today.year
                                                    )

            if sweepentries.count():
                raise forms.ValidationError("You have already participated today, please come back tomorrow for another choice to win.")
        return cleaned_data
