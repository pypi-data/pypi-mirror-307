from django.contrib import admin
from sam_djtools.admin_models import SamAdmin
from .models import ModelWithUpdateLog


class ModelUpdateLogAdmin(SamAdmin):
    pass


# Register your models here.
admin.site.register(ModelWithUpdateLog, ModelUpdateLogAdmin)
