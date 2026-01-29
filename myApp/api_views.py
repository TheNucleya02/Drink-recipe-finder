from django.shortcuts import get_object_or_404

from .models import Recipe, Favorite
from .serializers import RecipeSerializer, FavoriteSerializer

from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action


class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by("id")
    serializer_class = RecipeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "ingredients__name"]

    # TODO: Users can filter like this:
    # http://127.0.0.1:8000/api/v1/recipes/?search=Sprite

    @action(detail=True, methods=["post"])
    def favorite(self, request, pk):
        if not request.user.is_authenticated:
            return Response(
                {"Auth": "You must be logged in to perform this action."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        recipe = get_object_or_404(Recipe, pk=pk)
        fav = Favorite.objects.filter(user=request.user, recipe=recipe)
        if fav.exists():
            fav.delete()
            return Response(
                {"Unfavorite": "The recipe has been deleted from your favorite list."},
                status=status.HTTP_200_OK,
            )

        new_fav = Favorite.objects.create(user=request.user, recipe=recipe)
        serializer = FavoriteSerializer(new_fav)
        return Response({"Favorite": serializer.data}, status=status.HTTP_201_CREATED)
