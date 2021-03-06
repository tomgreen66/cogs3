import csv

from django.core.management.base import BaseCommand
from django.db import transaction

from users.models import CustomUser
from users.models import Profile


class Command(BaseCommand):
    help = 'Import Shibboleth user accounts from csv file.'

    def add_arguments(self, parser):
        parser.add_argument('csv_filename')

    def handle(self, *args, **options):
        filename = options['csv_filename']
        try:
            with open(filename, newline='', encoding='ISO-8859-1') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        with transaction.atomic():
                            user, created = CustomUser.objects.get_or_create(
                                username=row['institutional_address'].lower(),
                                email=row['institutional_address'].lower(),
                                first_name=row['firstname'].title(),
                                last_name=row['surname'].title(),
                                is_shibboleth_login_required=True,
                            )
                            if created:
                                user.set_password(CustomUser.objects.make_random_password())
                                user.save()
                                message = 'Successfully created user account: {email}'.format(
                                    email=row['institutional_address']
                                )
                                self.stdout.write(self.style.SUCCESS(message))
                            else:
                                message = '{email} already exists.'.format(email=row['institutional_address'])
                                self.stdout.write(self.style.SUCCESS(message))

                            profile = user.profile
                            if not profile.hpcw_username:
                                profile.hpcw_username = row['hpcw_username'].lower()
                            if not profile.hpcw_email:
                                profile.hpcw_email = row['hpcw_email'].lower()
                            profile.raven_username = row['raven_username']
                            if row['raven_uid']:
                                profile.uid_number = int(row['raven_uid'])
                            profile.raven_email = row['raven_email'].lower()
                            profile.description = row['description']
                            profile.phone = row['phone']
                            profile.shibboleth_id = row['institutional_address'].lower()
                            profile.save()

                            message = 'Successfully updated user profile: {email}'.format(
                                email=row['institutional_address']
                            )
                            self.stdout.write(self.style.SUCCESS(message))
                    except Exception as e:
                        message = '{error}\n{row}'.format(error=e, row=row)
                        self.stdout.write(self.style.ERROR(message))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Unable to open ' + filename))
