from django.conf import settings
from django.db import transaction, router
from django.contrib import admin, messages
from django.http import HttpResponseRedirect


def next_prev_id(model, row_id):
    output = {"prev": "", "next": "", "current": row_id}
    rec_count = model.objects.all().count()

    if rec_count <= 1:
        return output

    prev_obj = model.objects.filter(pk__lt=row_id).order_by("-pk").first()
    next_obj = model.objects.filter(pk__gt=row_id).order_by("pk").first()

    def update_output(nav_obj, direction):
        if nav_obj:
            output[direction] = nav_obj.pk
        else:
            sign = '-' if direction == 'prev' else ''
            nav_obj = model.objects.order_by(sign  + "pk").first()
            if nav_obj and nav_obj.pk != row_id:
                output[direction] = nav_obj.pk

    update_output(prev_obj, 'prev')
    update_output(next_obj, 'next')
    return output


class NavigateFormAdmin(admin.ModelAdmin):
    save_on_top = settings.SAVE_ON_TOP if hasattr(settings, 'SAVE_ON_TOP') else False

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        try:
            if object_id:
                obj_id = int(object_id)
                ids = next_prev_id(self.model, obj_id)
                if extra_context:
                    extra_context['npc_ids'] = ids
                else:
                    extra_context = {'npc_ids': ids}
            with transaction.atomic(using=router.db_for_write(self.model)):
                return self._changeform_view(request, object_id, form_url, extra_context)
        except Exception as e:
            self.message_user(request, e, level=messages.ERROR)
            return HttpResponseRedirect(request.path)
