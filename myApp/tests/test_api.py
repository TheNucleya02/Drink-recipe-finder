import pytest
from django.urls import reverse
from rest_framework import status
from myApp.models import Favorite


@pytest.mark.django_db
class TestRecipeAPI:

    def test_list_recipes(self, api_client, recipe):
        url = reverse("api:recipes-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["title"] == recipe.title

    def test_search_recipes(self, api_client, recipe):
        # Search for 'Test'
        url = reverse("api:recipes-list") + "?search=Test"
        response = api_client.get(url)
        assert len(response.data["results"]) == 1

        # Search for 'NonExistent'
        url = reverse("api:recipes-list") + "?search=NonExistent"
        response = api_client.get(url)
        assert len(response.data["results"]) == 0

    def test_favorite_action_unauthenticated(self, api_client, recipe):
        url = reverse("api:recipes-favorite", kwargs={"pk": recipe.pk})
        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_favorite_toggle(self, api_client, user, recipe):
        # Login
        api_client.force_authenticate(user=user)
        url = reverse("api:recipes-favorite", kwargs={"pk": recipe.pk})

        # 1. Add to favorite
        response = api_client.post(url)
        assert response.status_code == status.HTTP_201_CREATED
        assert Favorite.objects.filter(user=user, recipe=recipe).exists()

        # 2. Remove from favorite (Toggle)
        response = api_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert not Favorite.objects.filter(user=user, recipe=recipe).exists()
