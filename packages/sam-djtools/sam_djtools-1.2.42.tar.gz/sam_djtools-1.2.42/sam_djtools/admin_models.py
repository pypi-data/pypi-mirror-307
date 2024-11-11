from datetime import datetime

import pytz
from django.db import models
from django.contrib import admin
from django.conf import settings

from django.contrib.auth.models import User as UserModel
from django_currentuser.middleware import get_current_user

def get_default_user():
    cur_user = get_current_user()
    if not cur_user:
        raise Exception('No User found in request')
    return cur_user

def get_time_now():
    return datetime.now(tz=pytz.UTC)


class SamModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)

    created_by = models.ForeignKey(
        UserModel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_created_by",
        default=get_default_user
    )

    updated_by = models.ForeignKey(
        UserModel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_updated_by",
        default=get_default_user
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = self.created_at or datetime.now(tz=pytz.UTC)
            self.created_by = self.created_by or get_current_user()
        self.updated_at = datetime.now(tz=pytz.UTC)
        self.updated_by = get_current_user()
        super().save(*args, **kwargs)


log_fields = ['created_at', 'created_by', 'updated_at', 'updated_by']
aul_is = hasattr(settings, 'ADMIN_UPDATE_LOGS')
from .utils import GeneralUtils
class SamAdmin(admin.ModelAdmin):
    readonly_fields = log_fields if aul_is and settings.ADMIN_UPDATE_LOGS else []
    save_on_top = settings.SAVE_ON_TOP if hasattr(settings, 'SAVE_ON_TOP') else False
    exclude = log_fields if not aul_is or (aul_is and not settings.ADMIN_UPDATE_LOGS) else []

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context['site_url'] = GeneralUtils.site_url(request)
        res = super().render_change_form(request, context, add, change, form_url)
        return res


class SamInlineAdmin(admin.StackedInline):
    exclude = log_fields
