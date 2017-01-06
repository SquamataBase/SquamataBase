import os
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    help = 'Initializes SquamataBase'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        call_command('migrate', *args, **options)
        call_command('createsuperuser', *args, **options)
        call_command('sb_import', *args, **options)
        call_command('sb_restore', *args, **options)