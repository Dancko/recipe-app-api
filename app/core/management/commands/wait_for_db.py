"""
Command to wait for the database to be available before starting the app.
"""
import time

from psycopg2 import OperationalError as Psycopg2Error

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    """
    Django command to wait for the database
    """

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Waiting for the database...')
        db_up = False

        while db_up is False:
            try:
                self.check(databases=['default'])
                connection.ensure_connection()
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('Database unavailable. \
                    Waiting for 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))
