from django.db import models
from django.conf import settings

# Create your models here.

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class PersonDocument(models.Model):
    file = models.FileField(upload_to='people_files/')
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    PASSPORT = 0
    IDENTITY_DOCUMENT = 1
    DRIVERS_LICENSE = 2
    EXTRA = 3

    DOC_TYPE_CHOICES = [
        (PASSPORT, 'passport'),
        (IDENTITY_DOCUMENT, 'identity_document'),
        (DRIVERS_LICENSE, 'drivers_license'),
        (EXTRA, 'extra'),
    ]
    document_type = models.IntegerField(
        choices=DOC_TYPE_CHOICES,
        default=EXTRA)

    def __str__(self):
        return str(self.file.name)