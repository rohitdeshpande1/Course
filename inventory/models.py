from django.db import models
from django.contrib.auth.models import User

class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)
    quantity = models.FloatField()
    price_per_unit = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_required = models.FloatField()

class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        recipe_requirements = RecipeRequirement.objects.filter(menu_item=self.menu_item)
        for requirement in recipe_requirements:
            ingredient = requirement.ingredient
            if ingredient.quantity < requirement.quantity_required:
                raise ValueError(f"Not enough {ingredient.name} in stock!")
            ingredient.quantity -= requirement.quantity_required
            ingredient.save()
        super().save(*args, **kwargs)

