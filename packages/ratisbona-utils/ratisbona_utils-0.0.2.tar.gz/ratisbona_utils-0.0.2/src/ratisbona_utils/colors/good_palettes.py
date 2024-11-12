from ratisbona_utils.colors import normalized_to_rgb
from ratisbona_utils.colors.palette_generators import ega_num_to_rgb, cga_num_to_normalized_rgb
from ratisbona_utils.colors.simple_color import hex_to_rgb, lab_lighten_rgb

ULIS_WEBCOLORS_HEX = [
    '#993300',
    '#CC0000',
    '#FF6600',
    '#FFCC00',
    '#99CC00',
    '#009900',
    '#00CCCC',
    '#0099FF',
    '#0000CC',
    '#6600CC',
    '#CC00CC'
]

ULIS_WEBCOLORS = [hex_to_rgb(hexcolor) for hexcolor in ULIS_WEBCOLORS_HEX]

FIRE_PALETTE_HEX = [
    '#0000cc',
    '#3333ff',
    '#33ffff',
    #'#330033',
    '#ffff00',
    '#ffff33',
    '#ffcc00',
    '#ff0000',
    '#cc0000',
    '#660000',
    '#000000'
]

FIRE_PALETTE = [hex_to_rgb(hexcolor) for hexcolor in reversed(FIRE_PALETTE_HEX)]

EGA_PALETTE = [ega_num_to_rgb(i) for i in range(64)]

CGA_PALETTE = [normalized_to_rgb(cga_num_to_normalized_rgb(i)) for i in range(16)]

AMIGA_PALETTE = [
    (0, 85, 170),
    (255,255,255),
    (0,0,0),
    (255, 136, 0)
]

solarized_base03=(0x0, 0x2b, 0x36)
solarized_base02=(0x7, 0x36, 0x42)
solarized_base01=(0x58, 0x6e, 0x75)
solarized_base00=(0x65, 0x7b, 0x83)
solarized_base0=(0x83, 0x94, 0x96)
solarized_base1=(0x93, 0xa1, 0xa1)
solarized_base2=(0xee, 0xe8, 0xd5)
solarized_base3=(0xfd, 0xf6, 0xe3)
solarized_yellow=(0xb5, 0x89, 0x0)
solarized_orange=(0xcb, 0x4b, 0x16)
solarized_red=(0xdc, 0x32, 0x2f)
solarized_magenta=(0xd3, 0x36, 0x82)
solarized_violet=(0x6c, 0x71, 0xc4)
solarized_blue=(0x26, 0x8b, 0xd2)
solarized_cyan=(0x2a, 0xa1, 0x98)
solarized_green=(0x85, 0x99, 0x0)

SOLARIZED_COLORS_BASE=[
    solarized_base03,
    solarized_base02,
    solarized_base01,
    solarized_base00,
    solarized_base0,
    solarized_base1,
    solarized_base2,
    solarized_base3
]

SOLARIZED_COLORS_COLORS=[
    solarized_red,
    solarized_orange,
    solarized_yellow,
    solarized_green,
    solarized_cyan,
    solarized_blue,
    solarized_violet,
    solarized_magenta,
]

SOLARIZED_COLORS = SOLARIZED_COLORS_BASE + SOLARIZED_COLORS_COLORS
SOLARIZED_COLORS_EXTENDED = (
        SOLARIZED_COLORS
        + [lab_lighten_rgb(color, 20) for color in SOLARIZED_COLORS_COLORS]
        + [lab_lighten_rgb(color, -20) for color in SOLARIZED_COLORS_COLORS]
)


