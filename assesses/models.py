from django.db import models
from ApplyController.models import Restaurant


class Assessor(models.Model):
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=12)
    password = models.CharField(max_length=18)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AssessInfo(models.Model):
    ID = models.AutoField(primary_key=True)
    RestaurantID = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    AssessorID = models.ForeignKey(Assessor, on_delete=models.CASCADE)
    Result_category = (
        (0, '通过'),
        (1, '拒绝'),
    )
    Result = models.PositiveIntegerField(choices=Result_category)
    AssessTime = models.DateTimeField(auto_now_add=True)
    Notes = models.CharField(max_length=100, null=True)
