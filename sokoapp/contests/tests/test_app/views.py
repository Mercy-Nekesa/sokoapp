from django.views.generic import TemplateView

from .models import TimePeriod
from referee.views import TimePeriodMixin


class TimePeriodView(TimePeriodMixin, TemplateView):
    template_name = 'empty.html'
