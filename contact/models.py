from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=221, blank=True)
    message = models.TextField()


class Sub(models.Model):
    email = models.EmailField()
