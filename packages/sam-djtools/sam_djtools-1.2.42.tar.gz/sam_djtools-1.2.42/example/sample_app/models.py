from django.db import models
from sam_djtools.admin_models import SamModel


class ModelWithUpdateLog(SamModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
