from django.db import models

class TimeStampedModel(models.Model):
    """Time Stamped Model"""
    created = models.DateTimeField(blank=True,null=True,auto_now_add=True)
    updated = models.DateTimeField(blank=True,null=True,auto_now=True)

    class Meta:
        abstract = True
        