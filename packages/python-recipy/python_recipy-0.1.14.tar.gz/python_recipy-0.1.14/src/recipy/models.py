from typing import Optional, List
from pydantic import BaseModel, Field


class IngredientGroup(BaseModel):
    """
    Represents a group of ingredients in a recipe.

    Attributes:
        title (Optional[str]): The title of the ingredient group, if any.
        ingredients (List[str]): A list of ingredients in this group.
    """
    title: Optional[str]
    ingredients: List[str]


class InstructionGroup(BaseModel):
    """
    Represents a group of instructions in a recipe.

    Attributes:
        title (Optional[str]): The title of the instruction group, if any.
        instructions (List[str]): A list of instructions in this group.
    """
    title: Optional[str]
    instructions: List[str]


class Review(BaseModel):
    """
    Represents a review of a recipe.

    Attributes:
        author (Optional[str]): The name of the review's author.
        body (Optional[str]): The content of the review.
        rating (Optional[float]): The rating given in the review.
    """
    author: Optional[str]
    body: Optional[str]
    rating: Optional[float]


class Meta(BaseModel):
    """
    Represents metadata for a recipe.

    Attributes:
        prep_time_minutes (Optional[int]): The preparation time in minutes.
        cook_time_minutes (Optional[int]): The cooking time in minutes.
        total_time_minutes (Optional[int]): The total time in minutes.
        recipe_yield (Optional[str]): The yield or serving size of the recipe.
    """
    prep_time_minutes: Optional[int]
    cook_time_minutes: Optional[int]
    total_time_minutes: Optional[int]
    recipe_yield: Optional[str]


class Rating(BaseModel):
    """
    Represents the rating information for a recipe.

    :ivar value: The average rating value, defaulting to 0
    :type value: Optional[float]
    :ivar count: The number of ratings, defaulting to 0
    :type count: Optional[int]
    """
    value: Optional[float] = Field(0)
    count: Optional[int] = Field(0)


class Recipe(BaseModel):
    """
    Represents a recipe.

    :ivar title: The title of the recipe
    :type title: str
    :ivar description: A description of the recipe
    :type description: Optional[str]
    :ivar ingredient_groups: A list of ingredient groups in the recipe, defaulting to an empty list
    :type ingredient_groups: Optional[List[IngredientGroup]]
    :ivar instruction_groups: A list of instruction groups in the recipe, defaulting to an empty list
    :type instruction_groups: Optional[List[InstructionGroup]]
    :ivar notes: Any additional notes for the recipe
    :type notes: Optional[str]
    :ivar reviews: A list of reviews for the recipe, defaulting to an empty list
    :type reviews: List[Review]
    :ivar image_urls: A list of image URLs associated with the recipe, defaulting to an empty list
    :type image_urls: List[str]
    :ivar rating: The rating information for the recipe
    :type rating: Optional[Rating]
    :ivar meta: The metadata associated with the recipe
    :type meta: Optional[Meta]
    """
    title: str
    description: Optional[str]
    ingredient_groups: Optional[List[IngredientGroup]] = Field(default_factory=list)
    instruction_groups: Optional[List[InstructionGroup]] = Field(default_factory=list)
    notes: Optional[str] = None
    reviews: List[Review] = Field(default_factory=list)
    image_urls: List[str] = Field(default_factory=list)
    rating: Optional[Rating] = None
    meta: Optional[Meta] = None
