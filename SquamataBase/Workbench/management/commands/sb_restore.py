import os
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    help = 'Restores SquamataBase from a collection of fixtures'

    def add_arguments(self, parser):        
        pass

    def handle(self, *args, **options):
        try:
            f = settings.FIXTURES
        except AttributeError:
            raise ImproperlyConfigured(
                'The settings file is missing a fixture registry.'
                'Database will not be restored without one.'
            )
        fixtures = []
        for fixture, content in f.items():
            fixtures.extend([os.path.join(fixdir, fixture) for fixdir in content['dirs']])
        call_command('loaddata', *fixtures)
