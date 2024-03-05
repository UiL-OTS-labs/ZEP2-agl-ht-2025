import argparse
import os.path as p
import sys
import typing
import random

import cairo

str_list = typing.Literal[str]


RED = [1.0, 0.0, 0.0]
GREEN = [0.0, 1.0, 0.0]
BLUE = [0.0, 0.0, 1.0]
YELLOW = [1.0, 1.0, 0.0]
PURPLE = [1.0, 0.0, 1.0]
WHITE = [1.0, 1.0, 1.0]
BLACK = [0.0, 0.0, 0.0]
CYAN = [0.0, 1.0, 1.0]

COLORS = {
    "red": RED,
    "green": GREEN,
    "blue": BLUE,
    "yellow": YELLOW,
    "purple": PURPLE,
    "black": BLACK,
    "white": WHITE,
    "cyan": CYAN,
}


def positive_int(num) -> int:
    """Helper function to determine whether num is a positive integer"""
    inum = int(num)
    if inum < 1:
        raise argparse.ArgumentTypeError(f"{num} isn't an int greater than zero")
    return inum


def gen_stimulus(n: int, width: int, height: int, colors: str_list) -> None:
    with cairo.ImageSurface(cairo.FORMAT_RGB24, width, height) as surf:
        num_colors = len(colors)
        color_list = []
        for color in colors:
            color_list += [color] * num_colors
        cr = cairo.Context(surf)
        random.shuffle(color_list)

        for row in range(num_colors):
            for col in range(num_colors):
                color = COLORS[color_list[row * num_colors + col]]
                cr.set_source_rgb(color[0], color[1], color[2])
                w = width / num_colors
                h = height / num_colors
                r = row * h
                c = col * w
                cr.rectangle(c, r, w, h)
                cr.fill()
        surf.write_to_png(f"./stimuli/images/grid{n}.png")
    return


def gen_stimuli(num_stimuli: int, width: int, height: int, colors: str_list) -> None:
    """The worker that generates the stimuli"""
    for n in range(num_stimuli):
        gen_stimulus(n, width, height, colors)


def main():
    parser = argparse.ArgumentParser(
        p.basename(sys.argv[0]),
        description="generate stimuli for the ht familiarization phase.",
    )
    parser.add_argument(
        "-w",
        "--width",
        help="The width of the stimuli must be larger than 0",
        type=positive_int,
        metavar="[1, inf)",
        default=800,
    )
    parser.add_argument(
        "-H",
        "--height",
        help="The height of the stimuli, must be larger than 0",
        type=positive_int,
        metavar="[1, inf)",
        default=800,
    )
    parser.add_argument(
        "-n",
        "--num-stimuli",
        help="The number of stimuli to generate",
        type=positive_int,
        metavar="[1, inf)",
        default=25,
    )
    parser.add_argument(
        "-c",
        "--colors",
        choices=COLORS.keys(),
        help="The colors that used to generate the stimuli",
        nargs="+",
        default=["red", "blue", "yellow", "purple", "black"],
    )
    args = parser.parse_args()

    n = args.num_stimuli
    width = args.width
    height = args.height
    colors = args.colors

    gen_stimuli(n, width, height, colors)


if __name__ == "__main__":
    main()
