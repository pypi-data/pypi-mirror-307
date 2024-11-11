# Recipy

Recipy extracts recipes from web pages using JSON-LD and converts them into Python objects. It also supports generating
Markdown, LaTeX, and PDFs.

```python
from recipy.json_ld import recipe_from_url

recipe = recipe_from_url("https://www.allrecipes.com/recipe/14231/guacamole/")

if recipe:
    print(recipe.model_dump_json(indent=2))
```

## Installation

### Install via pip

```bash
pip install python-recipy
```

### Install `texlive` for PDF Generation

#### Debian/Ubuntu

```bash
sudo apt install texlive
```

#### macOS

```bash
brew install texlive
```

## Examples

### Load Recipe from JSON-LD

```python
from recipy.json_ld import recipe_from_json

json_data = '''
{
  "name": "Tomato Basil Salad",
  "description": "A simple and fresh tomato basil salad.",
  "recipeIngredient": [
    "2 ripe tomatoes, sliced",
    "1/4 cup fresh basil leaves, torn"
  ],
  "recipeInstructions": [
    {
      "@type": "HowToSection",
      "name": "Making the Salad",
      "itemListElement": [
        {
          "@type": "HowToStep",
          "text": "Arrange the tomato slices on a plate."
        },
        {
          "@type": "HowToStep",
          "text": "Scatter the torn basil leaves over the tomatoes."
        }
      ]
    },
    {
      "@type": "HowToSection",
      "name": "Preparing the Dressing",
      "itemListElement": [
        {
          "@type": "HowToStep",
          "text": "In a small bowl, whisk together the olive oil and balsamic vinegar."
        },
        {
          "@type": "HowToStep",
          "text": "Drizzle the dressing over the tomatoes and basil before serving."
        }
      ]
    }
  ],
  "comment": "Serve immediately for the best flavor."
}
'''

recipe = recipe_from_json(json_data)

if recipe:
    print(recipe.model_dump_json(indent=2))
```

See:

