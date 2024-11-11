import json
from pathlib import Path

import pytest

from recipy.json_ld import recipe_from_json


def get_test_data_files():
    """Get all JSON files from the test_data directory."""
    test_dir = Path(__file__).parent / "test_data"
    return sorted(test_dir.glob("*.json"))


@pytest.mark.parametrize("json_path", get_test_data_files(), ids=lambda p: p.name)
def test_parse_json_recipe(json_path: Path):
    """Test that each JSON recipe file can be parsed successfully."""
    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to decode JSON file {json_path.name}: {str(e)}")

    recipe = recipe_from_json(data)
    assert recipe is not None, f"Failed to parse recipe from {json_path.name}"

    # Basic validation of required fields
    assert recipe.title, f"Recipe from {json_path.name} is missing title"
    assert recipe.ingredient_groups, f"Recipe from {json_path.name} is missing ingredients"
    assert recipe.instruction_groups, f"Recipe from {json_path.name} is missing instructions"
