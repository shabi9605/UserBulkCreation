from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    age = models.IntegerField(validators=[MaxValueValidator(120), MinValueValidator(0)])

    def __str__(self):
        return str(self.id)
