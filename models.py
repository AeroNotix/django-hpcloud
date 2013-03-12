import datetime

from django.db import models
from django_hpcloud.tzhelpers import Local

class AuthToken(models.Model):
    token = models.CharField(max_length=1000)
    expires = models.DateTimeField()

    def save(self, *args, **kwargs):
        if len(AuthToken.objects.all()) > 0:
            AuthToken.objects.all().delete()
        super(AuthToken, self).save(*args,  **kwargs)

    def is_valid(self):
        '''
        Returns whether this token has expired or not.
        '''
        now = datetime.datetime.now(tz=Local)
        return now <= self.expires
