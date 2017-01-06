import os
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    help = 'Restores SquamataBase from a collection of fixtures'

    def add_arguments(self, parser):
        parser.add_argument(
            '-e', '--exclude', dest='exclude', action='append', default=['Taxonomy'],
            help='An app_label to exclude '
                 '(use multiple --exclude to exclude multiple apps/models).'
        )

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
            if fixture in options['exclude']:
                continue
            fps = [os.path.join(fixdir, fixture) for fixdir in content['dirs']]
            fixtures.extend([os.path.join(fp, f) for fp in fps for f in os.listdir(fp) if f.endswith('.json') or f.endswith('.json.zip')])
        print("Loading fixture data (may take some time) . . .")
        call_command('loaddata', *fixtures)