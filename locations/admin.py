from django.contrib import admin
from locations.models import *
from rest_framework.authtoken.models import Token


# Register your models here.
admin.site.register(Provider)
admin.site.register(Coordinate)
admin.site.register(Polygon)
admin.site.register(Token)
