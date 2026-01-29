from . import api_views
from django.urls import path, include
from rest_framework.routers import DefaultRouter


app_name = "myApp"

router = DefaultRouter()
router.register(r"recipes", api_views.RecipeViewset, basename="recipes")

urlpatterns = [
    path("", include(router.urls)),
]
