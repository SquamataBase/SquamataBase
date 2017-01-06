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
    outfile_prefix = infile.split('.json')[0]
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
        parser.add_argument(
            '-p', '--page-size', default=10000, dest='page_size',
            help='Specifies maximum number of objects per JSON array.'
        )

    def handle(self, *args, **options):
        try:
            fixtures = settings.FIXTURES
        except AttributeError:
            raise ImproperlyConfigured(
                'The settings file is missing a fixture registry.'
                'Database backups will not be performed without one.'
            )
        PAGE_SIZE = options.pop('page_size')
        for fixture, content in fixtures.items():
            if not content['backup']:
                continue
            app_label = content['app_label']
            if app_label == 'Taxonomy':
                print('You have chosen to create a Taxonomy fixture. '
                    'This is not allowed.')
                continue
            options.update({
                'output': os.path.join(content['dirs'][-1], fixture, fixture.lower()+'.json'),
                'exclude': ['.'.join([app_label, model_label]) for model_label in content.get('exclude', [])],
            })
            if content.get('include', False):
                app_labels = ['.'.join([app_label, model_label]) for model_label in content['include']]
            else:
                app_labels = [app_label]
            if len(set(app_labels).intersection(options['exclude'])):
                raise ImproperlyConfigured(
                        'Cannot simultaneously include and exclude models '
                        'from the %s fixture.' % app_label
                    )
            if options['verbosity'] > 0:
                print('Creating fixture for %s objects' % fixture)
            call_command('dumpdata', *app_labels, **options)
            if options['verbosity'] > 0:
                print('Formatting fixture . . .')
            split_json_stream(options['output'],  PAGE_SIZE)
            os.remove(options['output'])
        

