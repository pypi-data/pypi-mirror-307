from recipy.markdown import recipe_from_markdown


def test_minimal_recipe():
    markdown = """# Simple Recipe

## Ingredients

* 1 cup water
* 2 tbsp sugar

## Instructions

1. Mix ingredients
2. Serve
"""
    recipe = recipe_from_markdown(markdown)
    assert recipe is not None
    assert recipe.title == "Simple Recipe"
    assert recipe.description is None
    assert recipe.image_urls == []
    assert len(recipe.ingredient_groups) == 1
    assert recipe.ingredient_groups[0].ingredients == ["1 cup water", "2 tbsp sugar"]
    assert len(recipe.instruction_groups) == 1
    assert recipe.instruction_groups[0].instructions == ["Mix ingredients", "Serve"]


def test_recipe_with_description():
    markdown = """# Tasty Recipe

A delicious traditional recipe.

## Ingredients

* 1 cup flour
* 2 eggs

## Instructions

1. Mix well
2. Bake
"""
    recipe = recipe_from_markdown(markdown)
    assert recipe is not None
    assert recipe.title == "Tasty Recipe"
    assert recipe.description == "A delicious traditional recipe."
    assert recipe.image_urls == []


def test_recipe_with_single_image():
    markdown = """# Photo Recipe

![Recipe Photo](/images/recipe.jpg)

## Ingredients

* 1 cup milk

## Instructions

1. Pour
"""
    recipe = recipe_from_markdown(markdown)
    assert recipe is not None
    assert recipe.title == "Photo Recipe"
    assert recipe.description is None
    assert recipe.image_urls == ["/images/recipe.jpg"]


def test_recipe_with_description_and_single_image():
    markdown = """# Photo Recipe

A great recipe with photo.

![Recipe Photo](/images/recipe.jpg)

## Ingredients

* 1 cup milk

## Instructions

1. Pour
"""
    recipe = recipe_from_markdown(markdown)
    assert recipe is not None
    assert recipe.title == "Photo Recipe"
    assert recipe.description == "A great recipe with photo."
    assert recipe.image_urls == ["/images/recipe.jpg"]


def test_recipe_with_multiple_images():
    markdown = """# Multi Photo Recipe

![Recipe Photo 1](/images/recipe1.jpg)

![Recipe Photo 2](/images/recipe2.jpg)

## Ingredients

* 1 cup milk

## Instructions

1. Pour
"""
    recipe = recipe_from_markdown(markdown)
    assert recipe is not None
    assert recipe.title == "Multi Photo Recipe"
    assert recipe.description is None
    assert recipe.image_urls == ["/images/recipe1.jpg", "/images/recipe2.jpg"]


def test_recipe_with_description_and_multiple_images():
    markdown = """# Multi Photo Recipe

A recipe with multiple photos.

![Recipe Photo 1](/images/recipe1.jpg)

![Recipe Photo 2](/images/recipe2.jpg)

## Ingredients

* 1 cup milk

## Instructions

1. Pour
"""
    recipe = recipe_from_markdown(markdown)
    assert recipe is not None
    assert recipe.title == "Multi Photo Recipe"
    assert recipe.description == "A recipe with multiple photos."
    assert recipe.image_urls == ["/images/recipe1.jpg", "/images/recipe2.jpg"]


def test_recipe_with_grouped_ingredients():
    markdown = """# Grouped Recipe

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
    recipe = recipe_from_markdown(markdown)
    assert recipe is not None
    assert len(recipe.ingredient_groups) == 2
    assert recipe.ingredient_groups[0].title == "Wet Ingredients"
    assert recipe.ingredient_groups[0].ingredients == ["1 cup milk", "2 eggs"]
    assert recipe.ingredient_groups[1].title == "Dry Ingredients"
    assert recipe.ingredient_groups[1].ingredients == ["2 cups flour", "1 tsp salt"]


def test_recipe_with_grouped_instructions():
    markdown = """# Grouped Recipe

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
    recipe = recipe_from_markdown(markdown)
    assert recipe is not None
    assert len(recipe.instruction_groups) == 2
    assert recipe.instruction_groups[0].title == "Preparation"
    assert recipe.instruction_groups[0].instructions == ["Mix ingredients", "Let rest"]
    assert recipe.instruction_groups[1].title == "Cooking"
    assert recipe.instruction_groups[1].instructions == ["Heat pan", "Cook mixture"]


def test_recipe_with_notes():
    markdown = """# Recipe With Notes

## Ingredients

* 1 cup flour

## Instructions

1. Mix well

## Notes

Store in an airtight container.
"""
    recipe = recipe_from_markdown(markdown)
    assert recipe is not None
    assert recipe.notes == "Store in an airtight container."


def test_invalid_recipe_format():
    markdown = """This is not a recipe format

Just some random text."""
    recipe = recipe_from_markdown(markdown)
    assert recipe is None


def test_missing_ingredients():
    markdown = """# Invalid Recipe

## Instructions

1. Do something
"""
    recipe = recipe_from_markdown(markdown)
    assert recipe is None


def test_missing_instructions():
    markdown = """# Invalid Recipe

## Ingredients

* 1 cup flour
"""
    recipe = recipe_from_markdown(markdown)
    assert recipe is None


def test_empty_ingredient_group():
    markdown = """# Invalid Recipe

## Ingredients

### Empty Group

## Instructions

1. Do something
"""
    recipe = recipe_from_markdown(markdown)
    assert recipe is None


def test_empty_instruction_group():
    markdown = """# Invalid Recipe

## Ingredients

* 1 cup flour

## Instructions

### Empty Group
"""
    recipe = recipe_from_markdown(markdown)
    assert recipe is None
