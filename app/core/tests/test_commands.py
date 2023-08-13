"""
Test Django management commands.
"""

# To mock behaviour of a database
from unittest.mock import patch

# Error that would be raised when we try connecting to DB when DB is not ready.
from psycopg2 import OperationalError as Psycopg2Error

# Django helper f-n that allows to call command by the name. It will allow to \
# call command which we are testing.
from django.core.management import call_command
# Another 'OperationalError'. It may get thrown by DB depending on what \
# state of the start-up process DB is in. So we cover both options.
from django.db.utils import OperationalError
# Base test class that we will use for creating our unit tests. \
# 'SimpleTestCase' doesn't create any DB setup.
from django.test import SimpleTestCase


# Will be doing testing for diferent methods therefore we add here \
# "@patch". The command that we are mocking is \
# "'core.management.commands.wait_for_db.Command.check'". We will \
# be mocking 'check' method to simulate 'check' methos returning \
# Exception and we can simulate returning the value.
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    # Because we are using '@patch', it will add a new/additional \
    # argument to each of the calls that we make to test methods. \
    # And we need to catch that argument, therefore adding parameter \
    # 'patched_check'. We can use that to customise the behaviour.
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database is ready."""
        # Meaning: When 'check' is called inside of a command/test-case, \
        # we want to return True.
        patched_check.return_value = True

        call_command('wait_for_db')

        # Tests if the mocked object i.e. "check" is called with \
        # these parameters: database=['default']
        patched_check.assert_called_once_with(databases=['default'])

    # Testing what should happen if the database is NOT ready. If \
    # Database or 'check' returns some exceptions, that indicated \
    # that DB is not ready yet.
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError"""
        # If DB is not ready we want to raise exceptions. We will \
        # raise exception here using "side_effect". "side_effect" \
        # allows passing-in various diferent items that are handled \
        # diferently depending on their type. If we pass-in exception, \
        # then mocking lybrary will return exception. If we will pass \
        # Boolean, then it will return Boolean value.
        # Steps:
        # 1) "[Psycopg2Error] * 2" meaning: First 2 times when we call \
        # mocked method, we want to raise Psycopg2Error error.
        #  2) "[OperationalError] * 3" meaning: then we want to raise \
        # 3 OperationalError errors
        #  3) "[True]" meaning: When we call mocked method 6th time, \
        # we got back 'True'.
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        # We expect to call 'check' method 6 times.
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
