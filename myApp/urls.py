from django.urls import path
from . import views

app_name = "myApp"

urlpatterns = [
    path("add_to_favorite/<int:pk>", views.add_to_favorite, name="add_favorite"),
    path("delete_favorite/<int:pk>/", views.delete_favorite, name="delete_favorite"),
    path("rating_form/<int:pk>/", views.RatingFormView.as_view(), name="rating_form"),
    path(
        "favorite_detail/<int:pk>/",
        views.MyFavoriteDetailView.as_view(),
        name="detail_favorite",
    ),
    path("search", views.SearchView.as_view(), name="search"),
    path("my_favorites/", views.my_favorites, name="my_favorites"),
    path("", views.IndexView.as_view(), name="index"),
]
