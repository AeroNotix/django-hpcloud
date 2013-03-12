from django.db import models

class AuthToken(models.Model):
    token = models.CharField(max_length=1000)
    expires = models.DateTimeField()

    def save(self, *args, **kwargs):
        if len(AuthToken.objects.all()) > 0:
            AuthToken.objects.all().delete()
        super(AuthToken, self).save(*args,  **kwargs)
