from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .managers import CurrentTimePeriodManager, CurrentAndPastTimePeriodManager


class TimePeriodBase(models.Model):
    objects = models.Manager()
    current = CurrentTimePeriodManager()
    current_and_past = CurrentAndPastTimePeriodManager()
    name = models.CharField(max_length=100, blank=False, unique=True,
                            help_text=_('The name of this time period'))
    period_start = models.DateTimeField(blank=False, null=False)
    period_end = models.DateTimeField(blank=False, null=True)

    class Meta:
        abstract = True
        unique_together = ('period_start', 'period_end',)
        ordering = ('-period_start',)

    def __unicode__(self):
        return self.name

    def clean(self, *args, **kwargs):
        super(TimePeriodBase, self).clean(*args, **kwargs)
        cls = self.__class__

        if self.period_end <= self.period_start:
            raise ValidationError(
                _('period_end needs to be after period_start')
            )

        # Don't overlap single dates with another period
        for period in ('period_start', 'period_end'):
            datetime_ = getattr(self, period)
            q = cls.objects.extra(
                where=['%s BETWEEN period_start AND period_end'],
                params=[datetime_]
            )
            if self.pk: q = q.exclude(pk=self.pk)

            if q.exists():
                raise ValidationError(
                    _('{0} already in another period.'.format(period))
                )

        # A period shall not encompass his neighbours period
        q = cls.objects.extra(
            where=['((period_start BETWEEN %s AND %s) '
                   ' OR (period_end BETWEEN %s AND %s))'],
            params=[self.period_start, self.period_end,
                    self.period_start, self.period_end]
        )
        if self.pk: q = q.exclude(pk=self.pk)

        if(q.exists()):
            raise ValidationError(_('This period encompass another period.'))

    @classmethod
    def past_periods(cls):
        try:
            current = cls.current.get().period_start
        except cls.DoesNotExist:
            # When there is no current time periods at all, just
            # anything before now
            current = timezone.now()

        return cls.objects.filter(period_start__lt=current)


class TimePeriod(TimePeriodBase):
    pass
