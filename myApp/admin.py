from django.contrib import admin
from .models import Category, Rating, Recipe, Ingredient, Favorite, RecipeIngredient


admin.site.register(RecipeIngredient)
admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Favorite)
