import os
import sam_pytools
from ...del_migrations import del_process

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

try:
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
except:
    pass


class Command(BaseCommand):
    help = 'setting up db i.e. create db or drop db for dev purpose'
    str = 'website/management/commands'

    def drop_create_db(self):
        res = 'Unknown'
        database_info = settings.DATABASES['default']
        del_process()
        db_engine = database_info['ENGINE']
        if db_engine.endswith('sqlite3') or db_engine.endswith('sqlite3_backend'):
            db_path = str(settings.BASE_DIR) + '/db.sqlite3'
            if os.path.exists(db_path):
                os.remove(db_path)
            return 'created'
        else:
            db_con = None
            if db_engine.endswith('postgresql') or db_engine.endswith('postgresql_backend'):
                db_con = psycopg2.connect(
                    host="localhost", user=database_info['USER'],
                    dbname='postgres', password=database_info['PASSWORD']
                )
                db_con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cur = db_con.cursor()
                disconnect_query = f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{database_info['NAME']}'
                  AND pid <> pg_backend_pid();
                """
                cur.execute(disconnect_query)
                drop_query = f"DROP DATABASE IF EXISTS {database_info['NAME']}"
                cur.execute(drop_query)
                create_query = f"CREATE DATABASE {database_info['NAME']}"
                cur.execute(create_query)
            if db_con:
                db_con.close()
                return 'created'
            else:
                return ' failed to connect'

    def add_arguments(self, parser):
        parser.add_argument(
            '-hard', '--hard', action='store_true',
            help='drop database if exists and create new one'
        )

    def handle(self, *args, **kwargs):
        try:
            res = self.drop_create_db()
            if res == 'created':
                call_command('makemigrations')
                call_command('migrate')
                fixture_path = settings.FIXTURES_PATH if hasattr(settings, 'FIXTURES_PATH') else ''
                if fixture_path and os.path.isfile(fixture_path):
                    call_command('loaddata', fixture_path)
                else:
                    print(f'{fixture_path} does not exist')
            elif res == 'already exists':
                print('Already created')
            else:
                print(f'Failed because {res}')
        except:
            error_message = sam_pytools.LogUtils.get_error_message()
            print(f'Error {error_message}')
