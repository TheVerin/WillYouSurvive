from django.db import models


class Titanic(models.Model):
    title = models.CharField(max_length=20)
    name = models.CharField(max_length=60)
    sex = models.CharField(max_length=20)
    cls = models.CharField(max_length=20)
    family = models.CharField(max_length=20, default='NaN')
    fare = models.IntegerField()
    result = models.IntegerField(default='000000')
    age = models.IntegerField()

    class Meta:
        db_table = 'titanic'

    def __str__(self):
        return self.name
