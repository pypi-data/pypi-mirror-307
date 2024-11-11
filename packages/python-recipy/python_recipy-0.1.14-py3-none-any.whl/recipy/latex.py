from typing import Optional

from .models import Recipe


class LatexOptions:
    """
    Represents options for the LaTeX conversion process.

    :ivar main_font: The main font to use in the LaTeX document
    :type main_font: str
    :ivar heading_font: The font to use for headings in the LaTeX document
    :type heading_font: str
    """

    def __init__(self, main_font: str = "TeX Gyre Termes", heading_font: str = "TeX Gyre Termes"):
        self.main_font = main_font
        self.heading_font = heading_font


def recipe_to_latex(recipe: Recipe, options: Optional[LatexOptions] = None) -> str:
    """
    Converts a `Recipe` object into a LaTeX formatted string for generating a PDF.

    :param recipe: The `Recipe` object to be converted
    :type recipe: Recipe
    :param options: The options to use for the LaTeX conversion process
    :type options: LatexOptions
    :returns: A LaTeX formatted string representing the recipe, including the title, description, ingredients, and instructions
    :rtype: str
    """
    if options is None:
        options = LatexOptions()

    title = recipe.title
    description = recipe.description
    ingredient_groups = recipe.ingredient_groups
    instruction_groups = recipe.instruction_groups

    latex = [
        "\\documentclass[10pt]{article}",
        "\\pdfvariable suppressoptionalinfo \\numexpr32+64+512\\relax",
        "\\usepackage{fontspec}",
        "\\usepackage{geometry}",
        "\\usepackage{enumitem}",
        "\\usepackage{graphicx}",
        "\\usepackage{paracol}",
        "\\usepackage{microtype}",
        "\\usepackage{parskip}",
        "\\usepackage{fancyhdr}",
        "\\geometry{letterpaper, margin=0.75in}",
        f"\\setmainfont{{{options.main_font}}}",
        f"\\newfontfamily\\headingfont{{{options.heading_font}}}",
        "\\pagestyle{fancy}",
        "\\fancyhf{}",
        "\\renewcommand{\\headrulewidth}{0pt}",
        "\\begin{document}",
        "\\setlist[enumerate,1]{itemsep=0em}",
        "\\begin{center}",
        "{\\huge \\bfseries \\headingfont " + _escape_latex(title) + "}",
        "\\end{center}",
        "\\vspace{1em}",
        "\\normalsize"  # Adjust font size for the rest of the document
    ]

    if description:
        latex.append("\\noindent " + _escape_latex(description))

    latex.append("\\vspace{1em}")
    latex.append("\\columnratio{0.35}")
    latex.append("\\begin{paracol}{2}")
    
    # Use headingfont for section and subsection headings
    latex.append("\\section*{\\headingfont Ingredients}")
    latex.append("\\raggedright")

    for ingredient_group in ingredient_groups:
        if ingredient_group.title:
            latex.append(f"\\subsection*{{\\headingfont {_escape_latex(ingredient_group.title)}}}")
        latex.append("\\begin{itemize}[leftmargin=*]")
        for ingredient in ingredient_group.ingredients:
            latex.append(f"\\item {_escape_latex(ingredient)}")
        latex.append("\\end{itemize}")

    latex.append("\\switchcolumn")
    latex.append("\\section*{\\headingfont Instructions}")

    for instruction_group in instruction_groups:
        if instruction_group.title:
            latex.append(f"\\subsection*{{\\headingfont {_escape_latex(instruction_group.title)}}}")
        latex.append("\\begin{enumerate}[leftmargin=*]")
        for instruction in instruction_group.instructions:
            latex.append(f"\\item {_escape_latex(instruction)}")
        latex.append("\\end{enumerate}")

    latex.append("\\end{paracol}")
    latex.append("\\end{document}")
    latex.append("")

    return "\n".join(latex)


def _escape_latex(text: str) -> str:
    mapping = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}'
    }
    return "".join(mapping.get(c, c) for c in text)
