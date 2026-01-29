import pytest
from django.urls import reverse
from unittest.mock import patch
from myApp.models import Recipe, Favorite, Ingredient


@pytest.mark.django_db
class TestStandardViews:

    @patch("myApp.views.requests.get")
    def test_index_view_success(self, mock_get, client):
        # Mock the external API response
        mock_response = {"drinks": [{"strDrink": "Mojito", "strDrinkThumb": "url"}]}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        url = reverse("myApp:index")
        response = client.get(url)

        assert response.status_code == 200
        assert response.context["drink"] == mock_response["drinks"][0]

    @patch("myApp.views.requests.get")
    def test_search_view(self, mock_get, client):
        mock_response = {"drinks": [{"strDrink": "Margarita"}]}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        url = reverse("myApp:search") + "?query=Margarita"
        response = client.get(url)

        assert response.status_code == 200
        assert response.context["drinks"] == mock_response["drinks"]

    def test_my_favorites_view(self, client, user, recipe):
        client.force_login(user)
        Favorite.objects.create(user=user, recipe=recipe)

        url = reverse("myApp:my_favorites")
        response = client.get(url)

        assert response.status_code == 200
        assert recipe in [f.recipe for f in response.context["favorites"]]

    # --- Testing Complex "Add to Favorite" Logic ---

    @patch("myApp.views.requests.get")
    def test_add_to_favorite_new_recipe(self, mock_get, client, user):
        """Test adding a recipe that does NOT exist in our DB yet"""
        client.force_login(user)

        # 1. Create base mock data
        mock_drink_data = {
            "idDrink": "99999",
            "strDrink": "New Cocktail",
            "strCategory": "Punch",
            "strInstructions": "Mix it.",
            "strDrinkThumb": "http://img.com",
            # Add the first ingredient
            "strIngredient1": "Rum",
            "strMeasure1": "2 oz",
        }

        # 2. Fill keys 2 through 15 with None (to match real API behavior)
        for i in range(2, 16):
            mock_drink_data[f"strIngredient{i}"] = None
            mock_drink_data[f"strMeasure{i}"] = None

        # 3. Setup the mock response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"drinks": [mock_drink_data]}

        # 4. Call the view
        url = reverse("myApp:add_favorite", kwargs={"pk": 99999})
        response = client.get(url, follow=True)

        # 5. Assertions
        assert Recipe.objects.filter(recipe_id=99999).exists()
        assert Ingredient.objects.filter(name="Rum").exists()
        new_recipe = Recipe.objects.get(recipe_id=99999)
        assert Favorite.objects.filter(user=user, recipe=new_recipe).exists()

        # Check Redirect
        assert response.redirect_chain[0][0] == reverse("myApp:my_favorites")

    def test_delete_favorite(self, client, user, recipe):
        client.force_login(user)
        fav = Favorite.objects.create(user=user, recipe=recipe)

        url = reverse("myApp:delete_favorite", kwargs={"pk": fav.pk})
        response = client.get(url, follow=True)

        assert not Favorite.objects.filter(pk=fav.pk).exists()
        assert "Recipe has been deleted successfully" in [
            m.message for m in list(response.context["messages"])
        ]
