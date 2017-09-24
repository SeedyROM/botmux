import glob
import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """A command to remove all migrations from django apps.
    """
    help = 'Remove all previous migrations \
            (from and app or all apps) and recreate them.'

    def add_arguments(self, parser):
        """Add optional argument to specify which app is being reset.
        """
        parser.add_argument(
            'app_module_name',
            nargs='+',
            type=str,
            default=None
            )

    def handle(self, *args, **options):
        """Called when the command in run from the manager.
        """
        app_names = options.get('app_module_name')

        if settings.DEBUG is not True:
            raise CommandError(
                'Cannot reset migrations on non debug application!'
                )

        try:
            if app_names:
                for app_name in options['app_module_name']:
                    self.clear_migrations_for_app(app_name)
            else:
                self.clear_all_migrations()
        except BaseExcetion as e:
            raise e from None
            raise CommandError('Failed to reset migrations!')

    def clear_migrations_for_app(self, app_name):
        """Clearmigrations for a certain app.
        """
        migration_files = glob.iglob(
            os.path.join(settings.BASE_DIR, f'{app_name}/migrations/[!__]*.py')
            )

        [os.remove(filename) for filename in migration_files]

        call_command('makemigrations', app_name, verbosity=3)

    def clear_all_migrations(self):
        """Clear migrations for all apps in the project.
        """
        migration_files = glob.iglob(
            os.path.join(settings.BASE_DIR, '**/migrations/[!__]*.py')
            )

        [os.remove(filename) for filename in migration_files]

        call_command('makemigrations', verbosity=3)
