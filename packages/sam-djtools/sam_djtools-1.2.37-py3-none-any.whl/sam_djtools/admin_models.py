import pytz
from datetime import datetime
from .utils import DjangoUtils

from django.db import models
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.models import User as user_model
from django_currentuser.middleware import get_current_user
log_fields = ['created_at', 'created_by', 'updated_at', 'updated_by']
aul_is = hasattr(settings, 'ADMIN_UPDATE_LOGS')


class SamAdmin(admin.ModelAdmin):
    readonly_fields = log_fields if aul_is and settings.ADMIN_UPDATE_LOGS else []
    save_on_top = settings.SAVE_ON_TOP if hasattr(settings, 'SAVE_ON_TOP') else False
    exclude = log_fields if not aul_is or (aul_is and not settings.ADMIN_UPDATE_LOGS) else []

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context['site_url'] = DjangoUtils.site_url(request)
        res = super().render_change_form(request, context, add, change, form_url)
        return res


class SamInlineAdmin(admin.StackedInline):
    exclude = log_fields


class SamModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(null=True, blank=True,)
    created_by = models.ForeignKey(
        user_model,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_created_by',
        related_query_name='%(app_label)s_%(class)s'
    )
    updated_at = models.DateTimeField(null=True, blank=True,)
    updated_by = models.ForeignKey(
        user_model,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_updated_by',
        related_query_name='%(app_label)s_%(class)s'
    )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        instance = self
        if instance.pk:
            instance.updated_at = datetime.now(tz=pytz.UTC)
            instance.updated_by = get_current_user()
        else:
            instance.created_at = datetime.now(tz=pytz.UTC)
            instance.created_by = get_current_user()
        return super().save(force_insert, force_update, using,
             update_fields)
