from django.db import models

# Create your models here.


class Administrator(models.Model):
    administrator_name = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=20, null=False)
    authority = models.BooleanField(null=False)

    def __str__(self):
        return self.administrator_name

