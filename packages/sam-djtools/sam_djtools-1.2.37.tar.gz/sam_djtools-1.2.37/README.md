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
4. `python manage.py initsql.py`
   5. This step will create db (sqlite)
   6. will make makemigrations and migrate 
   7. create a super user `sa` with password `123`
   8. will also add three rows to `sample_app.Model1`
   9. So u can directly test form navigation without doing setup

4. `python manage.py runsever`

5. Open following url in your browser and login with given username `sa` and password `123`
   http://127.0.0.1:8000/admin/ 

6. Go to
   http://127.0.0.1:8000/admin/sample_app/model1/1/change/

7. Add image to check preview
