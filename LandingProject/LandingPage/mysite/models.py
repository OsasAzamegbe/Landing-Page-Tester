from django.db import models


class Info(models.Model):
    firstname = models.CharField(max_length=32)
    lastname = models.CharField(max_length=32)
    username = models.CharField(max_length=32)
    email = models.EmailField()
    password = models.CharField(max_length=32)

    def __str__(self):
        return self.email
