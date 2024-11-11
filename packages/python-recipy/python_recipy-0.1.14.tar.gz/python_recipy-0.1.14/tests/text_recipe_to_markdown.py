from recipy.markdown import recipe_from_markdown, recipe_to_markdown
from recipy.models import Recipe, IngredientGroup, InstructionGroup


def test_minimal_recipe_to_markdown():
    recipe = Recipe(
        title="Simple Recipe",
        description=None,
        ingredient_groups=[
            IngredientGroup(
                title=None,
                ingredients=["1 cup water", "2 tbsp sugar"]
            )
        ],
        instruction_groups=[
            InstructionGroup(
                title=None,
                instructions=["Mix ingredients", "Serve"]
            )
        ],
        notes=None,
        reviews=[],
        image_urls=[],
        rating=None,
        meta=None
    )

    expected_markdown = """# Simple Recipe

## Ingredients

* 1 cup water
* 2 tbsp sugar

## Instructions

1. Mix ingredients
2. Serve
"""

    assert recipe_to_markdown(recipe) == expected_markdown


def test_recipe_with_description_to_markdown():
    recipe = Recipe(
        title="Tasty Recipe",
        description="A delicious traditional recipe.",
        ingredient_groups=[
            IngredientGroup(
                title=None,
                ingredients=["1 cup flour", "2 eggs"]
            )
        ],
        instruction_groups=[
            InstructionGroup(
                title=None,
                instructions=["Mix well", "Bake"]
            )
        ],
        notes=None,
        reviews=[],
        image_urls=[],
        rating=None,
        meta=None
    )

    expected_markdown = """# Tasty Recipe

A delicious traditional recipe.

## Ingredients

* 1 cup flour
* 2 eggs

## Instructions

1. Mix well
2. Bake
"""

    assert recipe_to_markdown(recipe) == expected_markdown


def test_recipe_with_single_image_to_markdown():
    recipe = Recipe(
        title="Photo Recipe",
        description=None,
        ingredient_groups=[
            IngredientGroup(
                title=None,
                ingredients=["1 cup milk"]
            )
        ],
        instruction_groups=[
            InstructionGroup(
                title=None,
                instructions=["Pour"]
            )
        ],
        notes=None,
        reviews=[],
        image_urls=["/images/recipe.jpg"],
        rating=None,
        meta=None
    )

    expected_markdown = """# Photo Recipe

![Photo Recipe](/images/recipe.jpg)

## Ingredients

* 1 cup milk

## Instructions

1. Pour
"""

    assert recipe_to_markdown(recipe) == expected_markdown


def test_recipe_with_description_and_image_to_markdown():
    recipe = Recipe(
        title="Photo Recipe",
        description="A great recipe with photo.",
        ingredient_groups=[
            IngredientGroup(
                title=None,
                ingredients=["1 cup milk"]
            )
        ],
        instruction_groups=[
            InstructionGroup(
                title=None,
                instructions=["Pour"]
            )
        ],
        notes=None,
        reviews=[],
        image_urls=["/images/recipe.jpg"],
        rating=None,
        meta=None
    )

    expected_markdown = """# Photo Recipe

A great recipe with photo.

![Photo Recipe](/images/recipe.jpg)

## Ingredients

* 1 cup milk

## Instructions

1. Pour
"""

    assert recipe_to_markdown(recipe) == expected_markdown


def test_recipe_with_grouped_ingredients_to_markdown():
    recipe = Recipe(
        title="Grouped Recipe",
        description=None,
        ingredient_groups=[
            IngredientGroup(
                title="Wet Ingredients",
                ingredients=["1 cup milk", "2 eggs"]
            ),
            IngredientGroup(
                title="Dry Ingredients",
                ingredients=["2 cups flour", "1 tsp salt"]
            )
        ],
        instruction_groups=[
            InstructionGroup(
                title=None,
                instructions=["Mix wet ingredients", "Add dry ingredients"]
            )
        ],
        notes=None,
        reviews=[],
        image_urls=[],
        rating=None,
        meta=None
    )

    expected_markdown = """# Grouped Recipe

## Ingredients

### Wet Ingredients

* 1 cup milk
* 2 eggs

### Dry Ingredients

* 2 cups flour
* 1 tsp salt

## Instructions

1. Mix wet ingredients
2. Add dry ingredients
"""

    assert recipe_to_markdown(recipe) == expected_markdown


