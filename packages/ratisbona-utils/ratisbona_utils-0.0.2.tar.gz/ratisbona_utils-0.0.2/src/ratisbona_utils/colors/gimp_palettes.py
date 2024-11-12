from pathlib import Path

import click

from ratisbona_utils.colors.simple_color import rgb_to_hex
from ratisbona_utils.colors.palette import Palette


def to_gimp_palette(palette: Palette) -> str:
    """
    Convert a Palette object to a GIMP palette file format.

    Args:
        palette (Palette): The palette object to convert

    Returns:
        str: The GIMP palette file content
    """
    lines = [
        "GIMP Palette",
        f"Name: {palette.name}",
        "# Description: {palette.description.replace('\n', ' ')}",
        "# Author: {palette.author}",
        "# Created: {palette.creation_date}",
        "Columns: 16"
    ]
    for color, name in zip(palette.colors, palette.color_names):
        lines.append(f"{color[0]} {color[1]} {color[2]} {name}")
    return "\n".join(lines)


def parse_gimp_palette(palette_as_str: str) -> Palette:
    """
    Parse a GIMP palette file and return the Palette object.

    Args:
        palette_as_str (str): The GIMP palette file content as a string

    Returns:
        Palette: The parsed palette object
    """
    lines = palette_as_str.splitlines()
    lines = map(str.strip, lines)
    lines = list(filter(lambda s: s and not s.startswith("#"), lines))
    if not lines[0] == "GIMP Palette":
        raise ValueError("Not a GIMP palette file")
    if not lines[1].startswith("Name: "):
        raise ValueError("Invalid palette name line {line[1]}. Does not start with 'Name: '")
    name = lines[1][6:]
    if not lines[2].startswith("Columns: "):
        raise ValueError("Invalid columns line {line[2]}. Does not start with 'Columns: '")


    colors = []
    names = []
    for line in lines[3:]:
        if not line:
            continue
        color = line.split()
        colors.append((int(color[0]), int(color[1]), int(color[2])))
        names.append(color[3])
    return Palette(
        name=name,
        description="",
        author="",
        creation_date=None,
        colors=colors,
        color_names=names,
        color_types=["RGB"] * len(colors)
    )

@click.command()
@click.argument("palette", type=click.Path(exists=True, path_type=Path, dir_okay=False, file_okay=True))
def gimp_palette_parser(palette: Path):
    """
    Parse a GIMP palette file and print the palette object.
    """
    with open(palette) as f:
        palette_str = f.read()
    palette = parse_gimp_palette(palette_str)
    print(palette)

    for color, name in zip(palette.colors, palette.color_names):
        python_name = name.replace("-", "_")
        r, g, b = color
        print(f"{python_name}=({hex(r)}, {hex(g)}, {hex(b)})")

    text="SOLARIZED_COLORS=[\n"
    for name in palette.color_names:
        python_name = name.replace("-", "_")
        text += f"    {python_name},\n"
    text+="]"

    print(text)


