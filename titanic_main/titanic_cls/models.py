from django.db import models


class Titanic(models.Model):
    title = models.CharField(max_length=10)
    name = models.CharField(max_length=60)
    sex = models.CharField(max_length=10)
    cls = models.CharField(max_length=10)
    age = models.IntegerField()
    family = models.CharField(max_length=10, default='NaN')
    fare = models.IntegerField()
    result = models.IntegerField(default='000000')

    class Meta:
        db_table = 'titanic'

    def __str__(self):
        return self.name
