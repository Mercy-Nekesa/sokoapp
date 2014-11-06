from django.db import models
from django.utils import timezone


class CurrentTimePeriodManager(models.Manager):
    def get_query_set(self, *args, **kwargs):
        now = timezone.now()

        return (super(CurrentTimePeriodManager, self)
                .get_query_set(*args, **kwargs)
                .extra(
                    where=['(%s BETWEEN period_start AND period_end) '
                           'OR (%s >= period_start AND period_end IS NULL)'],
                    params=[now, now]
                ))


class CurrentAndPastTimePeriodManager(models.Manager):
    def get_query_set(self, *args, **kwargs):
        now = timezone.now()

        return (super(CurrentAndPastTimePeriodManager, self)
                .get_query_set(*args, **kwargs)
                .filter(period_start__lte=now)
                .order_by('period_start'))
