import os
import json
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings


def split_json_stream(infile, PAGE_SIZE=10000):
    """Splits a Django fixture file into chunks.

        .. py:attribute:: infile

            A file that is the output of Django's dumpdata command.
            dumpdata must be called with --indent=0!

        .. py:attribute:: PAGE_SIZE

            The chunk size to use for splitting the fixture file.
            Each chunk is a single model instance.
    """
    outfile_prefix = infile.rstrip('.json')
    with open(infile) as f:
        object_count = 0
        file_count = 0
        objects = ''
        while True:
            next_char = f.read(1)
            if not next_char: # EOF
                object_count += 1
                with open('{}-{}.json'.format(outfile_prefix, file_count), 'w') as outfile:
                    outfile.write(json.dumps(json.loads(objects), indent=0, separators=(',', ':'), sort_keys=True))
                    file_count += 1
                return
            if objects.endswith('}, {'): # JSON object boundary. This condition is sensitive to fixture file formatting used with dumpdata
                object_count += 1
                if object_count % PAGE_SIZE == 0:
                    objects = objects.rstrip(', {')
                    objects += ']'
                    # dump logic
                    with open('{}-{}.json'.format(outfile_prefix, file_count), 'w') as outfile:
                        outfile.write(json.dumps(json.loads(objects), indent=0, separators=(',', ':'), sort_keys=True))
                        file_count += 1
                    # reset JSON string
                    objects = '[{'
            objects += next_char


class Command(BaseCommand):
    help = 'Creates a backup of SquamataBase'

    def add_arguments(self, parser):
        # arguments to datadump command that we'll use
        parser.add_argument(
            'args', metavar='app_label', nargs='*',
            help='Restricts dumped data to the specified app_label or app_label.ModelName.',
        )
        parser.add_argument(
            '-e', '--exclude', dest='exclude', action='append', default=['Geography.SpatialRefSys'],
            help='An app_label or app_label.ModelName to exclude '
                 '(use multiple --exclude to exclude multiple apps/models).',
        )
        # additional arguments specific to this command
        parser.add_argument(
            '-p', '--page-size', default=10000, dest='page_size',
            help='Specifies maximum number of objects per JSON array.'
        )


    def handle(self, *app_labels, **options):
        page_size = options.pop('page_size')
        # remaining options belong to datadump
        if len(app_labels) == 0:
            app_labels = ['Bibliography', 'FoodRecord', 'Geography', 'Glossary', 'Specimen', 'Workbench']
        try:
            settings.FIXTURES
        except AttributeError:
            raise ImproperlyConfigured(
                'The settings file is missing a fixture registry.'
                'Database backups will not be performed without one.'
            )
        for label in app_labels:
            try:
                settings.FIXTURES[label]
            except KeyError:
                raise ImproperlyConfigured(
                    'The %(app)s app is missing from the fixture registry in the settings file. '
                    'Database backups will not be performed unless this registry is complete.',
                    params={'app': label}
                )
        for label in app_labels:
            options.update(
                {
                    'output': os.path.join(settings.FIXTURES[label], '.'.join([label.lower(), 'json']))
                }
            )
            if options['verbosity'] > 0:
                print('Creating fixture for %s objects' % label)
            call_command('dumpdata', *[label], **options)
            if options['verbosity'] > 0:
                print('Formatting fixture . . .')
            split_json_stream(options['output'],  page_size)
            os.remove(options['output'])
        

