"""
Django command to wait for the database to be available.
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError

# Error that Django throws when DB is not ready
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        # 'stdout'- to log to the screen when command is executing.
        self.stdout.write('Waiting for database...')
        # Var to track if DB is up yet.
        db_up = False
        while db_up is False:
            try:
                # This 'check' method is being mocked inside our tests.
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
