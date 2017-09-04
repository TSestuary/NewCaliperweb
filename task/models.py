# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=200)
    configuration = JSONField()
    results = JSONField()
    output_path = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.name