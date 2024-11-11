import os
import glob
from os import path
from pathlib import Path
from django.conf import settings


def del_process():
    project_root = str(settings.BASE_DIR)
    def remove_migrations():
    
        res = glob.glob(project_root+'/**/migrations/*', recursive=True)
        skips = [project_root +'/django/']
        for file_path in res:
            for pth in skips:
                if file_path.startswith(pth):
                    continue
            if file_path.endswith('__pycache__'):
                file_path = file_path + '/*'
                sub_res = glob.glob(file_path)
                for file_path1 in sub_res:
                    os.remove(file_path1)
            elif not file_path.endswith('__init__.py'):
                if path.isfile(file_path):
                    os.remove(file_path)
        if path.exists('db.sqlite3'):
            os.remove('db.sqlite3')
        print('Migration files removed')
    
    
    def remove_file_by_extension(ext):
        cnt = 0
        files = Path(project_root).rglob('*.'+ext)
        for path in files:
            os.remove(str(path))
            cnt += 1
        print(f'{str(cnt)} {ext} files removed')
    
    
    remove_migrations()
    remove_file_by_extension('pyc')
    # remove_file_by_extension('po')
    print('done')
    
