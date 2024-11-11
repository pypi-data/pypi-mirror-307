**Installation**

1. `pip install sam-djtools`
2. Add `sam_djtools` in installed apps in `settings.py` of django project
   

    INSTALLED_APPS = [
       'sam_djtools',
       # ...
    ]
(at the top)

**Description**

It adds Next and Prev buttons to the top of each edit form of django admin site
for all the models of all the apps in your project, without need to do anything
except installing the module with pip plus adding to the top of `INSTALLED_APPS` in `settings.py`

**Instructions to run the sample usage**

1. `git clone https://github.com/humblesami/sam-djtools.git`
2. `cd sample_usage`
3. `pip install -r requirements.txt`
4. `python manage.py resetdb`
   1. This step will delete db (if engine is sqlite or posgtgresql)
   2. will make makemigrations and migrate 
   3. will create db
   4. create a super user `admin@localhost` with password `123`
   5. Will create three records of `ModelWithUpdateLog`

5. `python manage.py runsever`

### Features

1. You can import and use `GeneralUtils, EmailUtils, DbUtils` having variety of methods 
which we commonly would need to write in django project
2. Form navigation => while changing/reading records in form, you n=can navigate to next/prev records
3. You can use python manage.py resetdb if during development you need, also you can set 
`FIXTURES_PATH = str(BASE_DIR) + '/fixtures.json'` to your existing data
so all can be reset using a single command
4. The sample app contains a model (as following) inherited from `SamModel` and 
the `SamModel` is set to maintain all the update logs automatically

```
from django.db import models
from sam_djtools.admin_models import SamModel

class ModelWithUpdateLog(SamModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
```
and an admin as
```
from django.contrib import admin
from sam_djtools.admin_models import SamAdmin
from .models import ModelWithUpdateLog

class ModelUpdateLogAdmin(SamAdmin):
    pass

admin.site.register(ModelWithUpdateLog, ModelUpdateLogAdmin)
```
This admin will show all record update logs in form because we have set

```ADMIN_UPDATE_LOGS = True```

in `settings.py`

Open following url in your browser and login with given username `admin@localhost` and password `123`
   http://localhost:8000/admin/sample_app/modelwithupdatelog/1/change/
to explore the `update logs` and `navigation` feature 