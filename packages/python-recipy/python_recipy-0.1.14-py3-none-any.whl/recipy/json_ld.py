import html
import json
from typing import Optional, List, Dict, Union

import httpx
from bs4 import BeautifulSoup

from . import utils
from .models import Recipe, IngredientGroup, Rating, Meta, InstructionGroup, Review


def recipe_from_url(url: str) -> Optional[Union[Recipe, str]]:
    """
    Fetches a recipe from the given URL, parses the webpage content, and extracts the recipe information.

    :param url: The URL of the webpage containing the recipe
    :type url: str
    :returns: A `Recipe` object if the recipe is successfully parsed, or a string containing the recipe text if JSON-LD is not available. Returns `None` if neither is found
    :rtype: Optional[Union[Recipe, str]]
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Referer': 'https://www.google.com/'
    }

    with httpx.Client() as client:
        response = client.get(url, headers=headers)
        response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    if not soup:
        raise ValueError("Failed to parse the recipe page.")

    recipe_json = _extract_recipe_json(soup)

    if recipe_json:
        recipe = recipe_from_json(recipe_json)
        if recipe:
            return recipe

    recipe_text = _extract_recipe_text(soup)
    if not recipe_text:
        return None
    return recipe_text


def recipe_from_json(json_data: Union[str, Dict]) -> Optional[Recipe]:
    """
    Parses JSON-LD data and converts it into a `Recipe` object.

    :param json_data: The JSON-LD data as a string or a dictionary
    :type json_data: Union[str, Dict]
    :returns: A `Recipe` object if parsing is successful, otherwise `None`
    :rtype: Optional[Recipe]
    """
    if isinstance(json_data, str):
        try:
            recipe = json.loads(json_data)
        except json.JSONDecodeError:
            raise ValueError("Failed to parse JSON.")
    else:
        recipe = json_data

    recipe_title = _get_title(recipe)
    if not recipe_title:
        print('No title found')
        return None

    recipe_ingredients = _get_ingredients(recipe)

    recipe_instruction_groups = _get_instruction_groups(recipe)

    return Recipe(
        title=recipe_title,
        description=_get_description(recipe),
        image_urls=_get_image_urls(recipe),
        ingredient_groups=[IngredientGroup(title=None, ingredients=recipe_ingredients)],
        instruction_groups=recipe_instruction_groups,
        reviews=_get_reviews(recipe),
        rating=Rating(value=_get_rating_value(recipe), count=_get_rating_count(recipe)),
        meta=Meta(
            prep_time_minutes=_get_prep_time_minutes(recipe),
            cook_time_minutes=_get_cook_time_minutes(recipe),
            total_time_minutes=_get_total_time_minutes(recipe),
            recipe_yield=_get_recipe_yield(recipe)
        ),
        notes=_get_notes(recipe)
    )


def recipe_to_json(recipe: Recipe) -> str:
    """
    Converts a `Recipe` object into a JSON-LD formatted string.

    :param recipe: The `Recipe` object to be converted
    :type recipe: Recipe
    :returns: A JSON-LD formatted string representing the recipe
    :rtype: str
    """
    recipe_json_ld = {
        "@context": "https://schema.org/",
        "@type": "Recipe",
        "name": recipe.title,
        "description": recipe.description,
        "image": recipe.image_urls,
        "recipeIngredient": [
            ingredient
            for group in recipe.ingredient_groups
            for ingredient in group.ingredients
        ],
        "recipeInstructions": [
            {
                "@type": "HowToStep",
                "text": instruction
            }
            for group in recipe.instruction_groups
            for instruction in group.instructions
        ],
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": recipe.rating.value if recipe.rating else 0,
            "ratingCount": recipe.rating.count if recipe.rating else 0
        } if recipe.rating else None,
        "prepTime": f"PT{recipe.meta.prep_time_minutes}M" if recipe.meta and recipe.meta.prep_time_minutes else None,
        "cookTime": f"PT{recipe.meta.cook_time_minutes}M" if recipe.meta and recipe.meta.cook_time_minutes else None,
        "totalTime": f"PT{recipe.meta.total_time_minutes}M" if recipe.meta and recipe.meta.total_time_minutes else None,
        "recipeYield": recipe.meta.recipe_yield if recipe.meta and recipe.meta.recipe_yield else None,
        "review": [
            {
                "@type": "Review",
                "author": review.author,
                "reviewBody": review.body,
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": review.rating
                } if review.rating else None
            }
            for review in recipe.reviews
        ],
        "comment": {
            "text": recipe.notes
        } if recipe.notes else None
    }

    # Remove keys with None values
    recipe_json_ld = {k: v for k, v in recipe_json_ld.items() if v is not None}

    return json.dumps(recipe_json_ld, indent=2)


def _extract_recipe_text(soup: BeautifulSoup) -> Optional[str]:
    recipe_text = soup.find('div', {'itemtype': 'https://schema.org/Recipe'})
    if recipe_text:
        return recipe_text.text

    return None


def _extract_recipe_json(soup: BeautifulSoup) -> Optional[Dict]:
    scripts = soup.find_all('script', {'type': 'application/ld+json'})
    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, list):
                for item in data:
                    if item.get("@type") == "Recipe" or "Recipe" in item.get("@type", []):
                        return item
            else:
                if data.get("@type") == "Recipe" or "Recipe" in data.get("@type", []):
                    return data
        except json.JSONDecodeError:
            print(f"Failed to parse JSON: {script.string}")
            continue
    return None


def _get_title(recipe: dict) -> Optional[str]:
    val = recipe.get("name")
    if val:
        val = html.unescape(val)
        val = val.strip()
    return val


def _get_url(recipe: dict) -> Optional[str]:
    url = recipe.get("url")
    if isinstance(url, str):
        return url
    main_entity_of_page = recipe.get("mainEntityOfPage")
    if isinstance(main_entity_of_page, dict):
        return main_entity_of_page.get("@id")
    id_ = recipe.get("@id")
    if id_ and id_.startswith("http"):
        return id_
    return None


def _get_description(recipe: dict) -> Optional[str]:
    val = recipe.get("description")
    if val:
        val = utils.clean_text(val)
    return val


def _get_image_urls(recipe: dict) -> List[str]:
    image = recipe.get("image")
    if not image:
        return []
    if isinstance(image, str):
        return [image]
    if isinstance(image, dict):
        return [image.get("url")]
    if isinstance(image, list):
        if all(isinstance(i, str) for i in image):
            return image
        if all(isinstance(i, dict) for i in image):
            return [i.get("url") for i in image]
    raise ValueError(f"Unexpected image type: {image}")


def _get_ingredients(recipe: dict) -> Optional[List[str]]:
    ingredients = recipe.get("recipeIngredient")
    if not ingredients:
        return None
    cleaned = []
    if isinstance(ingredients, list):
        for i in ingredients:
            i = utils.clean_text(i)
            cleaned.append(i)
    return cleaned


def _get_instruction_groups(recipe: dict) -> Optional[List[InstructionGroup]]:
    instructions_element = recipe.get("recipeInstructions")
    instruction_groups = []

    if isinstance(instructions_element, str):
        cleaned_instruction = utils.clean_text(instructions_element)
        if not instruction_groups:
            instruction_groups.append(InstructionGroup(title=None, instructions=[]))
        instruction_groups[0].instructions.append(cleaned_instruction)
    elif isinstance(instructions_element, list):
        for element in instructions_element:
            if isinstance(element, str):
                cleaned_instruction = utils.clean_text(element)
                if not instruction_groups:
                    instruction_groups.append(InstructionGroup(title=None, instructions=[]))
                instruction_groups[0].instructions.append(cleaned_instruction)
            elif isinstance(element, dict):
                element_type = element.get("@type")

                if element_type == "HowToStep":
                    step_text = utils.clean_text(element.get("text") or element.get("name"))
                    if not instruction_groups:
                        instruction_groups.append(InstructionGroup(title=None, instructions=[]))
                    instruction_groups[0].instructions.append(step_text)

                elif element_type == "HowToSection":
                    group_name = element.get("name")
                    item_list_element = element.get("itemListElement")
                    if item_list_element:
                        group_instructions = [utils.clean_text(instruction.get("text")) for instruction in
                                              item_list_element if instruction.get("text")]
                        instruction_groups.append(InstructionGroup(title=group_name, instructions=group_instructions))

    for group in instruction_groups:
        group.instructions = [i for i in group.instructions if i]
    instruction_groups = [group for group in instruction_groups if group.instructions]

    return instruction_groups if instruction_groups else None


def _get_rating_value(recipe: dict) -> float:
    aggregate_rating = recipe.get("aggregateRating")
    if isinstance(aggregate_rating, dict):
        rating_value_str = aggregate_rating.get("ratingValue")
        if isinstance(rating_value_str, str):
            try:
                rating_value = float(rating_value_str)
            except ValueError:
                rating_value = 0.0
        else:
            rating_value = aggregate_rating.get("ratingValue", 0.0)
    else:
        rating_value = 0.0
    return max(0.0, min(rating_value, 5.0))


def _get_rating_count(recipe: dict) -> int:
    aggregate_rating = recipe.get("aggregateRating")
    if isinstance(aggregate_rating, dict):
        rating_count_str = aggregate_rating.get("ratingCount")
        if isinstance(rating_count_str, str):
            try:
                rating_count = int(rating_count_str)
            except ValueError:
                rating_count = 0
        else:
            rating_count = aggregate_rating.get("ratingCount", 0)
    else:
        rating_count = 0
    return max(0, rating_count)


def _get_reviews(recipe: dict) -> List[Review]:
    reviews = []
    review_element = recipe.get("review")
    if isinstance(review_element, list):
        for review in review_element:
            if isinstance(review, str):
                reviews.append(Review(author="Anonymous", rating=0.0, body=utils.clean_text(review)))
            elif isinstance(review, dict):
                author = _get_review_author(review)
                rating = _get_review_rating(review)
                body = _get_review_body(review)
                if author or rating is not None or body:
                    reviews.append(Review(author=author, rating=rating, body=body))
            else:
                raise ValueError(f"Unknown review format: {review}")
    return reviews


def _get_review_author(review: dict) -> str:
    author_element = review.get("author")
    if isinstance(author_element, dict):
        return author_element.get("name", "Anonymous")
    elif isinstance(author_element, str):
        return author_element
    return "Anonymous"


def _get_review_rating(review: dict) -> Optional[float]:
    rating_element = review.get("reviewRating")
    if isinstance(rating_element, str):
        try:
            return float(rating_element)
        except ValueError:
            pass
    elif isinstance(rating_element, dict):
        rating_value_element = rating_element.get("ratingValue")
        if isinstance(rating_value_element, str):
            try:
                return float(rating_value_element)
            except ValueError:
                pass
        else:
            return rating_value_element
    elif isinstance(rating_element, (int, float)):
        return float(rating_element)
    return None


def _get_review_body(review: dict) -> Optional[str]:
    body = html.unescape(review.get("reviewBody", "")) if review.get("reviewBody") else None
    if body:
        if '<' in body:
            body = utils.strip_html(body)
        body = utils.normalize_fractions(body)
        body = utils.normalize_temperatures(body)
        body = utils.collapse_whitespace(body)
    return body


def _get_prep_time_minutes(recipe: dict) -> Optional[int]:
    prep_time_element = recipe.get("prepTime")
    if isinstance(prep_time_element, str):
        return utils.parse_time(prep_time_element)
    return None


def _get_cook_time_minutes(recipe: dict) -> Optional[int]:
    cook_time_element = recipe.get("cookTime")
    if isinstance(cook_time_element, str):
        return utils.parse_time(cook_time_element)
    return None


def _get_total_time_minutes(recipe: dict) -> Optional[int]:
    total_time_element = recipe.get("totalTime")
    if isinstance(total_time_element, str):
        return utils.parse_time(total_time_element)
    return None


def _get_recipe_yield(recipe: dict) -> Optional[str]:
    recipe_yield_element = recipe.get("recipeYield")
    if isinstance(recipe_yield_element, str):
        return recipe_yield_element
    if isinstance(recipe_yield_element, list):
        return recipe_yield_element[0]
    return None


def _get_notes(recipe: dict) -> Optional[str]:
    notes = recipe.get("comment")
    if isinstance(notes, str):
        return notes
    elif isinstance(notes, dict):
        return notes.get("text")
    else:
        return None
