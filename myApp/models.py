from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from decimal import Decimal


class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    recipe_id = models.PositiveIntegerField(unique=True)  # From the API
    title = models.CharField(max_length=255)
    instructions = models.TextField()
    picture_url = models.URLField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")

    def get_average_rating(self):
        ratings = self.ratings.all()
        if not ratings:
            return Decimal("0.0")
        else:
            total = sum(rating.rate for rating in ratings)
        return Decimal(round(total / len(ratings), 1))

    def get_rates_number(self):
        return len(self.ratings.all())

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipe_ingredients"
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100)
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = (("recipe", "ingredient"),)
        ordering = ["order"]  # Ensure the default ordering by the order field

    def __str__(self):
        return f"{self.amount} {self.ingredient.name} in {self.recipe.title}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favorites"
    )
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} added {self.recipe.title}"


class Rating(models.Model):
    rate = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MaxValueValidator(Decimal(5.0)), MinValueValidator(Decimal(1.0))],
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ratings")
    date = models.DateTimeField(auto_now=True)
    review = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        # We don't want a user gives more than one rating to a recipe
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "user"], name="unique_recipe_user_rating"
            )
        ]

    def __str__(self):
        return f"{self.user.username} rateed {self.rate} to {self.recipe.title}"
