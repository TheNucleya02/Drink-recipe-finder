import pytest
from decimal import Decimal
from myApp.models import Rating, Favorite
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestModels:

    def test_recipe_string_representation(self, recipe):
        assert str(recipe) == "Test Drink"

    def test_average_rating_calculation(self, recipe, user):
        # Create two ratings
        Rating.objects.create(recipe=recipe, user=user, rate=Decimal(5.0))

        user2 = User.objects.create_user(username="u2", password="p")
        Rating.objects.create(recipe=recipe, user=user2, rate=Decimal(3.0))

        # (5 + 3) / 2 = 4.0
        assert recipe.get_average_rating() == Decimal("4.0")
        assert recipe.get_rates_number() == 2

    def test_average_rating_empty(self, recipe):
        # Should return 0.0 if no ratings exist
        assert recipe.get_average_rating() == Decimal("0.0")

    def test_favorite_creation(self, user, recipe):
        fav = Favorite.objects.create(user=user, recipe=recipe)
        assert str(fav) == f"{user.username} added {recipe.title}"