* [https://schema.org/Recipe](https://schema.org/Recipe)
* [https://json-ld.org/](https://json-ld.org/)

### Parse Recipe from Markdown

```python
from recipy.markdown import recipe_from_markdown

markdown_content = """
# Tomato Basil Salad

A simple and fresh tomato basil salad.

## Ingredients

### For the Salad

* 2 ripe tomatoes, sliced
* 1/4 cup fresh basil leaves, torn

### For the Dressing

* 2 tablespoons olive oil
* 1 tablespoon balsamic vinegar

## Instructions

### Making the Salad

1. Arrange the tomato slices on a plate.
2. Scatter the torn basil leaves over the tomatoes.

### Preparing the Dressing

1. In a small bowl, whisk together the olive oil and balsamic vinegar.
2. Drizzle the dressing over the tomatoes and basil before serving.

## Notes

Serve immediately for the best flavor.
"""

recipe = recipe_from_markdown(markdown_content)

if recipe:
    print(recipe.model_dump_json(indent=2))
```

#### Markdown Structure

* The recipe title must be an H1 (`# Title`).
* Ingredients must be under an H2 heading `## Ingredients`, with optional H3 subheadings for ingredient groups.
* Instructions must be under an H2 heading `## Instructions`, with optional H3 subheadings for instruction groups.
* Notes can be included under an H2 heading `## Notes`.

### Convert Recipe to JSON-LD

```python
from recipy.json_ld import recipe_from_url, recipe_to_json

recipe = recipe_from_url("https://www.allrecipes.com/recipe/14231/guacamole/")

if recipe:
    json_data = recipe_to_json(recipe)
    print(json_data)
```

### Convert Recipe to PDF

```python
from recipy.json_ld import recipe_from_url
from recipy.pdf import recipe_to_pdf, PdfOptions

recipe = recipe_from_url("https://www.allrecipes.com/recipe/14231/guacamole/")

if recipe:
    pdf_options = PdfOptions(reproducible=True)
    pdf_content = recipe_to_pdf(recipe, pdf_options=pdf_options)
    with open("recipe.pdf", "wb") as f:
        f.write(pdf_content)
```

### Convert Recipe to LaTeX

```python
from recipy.json_ld import recipe_from_url
from recipy.latex import recipe_to_latex, LatexOptions

recipe = recipe_from_url("https://www.allrecipes.com/recipe/14231/guacamole/")

if recipe:
    latex_options = LatexOptions(main_font="Liberation Serif", heading_font="Liberation Sans")
    latex_content = recipe_to_latex(recipe, options=latex_options)
    print(latex_content)
```

## Recipe Model

```python
from recipy.models import Recipe, IngredientGroup, InstructionGroup, Review, Meta, Rating

recipe = Recipe(
    title="Tomato Basil Salad",
    description="A simple, fresh salad perfect for summer.",
    ingredient_groups=[
        IngredientGroup(
            title="For the Salad",
            ingredients=[
                "2 ripe tomatoes, sliced",
                "1/4 cup fresh basil leaves, torn"
            ]
        ),
        IngredientGroup(
            title="For the Dressing",
            ingredients=[
                "2 tablespoons olive oil",
                "1 tablespoon balsamic vinegar"
            ]
        )
    ],
    instruction_groups=[
        InstructionGroup(
            title="Making the Salad",
            instructions=[
                "Arrange the tomato slices on a plate.",
                "Scatter the torn basil leaves over the tomatoes."
            ]
        ),
        InstructionGroup(
            title="Preparing the Dressing",
            instructions=[
                "In a small bowl, whisk together the olive oil and balsamic vinegar.",
                "Drizzle the dressing over the tomatoes and basil before serving."
            ]
        )
    ],
    notes="Serve immediately for the best flavor.",
    reviews=[
        Review(
            author="Jane Doe",
            body="This salad is so fresh and delicious!",
            rating=4.5
        ),
        Review(
            author="John Smith",
            body="Simple yet tasty. I added some mozzarella for extra flavor.",
            rating=4.0
        )
    ],
    image_urls=[
        "https://example.com/tomato_basil_salad_small.jpg",
        "https://example.com/tomato_basil_salad_medium.jpg",
        "https://example.com/tomato_basil_salad_large.jpg"
    ],
    rating=Rating(value=4.3, count=28),
    meta=Meta(
        prep_time_minutes=10,
        cook_time_minutes=0,
        total_time_minutes=10,
        recipe_yield="2 servings"
    )
)

print(recipe.model_dump_json(indent=2))
```

## Supported Features by Format

<table>
    <thead>
        <tr>
            <th></th>
            <th colspan="2">JSON-LD</th>
            <th colspan="2">Markdown</th>
            <th>LaTeX</th>
        </tr>
        <tr>
            <th>Feature</th>
            <th>Input</th>  <!-- json input -->
            <th>Output</th> <!-- json output -->
            <th>Input</th>  <!-- markdown input -->
            <th>Output</th> <!-- markdown output -->
            <th>Output</th> <!-- latex output -->
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Title</td>
            <td>✅</td> <!-- json input -->
            <td>✅</td> <!-- json output -->
            <td>✅</td> <!-- markdown input -->
            <td>✅</td> <!-- markdown output -->
            <td>✅</td> <!-- latex output -->
        </tr>
        <tr>
            <td>Description</td>
            <td>✅</td> <!-- json input -->
            <td>✅</td> <!-- json output -->
            <td>✅</td> <!-- markdown input -->
            <td>✅</td> <!-- markdown output -->
            <td>✅</td> <!-- latex output -->
        </tr>
        <tr>
            <td>Ingredient Groups</td>
            <td>❌</td> <!-- json input -->
            <td>❌</td> <!-- json output -->
            <td>✅</td> <!-- markdown input -->
            <td>✅</td> <!-- markdown output -->
            <td>✅</td> <!-- latex output -->
        </tr>
        <tr>
            <td>Ingredients</td>
            <td>✅</td> <!-- json input -->
            <td>✅</td> <!-- json output -->
            <td>✅</td> <!-- markdown input -->
            <td>✅</td> <!-- markdown output -->
            <td>✅</td> <!-- latex output -->
        </tr>
        <tr>
            <td>Instruction Groups</td>
            <td>✅</td> <!-- json input -->
            <td>✅</td> <!-- json output -->
            <td>✅</td> <!-- markdown input -->
            <td>✅</td> <!-- markdown output -->
            <td>✅</td> <!-- latex output -->
        </tr>
        <tr>
            <td>Instructions</td>
            <td>✅</td> <!-- json input -->
            <td>✅</td> <!-- json output -->
            <td>✅</td> <!-- markdown input -->
            <td>✅</td> <!-- markdown output -->
            <td>✅</td> <!-- latex output -->
        </tr>
        <tr>
            <td>Images</td>
            <td>✅</td> <!-- json input -->
            <td>✅</td> <!-- json output -->
            <td>✅</td> <!-- markdown input -->
            <td>✅</td> <!-- markdown output -->
            <td>❌</td> <!-- latex output -->
        </tr>
        <tr>
            <td>Rating</td>
            <td>✅</td> <!-- json input -->
            <td>✅</td> <!-- json output -->
            <td>❌</td> <!-- markdown input -->
            <td>❌</td> <!-- markdown output -->
            <td>❌</td> <!-- latex output -->
        </tr>
        <tr>
            <td>Reviews</td>
            <td>✅</td> <!-- json input -->
            <td>✅</td> <!-- json output -->
            <td>❌</td> <!-- markdown input -->
            <td>❌</td> <!-- markdown output -->
            <td>❌</td> <!-- latex output -->
        </tr>
        <tr>
            <td>Metadata</td>
            <td>✅</td> <!-- json input -->
            <td>✅</td> <!-- json output -->
            <td>❌</td> <!-- markdown input -->
            <td>❌</td> <!-- markdown output -->
            <td>❌</td> <!-- latex output -->
        </tr>
        <tr>
            <td>Notes</td>
            <td>✅</td> <!-- json input -->
            <td>✅</td> <!-- json output -->
            <td>✅</td> <!-- markdown input -->
            <td>✅</td> <!-- markdown output -->
            <td>✅</td> <!-- latex output -->
        </tr>
    </tbody>
</table>

## License

```
Permission to use, copy, modify, and/or distribute this software for
any purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED “AS IS” AND THE AUTHOR DISCLAIMS ALL
WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE
FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY
DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN
AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
```