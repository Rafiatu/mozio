from django.db import models
from .coordinates_model import Coordinate
from .provider_model import Provider


class Polygon(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.ForeignKey(
        Provider,
        related_name="provider",
        verbose_name="provider",
        on_delete=models.CASCADE,
    )
    coordinates = models.ManyToManyField(
        Coordinate, related_name="coordinates", verbose_name="coordinates", blank=True
    )
    type = models.CharField(max_length=7, editable=False, default="Polygon")

    def __str__(self) -> str:
        return self.name
