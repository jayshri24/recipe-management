import graphene
import graphql_jwt
from .models import Ingredient, Recipe
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from .serializers import IngredientSerializer, RecipeSerializer

class IngredientInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name")


class RecipeType(DjangoObjectType):
    ingredient_count = graphene.Int()

    class Meta:
        model = Recipe
        fields = ("id", "title", "ingredients")

    def resolve_ingredient_count(self, info):
        return self.ingredients.count()


class Query(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType, 
                                    name=graphene.String(),
                                    limit=graphene.Int(),
                                    offset=graphene.Int())
    all_recipes = graphene.List(RecipeType)

    @login_required
    def resolve_all_ingredients(self, info, name=None,limit=None, offset=None):
        qs = Ingredient.objects.all()
        if name:
            qs = qs.filter(name__icontains=name)
        if offset is not None:
            qs = qs[offset:]
        if limit is not None:
            qs = qs[:limit]
        return qs

    @login_required
    def resolve_all_recipes(self, info):
        return Recipe.objects.all()


class CreateIngredient(graphene.Mutation):
    ingredient = graphene.Field(IngredientType)

    class Arguments:
        name = graphene.String(required=True)

    @login_required
    def mutate(self, info, name):
        data = {'name': name}
        serializer = IngredientSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        ingredient = serializer.save()
        return CreateIngredient(ingredient=ingredient)


class UpdateIngredient(graphene.Mutation):
    ingredient = graphene.Field(IngredientType)

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()

    @login_required
    def mutate(self, info, id, name=None):
        ingredient = Ingredient.objects.get(pk=id)
        data = {'name': name} if name else {}
        serializer = IngredientSerializer(ingredient, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        ingredient = serializer.save()
        return UpdateIngredient(ingredient=ingredient)


class DeleteIngredient(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, id):
        try:
            Ingredient.objects.get(pk=id).delete()
            return DeleteIngredient(ok=True)
        except Ingredient.DoesNotExist:
            return DeleteIngredient(ok=False)
        

class CreateRecipe(graphene.Mutation):
    recipe = graphene.Field(RecipeType)

    class Arguments:
        title = graphene.String(required=True)
        ingredients = graphene.List(graphene.NonNull(IngredientInput), required=True) 

    @login_required
    def mutate(self, info, title, ingredients):
        data = {
            'title': title,
            'ingredients': [dict(ingredient) for ingredient in ingredients]  
        }
        serializer = RecipeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()
        return CreateRecipe(recipe=recipe)

class AddIngredientsToRecipe(graphene.Mutation):
    recipe = graphene.Field(RecipeType)

    class Arguments:
        recipe_id = graphene.ID(required=True)
        ingredient_ids = graphene.List(graphene.ID, required=True)

    @login_required
    def mutate(self, recipe_id, ingredient_ids):
        recipe = Recipe.objects.get(pk=recipe_id)
        ingredients = Ingredient.objects.filter(id__in=ingredient_ids)
        recipe.ingredients.add(*ingredients)
        return AddIngredientsToRecipe(recipe=recipe)


class RemoveIngredientsFromRecipe(graphene.Mutation):
    recipe = graphene.Field(RecipeType)

    class Arguments:
        recipe_id = graphene.ID(required=True)
        ingredient_ids = graphene.List(graphene.ID, required=True)

    @login_required
    def mutate(self, recipe_id, ingredient_ids):
        recipe = Recipe.objects.get(pk=recipe_id)
        ingredients = Ingredient.objects.filter(id__in=ingredient_ids)
        recipe.ingredients.remove(*ingredients)
        return RemoveIngredientsFromRecipe(recipe=recipe)


class AuthMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()  
    verify_token = graphql_jwt.Verify.Field()            
    refresh_token = graphql_jwt.Refresh.Field()          


class Mutation(AuthMutation, graphene.ObjectType):
    create_ingredient = CreateIngredient.Field()
    update_ingredient = UpdateIngredient.Field()
    delete_ingredient = DeleteIngredient.Field()
    create_recipe = CreateRecipe.Field()
    add_ingredients_to_recipe = AddIngredientsToRecipe.Field()
    remove_ingredients_from_recipe = RemoveIngredientsFromRecipe.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
