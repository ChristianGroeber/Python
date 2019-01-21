from django.db import models

# Create your models here.exit


class UserLogin(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    loggedInAt = models.DateTimeField('Date Published')

    def __str__(self):
        return self.username
