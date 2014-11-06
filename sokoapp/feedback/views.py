from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from feedback.forms import FeedbackForm
from feedback.models import Feedback

def feedback(request):
	"""
	Add feedback
	"""
	
	if request.method == 'POST':
		
		form = FeedbackForm(request.POST)
		if form.is_valid():
			
			new_fb = form.save(commit=False)
			new_fb.user_agent = request.META['HTTP_USER_AGENT']
			new_fb.save()

			#admin = User.objects.filter(pk=settings.ADMINS)

			# Send an email to the admin letting them know that feedback was submitted
			subject = render_to_string('feedback/email_subject.txt')
			message = render_to_string('feedback/email_body.txt',
									   { 'feedback': form.cleaned_data['feedback'], 'user_agent':request.META['HTTP_USER_AGENT']})
			recipients = [settings.ADMINS]
			send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients)

			return HttpResponseRedirect('/feedback-thanks/')
	
	else:
		
		form = FeedbackForm()

	return render_to_response('feedback/feedback_form.html', {
		'form':form,
	}, context_instance=RequestContext(request))