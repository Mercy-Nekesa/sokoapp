"""
Test support harness to make setup.py test work.
"""

import sys

from django.conf import settings
settings.configure(
    DATABASES = {
        'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory;'}
    },
    INSTALLED_APPS = ['django.contrib.auth', 'django.contrib.contenttypes', 'fack'],
    ROOT_URLCONF = 'fack.urls',
)

def runtests():
    import django.test.utils
    runner_class = django.test.utils.get_runner(settings)
    test_runner = runner_class(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['fack'])
    sys.exit(failures)