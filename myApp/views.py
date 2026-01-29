from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
import requests
from django.contrib import messages
from django.core.cache import cache

from .models import RecipeIngredient, Category, Recipe, Ingredient, Favorite, Rating
from .forms import RatingForm


# Create your views here.
class IndexView(generic.TemplateView):
    template_name = "myApp/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Look for 'random_drink' in the cache
        drink = cache.get("random_drink")

        if not drink:
            try:
                response = requests.get(
                    "https://www.thecocktaildb.com/api/json/v1/1/random.php"
                )
                response.raise_for_status()
                data = response.json()
                drink = data["drinks"][0]

                # Store it for 5 minutes (300 seconds)
                cache.set("random_drink", drink, 300)
            except Exception:
                messages.warning(self.request, "Check your internet connection.")
                drink = None

        context["drink"] = drink
        return context


class SearchView(generic.TemplateView):
    template_name = "myApp/search.html"

    def get(self, request, *args, **kwargs):
        query = request.GET.get("query")
        drinks = None

        if query:
            # Create a unique key for every search term
            cache_key = f"search_res_{query.lower().strip()}"
            drinks = cache.get(cache_key)

            if not drinks:
                url = (
                    f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={query}"
                )
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    drinks = response.json().get("drinks")

                    if drinks:
                        # Cache successful search results for 1 hour
                        cache.set(cache_key, drinks, 3600)
                    else:
                        drinks = {"error": "No drinks found!"}
                except Exception:
                    drinks = {"error": "API Error!"}

        return render(request, self.template_name, {"query": query, "drinks": drinks})


def add_to_favorite(request, pk):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={pk}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        drink = response.json()["drinks"][0]
        if not drink:  # Handle case where no drinks are found
            drink = {"error": "No drinks found for this search!"}
    except:  # noqa
        drink = {"error": "An Error happened!!! Try Another Time!"}

    if drink:
        if Recipe.objects.filter(recipe_id=drink["idDrink"]).exists():
            print("we've already had this item in the database.")
            recipe = get_object_or_404(Recipe, recipe_id=drink["idDrink"])
            if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
                messages.warning(request, "You've already added this item before!")
                return redirect("myApp:my_favorites")

            Favorite.objects.create(user=request.user, recipe=recipe)
            messages.success(request, "Recipe has been added successfully")
            return redirect("myApp:my_favorites")

        else:
            print("we don't have this drink in the database and we should add it.")
            # First we get or create the category
            drink_category, _ = Category.objects.get_or_create(
                name=drink["strCategory"]
            )

            # Then add the recipe
            recipe = Recipe.objects.create(
                recipe_id=drink["idDrink"],
                title=drink["strDrink"],
                instructions=drink["strInstructions"],
                category=drink_category,
                picture_url=drink["strDrinkThumb"],
            )

            # then the ingredients and amounts through RecipeIngredient Model
            # first we get the ingredients, amounts and orders
            ingredients_list = []
            amounts_list = []
            order_list = []
            for number in range(1, 16):
                if (
                    drink[f"strMeasure{number}"] is None
                    or drink[f"strIngredient{number}"] is None
                ):
                    break
                else:
                    ingredients_list.append(drink[f"strIngredient{number}"])
                    amounts_list.append(drink[f"strMeasure{number}"])
                    order_list.append(number)

            # Then we add them in the database through RecipeIngredient Model
            for index in range(len(amounts_list)):
                # get or create the ingredient
                ingredient, _ = Ingredient.objects.get_or_create(
                    name=ingredients_list[index]
                )
                # record the recipeIngredient
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=amounts_list[index],
                    order=order_list[index],
                )

            # add it to user's favorite
            Favorite.objects.create(user=request.user, recipe=recipe)
    messages.success(request, "Recipe has been added successfully")
    return redirect("myApp:my_favorites")


def my_favorites(request):
    favorite_list = Favorite.objects.filter(user=request.user)
    return render(request, "myApp/my_favorites.html", {"favorites": favorite_list})


def delete_favorite(request, pk):
    favorite = get_object_or_404(Favorite, pk=pk)
    favorite.delete()
    messages.success(request, "Recipe has been deleted successfully")
    return redirect("myApp:my_favorites")


class RatingFormView(generic.FormView):
    model = Rating
    form_class = RatingForm
    success_url = reverse_lazy("my_favorites")
    template_name = "myApp/rating_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        print(pk)
        context["recipe"] = get_object_or_404(Recipe, pk=pk)
        print(context["recipe"])
        return context

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        print(pk)

        recipe = get_object_or_404(Recipe, pk=pk)
        # Update if exists, or create a new entry
        rating, created = Rating.objects.update_or_create(
            recipe=recipe,
            user=self.request.user,
            defaults={"rate": form.cleaned_data["rate"]},
        )
        if created:
            messages.success(self.request, "Rating added successfully!")
        else:
            messages.success(self.request, "Rating updated successfully!")
        return redirect("myApp:my_favorites")


class MyFavoriteDetailView(generic.DetailView):
    model = Favorite
    template_name = "myApp/detail_favorite.html"
