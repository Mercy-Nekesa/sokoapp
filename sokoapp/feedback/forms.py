from django import forms
from django.forms import ModelForm
from feedback.models import Feedback

attrs_dict = {'class': 'required'}
        
class FeedbackForm(ModelForm):    
    class Meta:
        model = Feedback
        exclude = ('created', 'user_agent',)