from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    age = models.IntegerField()
    sex = models.BooleanField()

    def __str__(self):
        return self.name, self.password, self.age, self.sex
