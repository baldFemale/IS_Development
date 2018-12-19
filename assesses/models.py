from django.db import models

# Create your models here.
class Assess(models.Model):
    name = models.CharField(max_length=12)
    password = models.CharField(max_length=18)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

