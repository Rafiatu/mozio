from django.db import models


class Coordinate(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"[{self.latitude}, {self.longitude}]"