def test_recipe_with_grouped_instructions_to_markdown():
    recipe = Recipe(
        title="Grouped Recipe",
        description=None,
        ingredient_groups=[
            IngredientGroup(
                title=None,
                ingredients=["1 cup flour", "1 egg"]
            )
        ],
        instruction_groups=[
            InstructionGroup(
                title="Preparation",
                instructions=["Mix ingredients", "Let rest"]
            ),
            InstructionGroup(
                title="Cooking",
                instructions=["Heat pan", "Cook mixture"]
            )
        ],
        notes=None,
        reviews=[],
        image_urls=[],
        rating=None,
        meta=None
    )

    expected_markdown = """# Grouped Recipe

## Ingredients

* 1 cup flour
* 1 egg

## Instructions

### Preparation

1. Mix ingredients
2. Let rest

### Cooking

1. Heat pan
2. Cook mixture
"""

    assert recipe_to_markdown(recipe) == expected_markdown


def test_recipe_with_notes_to_markdown():
    recipe = Recipe(
        title="Recipe With Notes",
        description=None,
        ingredient_groups=[
            IngredientGroup(
                title=None,
                ingredients=["1 cup flour"]
            )
        ],
        instruction_groups=[
            InstructionGroup(
                title=None,
                instructions=["Mix well"]
            )
        ],
        notes="Store in an airtight container.",
        reviews=[],
        image_urls=[],
        rating=None,
        meta=None
    )

    expected_markdown = """# Recipe With Notes

## Ingredients

* 1 cup flour

## Instructions

1. Mix well

## Notes

Store in an airtight container.
"""

    assert recipe_to_markdown(recipe) == expected_markdown


def test_round_trip_conversion():
    """Test that converting markdown to recipe and back to markdown preserves structure"""
    original_markdown = """# Complete Recipe

A wonderful recipe to try.

![Complete Recipe](/images/recipe.jpg)

## Ingredients

### Wet Ingredients

* 1 cup milk
* 2 eggs

### Dry Ingredients

* 2 cups flour
* 1 tsp salt

## Instructions

### Preparation

1. Mix wet ingredients
2. Add dry ingredients gradually

### Cooking

1. Heat oven to 350°F
2. Bake for 30 minutes

## Notes

Best served warm."""

    # Convert markdown to recipe
    recipe = recipe_from_markdown(original_markdown)
    assert recipe is not None

    # Convert recipe back to markdown
    generated_markdown = recipe_to_markdown(recipe)

    # Convert generated markdown back to recipe to compare structure
    final_recipe = recipe_from_markdown(generated_markdown)
    assert final_recipe is not None

    # Compare structure of original and final recipe
    assert recipe.title == final_recipe.title
    assert recipe.description == final_recipe.description
    assert recipe.notes == final_recipe.notes
    assert recipe.image_urls == final_recipe.image_urls

    # Compare ingredient groups
    assert len(recipe.ingredient_groups) == len(final_recipe.ingredient_groups)
    for orig_group, final_group in zip(recipe.ingredient_groups, final_recipe.ingredient_groups):
        assert orig_group.title == final_group.title
        assert orig_group.ingredients == final_group.ingredients

    # Compare instruction groups
    assert len(recipe.instruction_groups) == len(final_recipe.instruction_groups)
    for orig_group, final_group in zip(recipe.instruction_groups, final_recipe.instruction_groups):
        assert orig_group.title == final_group.title
        assert orig_group.instructions == final_group.instructions
