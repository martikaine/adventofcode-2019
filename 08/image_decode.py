import numpy as np
from enum import IntEnum
from PIL import Image


class Color(IntEnum):
    black = 0
    white = 1
    transparent = 2


def load_image_data(filename: str) -> list:
    with open(filename) as f:
        chars = list(f.readline().strip())
        return [int(c) for c in chars]


def parse_image(data: list, width: int, height: int):
    return np.reshape(data, (-1, height, width))


def solve_part_one():
    data = load_image_data('image.txt')
    image = parse_image(data, 25, 6)
    layer_count = np.shape(image)[0]

    least_zeros_count = len(data)
    checksum = -1
    for layer in range(layer_count):
        _, counts = np.unique(image[layer], return_counts=True)
        zeros_count = counts[0]
        if zeros_count < least_zeros_count:
            least_zeros_count = zeros_count
            checksum = counts[1] * counts[2]

    print(checksum)


def render_image(layered_image: np.ndarray) -> np.ndarray:
    width = layered_image.shape[2]
    height = layered_image.shape[1]

    image_2d = np.zeros((height, width))

    for x in range(width):
        for y in range(height):
            image_2d[y][x] = get_pixel_color(x, y, layered_image)

    image = Image.fromarray(image_2d.astype('uint8')*255)
    image.show()


def get_pixel_color(x: int, y: int, layered_image: np.ndarray) -> int:
    layer_count = layered_image.shape[0]
    # go down the layers until we find the first non-transparent pixel
    for i in range(layer_count):
        layer = layered_image[i]
        pixel_color = layer[y][x]
        if pixel_color == Color.black or pixel_color == Color.white:
            return pixel_color
    else:
        return Color.transparent


def solve_part_two():
    data = load_image_data('image.txt')
    layer_image = parse_image(data, 25, 6)
    render_image(layer_image)


solve_part_one()
solve_part_two()

#print(parse_image([1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2], 3, 2))
#test_image = parse_image([int(c) for c in '0222112222120000'], 2, 2)
# print(test_image)
# render_image(test_image)
