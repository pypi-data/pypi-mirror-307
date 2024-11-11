from django.contrib import admin
from sam_djtools.navigate_records import NavigateFormAdmin

default_app_config = 'sam_djtools.apps.SamToolsConfig'
admin.ModelAdmin = NavigateFormAdmin