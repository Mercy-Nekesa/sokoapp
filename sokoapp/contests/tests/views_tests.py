import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from test_app.models import TimePeriod


class TimePeriodMixin(TestCase):
    def setUp(self):
        self.url = reverse('test:time-period')

    def test_when_no_time_period_in_db_should_return_false(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)
        self.assertIn('time_period', res.context)
        self.assertFalse(res.context['time_period'])

    def test_when_no_active_time_period_should_return_false(self):
        TimePeriod.objects.create(
            name="Shouldn't be seen",
            period_start=timezone.now() - datetime.timedelta(days=14),
            period_end=timezone.now() - datetime.timedelta(days=1),
        )

        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)
        self.assertIn('time_period', res.context)
        self.assertFalse(res.context['time_period'])

    def test_when_active_time_period_should_return_it(self):
        time_period = TimePeriod.objects.create(
            name='Test period',
            period_start=timezone.now(),
            period_end=timezone.now() + datetime.timedelta(days=14)
        )

        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)
        self.assertIn('time_period', res.context)
        self.assertTrue(res.context['time_period'])
        self.assertEqual(res.context['time_period'].pk, time_period.pk)
