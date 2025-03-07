from django.urls import path
from .views import IngredientListCreateView, MenuItemListCreateView, RecipeRequirementListCreateView, PurchaseListCreateView

urlpatterns = [
    path('ingredients/', IngredientListCreateView.as_view(), name='ingredient-list'),
    path('menu-items/', MenuItemListCreateView.as_view(), name='menu-item-list'),
    path('recipes/', RecipeRequirementListCreateView.as_view(), name='recipe-list'),
    path('purchases/', PurchaseListCreateView.as_view(), name='purchase-list'),
]
