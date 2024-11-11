import os
import json
from pathlib import Path

# Directory containing the JSON files
directory = Path('/tests/test_data')

# Loop through all JSON files in the directory
for json_file in directory.glob('*.json'):
    # Read the JSON content
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Extract the "recipe" object
    recipe_data = data.get('recipe', {})

    # Overwrite the file with the "recipe" object
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(recipe_data, file, indent=4, ensure_ascii=False)
