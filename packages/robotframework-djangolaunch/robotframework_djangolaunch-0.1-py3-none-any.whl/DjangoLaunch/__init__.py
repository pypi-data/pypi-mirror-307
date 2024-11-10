# -*- coding: utf-8 -*-
from robot.api import logger
from warnings import warn

import os
import signal
import subprocess

__version__ = '1.0'
ROBOT_LIBRARY_DOC_FORMAT = 'reST'


class DjangoLaunch:
    """DjangoLaunch is a web testing library to test Django with Robot
    Framework.
    """

    django_pid = None

    # TEST CASE => New instance is created for every test case.
    # TEST SUITE => New instance is created for every test suite.
    # GLOBAL => Only one instance is created during the whole test execution.
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self, host="0.0.0.0", port=8000, manage='mysite/manage.py',
                 settings='mysite.settings'):
        """Django2Library can be imported with optional arguments.

        `host` is the hostname of your Django instance. Default value is
        '127.0.0.1'.

        `port` is the port number of your Django instance. Default value is
        8000.

        `manage` is the path to your Django instance manage.py.

        `settings` is the path to your Django instance settings.py.

        Examples:
        | Library | DjangoLaunch    | 127.0.0.1         | 55001              | manage=mysite/manage.py | settings=mysite.settings | # Sets default hostname to 127.0.0.1 and the default port to 55001.                |  # noqa
        """
        self.host = host
        self.port = port
        self.manage = os.path.realpath(manage)
        self.settings = settings

    def manage_makemigrations(self):
        """Create migrations by running 'python manage.py makemigrations'."""
        args = [
            'python',
            self.manage,
            'makemigrations',
        ]
        subprocess.call(args)

    def manage_migrate(self):
        """Execute migration by running 'python manage.py migrate'."""
        args = [
            'python',
            self.manage,
            'migrate',
            '--settings=%s' % self.settings,
        ]
        subprocess.call(args)

    def manage_flush(self):
        """Clear database by running 'python manage.py flush'."""
        args = [
            'python',
            self.manage,
            'flush',
            '--noinput',
            '--settings=%s' % self.settings,
        ]
        subprocess.call(args)

    def start_django(self):
        """Start the Django server."""
        self.manage_flush()
        self.manage_makemigrations()
        self.manage_migrate()
        logger.console("-" * 78)
        args = [
            'python',
            self.manage,
            'runserver',
            '%s:%s' % (self.host, self.port),
            '--nothreading',
            '--noreload',
            '--settings=%s' % self.settings,
        ]

        self.django_pid = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        ).pid
        logger.console(
            "Django started (PID: %s)" % self.django_pid,
        )
        logger.console("-" * 78)

    def stop_django(self):
        """Stop the Django server."""
        os.kill(self.django_pid, signal.SIGKILL)
        logger.console(
            "Django stopped (PID: %s)" % self.django_pid,
        )
        logger.console("-" * 78)
