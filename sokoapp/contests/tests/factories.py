from datetime import datetime

from django.utils import timezone
import factory

from test_app.models import TimePeriod


class TimePeriodFactory(factory.DjangoModelFactory):
    FACTORY_FOR = TimePeriod

    name = factory.Sequence(lambda n: 'Period {0}'.format(n))
    period_start = factory.Iterator((
        datetime(2013, 5, 6, tzinfo=timezone.utc),
        datetime(2013, 5, 13, tzinfo=timezone.utc),
        datetime(2013, 5, 20, tzinfo=timezone.utc),
        datetime(2013, 5, 27, tzinfo=timezone.utc),
    ))
    period_end = factory.Iterator((
        datetime(2013, 5, 12, 23, 59, 59, tzinfo=timezone.utc),
        datetime(2013, 5, 19, 23, 59, 59, tzinfo=timezone.utc),
        datetime(2013, 5, 26, 23, 59, 59, tzinfo=timezone.utc),
        datetime(2013, 6, 2, 23, 59, 59, tzinfo=timezone.utc),
    ))
