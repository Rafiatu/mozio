from rest_framework.routers import SimpleRouter, DefaultRouter
from .views import *


router = DefaultRouter()
router.register(r"locations", LocationsView, basename="polygons")
router.register(r"providers", ProvidersView, basename="providers")
urlpatterns = router.urls
