import os
import glob
from os import path
from pathlib import Path
from django.conf import settings


def del_process():

    project_root = str(settings.BASE_DIR)

    def remove_folders(folder_name):
        res = glob.glob(project_root + '/**/' + folder_name + '/*', recursive=True)
        skips = [str(project_root) + '/django/']
        cnt = 0
        for file_path in res:
            for pth in skips:
                if file_path.startswith(pth):
                    continue
            skip = False
            if file_path.endswith('__init__.py') and folder_name == 'migrations':
                skip = True
            if not skip and path.isfile(file_path):
                os.remove(file_path)
                cnt += 1
        print(f'{cnt} Files removed from folder {folder_name}')

    def remove_file_by_extension(ext):
        cnt = 0
        files = Path(project_root).rglob('*.' + ext)
        for path in files:
            os.remove(str(path))
            cnt += 1
        print(str(cnt) + ' ' + ext + ' files removed')

    def remove_files(file_name):
        cnt = 0
        files = Path(project_root).rglob(file_name)
        for path in files:
            os.remove(str(path))
            cnt += 1
        print(str(cnt) + ' ' + file_name + ' files removed')

    def remove_migrations():
        remove_folders('migrations')
        if path.exists('db.sqlite3'):
            os.remove('db.sqlite3')

    # remove_folders('tests')
    # remove_folders('__pycache__')
    # remove_files('tests.py')
    remove_file_by_extension('pyc')
    remove_file_by_extension('po')
    remove_migrations()


print('done')

