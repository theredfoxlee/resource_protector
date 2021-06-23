from django.core.management.base import BaseCommand, CommandError
from resource_protector.models import ProtectedFileModel, ProtectedUrlModel


class Command(BaseCommand):

    RESOURCES_TO_PURGE = [ProtectedFileModel, ProtectedUrlModel]

    help = 'Removes old resources (like files or ulrs) from an app.'

    def add_arguments(self, parser):
        parser.add_argument('seconds', type=int, nargs='?', default=None)

    def handle(self, *args, **options):
        counter = 0
        for resource in self.RESOURCES_TO_PURGE:
            if options['seconds'] is not None:
                counter += resource.purge(seconds=options['seconds'])
            else:
                counter += resource.purge()
        if counter > 0:
            self.stdout.write(self.style.SUCCESS(f'Purged #{counter} elements.'))
        else:
            self.stdout.write(self.style.NOTICE('Nothing to purge.'))
