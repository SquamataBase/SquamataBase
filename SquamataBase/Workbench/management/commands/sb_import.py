import os
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

if settings.DATABASES['default']['ENGINE'].endswith('spatialite'):
    pass
else:
    raise ImproperlyConfigured(
            'The sb_import command is only configured to work '
            'with sqlite databases.'
        )

class Command(BaseCommand):
    help = 'Imports the SquamataBase taxonomy'

    def add_arguments(self, parser):
        try:
            fixtures = settings.FIXTURES
        except AttributeError:
            raise ImproperlyConfigured(
                'The settings file is missing a fixture registry. '
                'No imports will be performed without one.'
                )
        TAXONOMY = os.path.join(fixtures['Taxonomy']['dirs'][-1], 'Taxonomy', 'taxonomy.txt')
        parser.add_argument(
            '-p', '--path', default=TAXONOMY, dest='path',
            help='Absolute file path to taxonomy'
        )

    def handle(*args, **options):
        output = ".mode csv\n"
        output += "PRAGMA foreign_keys=OFF;\n"
        output += ".import %s sb_taxon\n" % options['path']
        output += ".read %s utf-8\n" % os.path.join(os.path.dirname(os.path.abspath(__file__)), '_create.sql')
        output += "PRAGMA foreign_keys=ON;\n"
        with open("/tmp/taxonomyInit.txt", "w") as f:
            f.write(output)
        cmd = "cat %s | spatialite -silent %s" % ("/tmp/taxonomyInit.txt", settings.DATABASES['default']['NAME'])
        print("Importing taxonomy tables (may take some time) . . .")
        os.system(cmd)
        print("Taxonomy import complete.")
        os.remove("/tmp/taxonomyInit.txt")
