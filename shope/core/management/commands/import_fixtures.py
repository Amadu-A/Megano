from django.db import IntegrityError
from django.core.management.base import BaseCommand
import os
import logging
import shutil
from django.core.mail import send_mail
from django.conf import settings

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    """Нстройка логов"""

    handler = logging.FileHandler(log_file, mode='w')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


class Command(BaseCommand):
    help = 'import fixtures'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--filename', type=str)
        parser.add_argument('-e', '--email', type=str)

    def handle(self, *args, **options):
        logger = setup_logger('log', 'import/successful_import/success_log.log', logging.INFO)
        error_logger = setup_logger('error', 'import/unsuccessful_import/unsuccess_log.log', logging.ERROR)

        if options['filename']:
            fixture = options['filename']
            s = os.system("python manage.py loaddata %s" % fixture)
            if not s:
                logger.info(f'{fixture} was uploaded')
                shutil.copy2(f'fixtures/{fixture}', 'import/successful_import')
            else:
                error_logger.error(f'an error occurred in the {fixture} file')
                shutil.copy2(f'fixtures/{fixture}', 'import/unsuccessful_import')

        else:
            for fixture in sorted(os.listdir('fixtures'), reverse=False):
                s = os.system("python manage.py loaddata %s" % fixture)
                if not s:
                    shutil.copy2(f'fixtures/{fixture}', 'import/successful_import')
                    logger.info(f'{fixture} was uploaded')
                else:
                    error_logger.error(f'an error occurred in the {fixture} file')
                    shutil.copy2(f'fixtures/{fixture}', 'import/unsuccessful_import')

        if options['email']:
            with open('import/unsuccessful_import/unsuccess_log.log', 'r') as file:
                head = ''.join(file.readlines(1))
            send_mail('Зарузка фикстур',
                      head,
                      settings.EMAIL_HOST_USER,
                      [options['email']])


