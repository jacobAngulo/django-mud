from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=999999999)
    token = models.CharField(max_length=999999999)
    gold = models.FloatField()
    encumbrance = models.FloatField()
    visited = models.CharField(max_length=999999999)
    path = models.CharField(max_length=999999999, default='')
