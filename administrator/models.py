from django.db import models

# Create your models here.


class Administrator(models.Model):
    administrator_name = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=20, null=False)
    authority = models.BooleanField(null=False)
    is_available = models.BooleanField(null=False, default=True)

    def __str__(self):
        return self.administrator_name


class LibRoot(models.Model):
    root_name = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=20, null=False)
    authority = models.CharField(max_length=1, null=False)

    def __str__(self):
        return self.root_name


