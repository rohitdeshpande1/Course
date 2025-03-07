from django.shortcuts import render
from rest_framework import generics, serializers
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from .serializers import IngredientSerializer, MenuItemSerializer, RecipeRequirementSerializer, PurchaseSerializer
from rest_framework.permissions import IsAuthenticated

class IngredientListCreateView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticated]

class MenuItemListCreateView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

class RecipeRequirementListCreateView(generics.ListCreateAPIView):
    queryset = RecipeRequirement.objects.all()
    serializer_class = RecipeRequirementSerializer
    permission_classes = [IsAuthenticated]

class PurchaseListCreateView(generics.ListCreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        purchase = serializer.save()
        recipe_requirements = RecipeRequirement.objects.filter(menu_item=purchase.menu_item)
        for requirement in recipe_requirements:
            ingredient = requirement.ingredient
            if ingredient.quantity < requirement.quantity_required:
                raise serializers.ValidationError(f"Not enough {ingredient.name} in stock!")
            ingredient.quantity -= requirement.quantity_required
            ingredient.save()
