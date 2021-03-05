# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User_Content(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    version = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_update_at = models.DateTimeField(auto_now=True)
    html = models.TextField(default='')
    css = models.TextField(default='')
    configuration = models.TextField(default='')
    active = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.configuration

    # def html(self):
    #     return self.html

    # def css(self):
    #     return self.css

    class Meta:
        unique_together = (("userid", "version"),)