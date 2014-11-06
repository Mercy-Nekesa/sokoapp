from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render, render_to_response, get_object_or_404
from django.utils import timezone

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.views.generic import TemplateView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin

from .models import Sweep, SweepEntry
from .forms import SweepEntryForm


class SweepEntryDetail(SingleObjectMixin, FormView):
    """
    Display the form to enter the sweeps by creating a SweepEntry instance.
    """

    form_class = SweepEntryForm
    template_name = 'vodkamartinisweeps/sweepentry_form.html'
    queryset = Sweep.live.all()

    def get_initial(self):
        self.object = self.get_object()
        email = self.request.GET.get('email', '')
        email = email.replace('%40', '@')
        return {'email': email, 
                'sweep': self.object,
               }

    def form_valid(self, form):
        #messages.info(self.request, 'Thank you for participating.')
        sweepentry = form.save()
        self.success_url = reverse('vodkamartinisweeps_sweepentry_submitted', kwargs={'slug': self.object.slug})
        return super(SweepEntryDetail, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Populate the context.
        Most of these details are initialized on self.get_initial
        """
        context = super(SweepEntryDetail, self).get_context_data(**kwargs)
        context['sweep'] = self.object
        if self.object.closed:
            now = timezone.now()
            context['is_sweep_closed'] = self.object.closed < now
        return context

class SweepEntrySubmitted(TemplateView):
    """
    The thank you page after submitting the form for the sweeps.
    """
    template_name = 'vodkamartinisweeps/sweepentry_submitted.html'
