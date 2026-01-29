import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from myApp.models import Category, Ingredient, Recipe, RecipeIngredient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="password")


@pytest.fixture
def category(db):
    return Category.objects.create(name="Cocktails")


@pytest.fixture
def ingredient(db):
    return Ingredient.objects.create(name="Lemon")


@pytest.fixture
def recipe(db, category, ingredient):
    recipe = Recipe.objects.create(
        recipe_id=12345,
        title="Test Drink",
        instructions="Mix it.",
        picture_url="http://test.com/img.jpg",
        category=category,
    )
    # Add ingredient connection
    RecipeIngredient.objects.create(
        recipe=recipe, ingredient=ingredient, amount="1 oz", order=1
    )
    return recipe
