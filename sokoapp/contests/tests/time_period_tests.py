import datetime

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from mock import Mock, patch

from .factories import TimePeriodFactory
from test_app.models import TimePeriod


class TimePeriodTest(TestCase):
    def test_should_create_several_periods_without_a_problem(self):
        TimePeriodFactory.create()
        TimePeriodFactory.create()

    def test_period_end_needs_to_be_after_period_start(self):
        period = TimePeriodFactory.build()

        period.period_end = period.period_start
        with self.assertRaises(ValidationError):
            period.full_clean()

        period.period_end = period.period_start - datetime.timedelta(days=1)
        with self.assertRaises(ValidationError) as e:
            period.full_clean()
            self.assertTrue('period_end needs to be after' in str(e.exception))

    def test_same_period_should_not_work(self):
        utc = timezone.utc
        TimePeriod.objects.create(
            name='test',
            period_start=datetime.datetime(2013, 1, 1, tzinfo=utc),
            period_end=datetime.datetime(2013, 1, 2, tzinfo=utc)
        )
        with self.assertRaises(IntegrityError):
            TimePeriod.objects.create(
                name='test 2',
                period_start=datetime.datetime(2013, 1, 1, tzinfo=utc),
                period_end=datetime.datetime(2013, 1, 2, tzinfo=utc)
            )

    def test_two_periods_should_not_overlap_start_date(self):
        period_1 = TimePeriodFactory.create()
        period_2 = TimePeriodFactory.build()
        period_2.period_start = (period_1.period_start
                                 + datetime.timedelta(days=1))
        period_2.period_end = (period_1.period_end
                               + datetime.timedelta(days=1))

        with self.assertRaises(ValidationError) as e:
            period_2.full_clean()
            self.assertTrue('period_start already in another'
                            in str(e.exception))

    def test_two_periods_should_not_overlap_end_date(self):
        period_1 = TimePeriodFactory.create()
        period_2 = TimePeriodFactory.build()
        period_2.period_start = (period_1.period_start
                                 - datetime.timedelta(days=2))
        period_2.period_end = (period_1.period_end
                               - datetime.timedelta(days=1))

        with self.assertRaises(ValidationError) as e:
            period_2.full_clean()
            self.assertTrue('period_end already in another'
                            in str(e.exception))

    def test_period_can_overlap_own_end_date(self):
        period_1 = TimePeriodFactory.create()
        period_1.period_end = (period_1.period_end
                               - datetime.timedelta(days=1))

        period_1.full_clean()

    def test_period_can_overlap_own_start_date(self):
        period_1 = TimePeriodFactory.create()
        period_1.period_start = (period_1.period_start
                                 + datetime.timedelta(days=1))

        period_1.full_clean()

    def test_one_period_can_not_encompass_another(self):
        period_1 = TimePeriodFactory.create()
        period_2 = TimePeriodFactory.build()
        period_2.period_start = (period_1.period_start
                                 - datetime.timedelta(days=1))
        period_2.period_end = (period_1.period_end
                               + datetime.timedelta(days=1))

        with self.assertRaises(ValidationError) as e:
            period_2.full_clean()
            self.assertTrue('encompass another period' in str(e.exception))

    def test_one_period_can_encompass_self(self):
        period_1 = TimePeriodFactory.create()
        period_1.period_start = (period_1.period_start
                                 - datetime.timedelta(days=1))
        period_1.period_end = (period_1.period_end
                               + datetime.timedelta(days=1))

        period_1.full_clean()

    def test_find_current_active_period(self):
        period_1 = TimePeriodFactory.create()
        period_2 = TimePeriodFactory.create()

        with patch('django.utils.timezone.now',
                   Mock(return_value=period_2.period_start)):
            period = TimePeriod.current.get()
            self.assertEqual(period.pk, period_2.pk)

        with patch('django.utils.timezone.now',
                   Mock(return_value=period_1.period_end)):
            period = TimePeriod.current.get()
            self.assertEqual(period.pk, period_1.pk)
