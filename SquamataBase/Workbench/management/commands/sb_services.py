import os
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings
from ._services import SERVICES

class Command(BaseCommand):
    help = 'Start and stop SquamataBase services'

    def add_arguments(self, parser):
        parser.add_argument(
            'args', metavar='command [service name]', nargs='*',
            help='availabe commands are start, stop, and list'
        )

    def handle(self, *args, **options):
        if len(args) == 0:
            pass
        elif len(args) == 1:
            if args[0] == 'list':
                for abbr, service in SERVICES.items():
                    print(service.VERBOSE_NAME, service.status())                    
            else:
                raise CommandError('Invalid arguments.')
        else:
            service_name = args[1]
            if args[0] == 'start':
                try:
                    SERVICES[service_name].start()
                except KeyError:
                    raise CommandError('Unrecognized service.')
            elif args[0] == 'stop':
                try:
                    SERVICES[service_name].stop()
                except KeyError:
                    raise CommandError('Unrecognized service.')
            elif args[0] == 'restart':
                try:
                    SERVICES[service_name].restart()
                except KeyError:
                    raise CommandError('Unrecognized service.')
            else:
                raise CommandError('Invalid arguments.')

