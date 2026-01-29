from rest_framework import serializers
from .models import Recipe, RecipeIngredient, Rating, Favorite, Category, Ingredient


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name"]


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ["id", "name"]


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ["id", "ingredient", "amount"]


class RatingSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = ["id", "rate", "user", "username", "date", "review"]

    def get_username(self, obj):
        return obj.user.username


class RecipeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    # recipe_ingredients is the related_name for
    # recipe foreinkey in RecipeIngredient Model
    recipe_ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    ratings = RatingSerializer(read_only=True, many=True)
    average_rate = serializers.SerializerMethodField()
    number_of_rates = serializers.SerializerMethodField()
    is_my_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            "id",
            "recipe_id",
            "title",
            "instructions",
            "picture_url",
            "is_my_favorite",
            "number_of_rates",
            "average_rate",
            "category",
            "recipe_ingredients",
            "ratings",
        ]

    def get_average_rate(self, obj):
        return obj.get_average_rating()

    def get_number_of_rates(self, obj):
        return obj.get_rates_number()

    def get_is_my_favorite(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return obj.favorites.filter(user=user).exists()
        return False


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ["id", "user", "recipe", "created_at"]
