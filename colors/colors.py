import random
import hashlib
import colorsys
import copy

import webcolors


COLORBREWER_COLORS = [(166, 206, 227), (31, 120, 180), (178, 223, 138), (51, 160, 44), (251, 154, 153), (227, 26, 28), (253, 191, 111), (255, 127, 0), (202, 178, 214), (106, 61, 154), (255, 255, 153), (177, 89, 40)]
BASE_HUES = [0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
BASE_LUMINANCE = 0.5


def word_to_color(word):
    """ Takes a string and returns an RGB color based on the
    md5 hash of that string """
    md5 = hashlib.md5()
    md5.update(word)
    hash_value = md5.hexdigest()
    rgb = '#' + hash_value[0:2] + hash_value[2:4] + hash_value[4:6]
    return rgb


def generate_color():
    # TODO - this might not be the optimal way - copy is expensive
    colors_to_generate = copy.copy(COLORBREWER_COLORS)
    colors_used = []

    while True:
        try:
            color = colors_to_generate.pop(0)
            colors_used.append(color)
        except IndexError:
            new_colors = get_new_colors(colors_used)
            colors_to_generate = new_colors
            colors_used = []
        yield webcolors.rgb_to_hex(color)


def calculate_distance_between_colors(color1, color2):
    """ Takes 2 color tupes and returns the average between them
    """
    return ((color1[0] + color2[0]) / 2, (color1[1] + color2[1]) / 2, (color1[2] + color2[2]) / 2)


def get_new_colors(colors_used):
    new_colors = []
    for i in xrange(len(colors_used) - 1):
        new_colors.append(calculate_distance_between_colors(colors_used[i], colors_used[i + 1]))

    return new_colors


def get_color(base_hues, base_luminance):
    """ Generate colors based on varying luminance"""
    count = 0
    while True:
        hue = base_hues[0 + count % len(base_hues)]
        luminance = base_luminance + (
            (0.2 * (count // len(base_hues))) % (0.9 - base_luminance)
        )
        yield colorsys.hls_to_rgb(hue, luminance, 1.0)
        count += 1


def save_html_page():
    """
    Save an HTML page with your generated colors to see the pallate
    """
    with open('test.html', 'w') as f:
        f.write('<html><head></head><body>')
        for idx, value in enumerate(get_color(BASE_HUES, BASE_LUMINANCE)):
            f.write('<div style="background-color:rgb({r},{g},{b})">{value}</div>'.format(
                value=value,
                r=int(value[0] * 255),
                g=int(value[1] * 255),
                b=int(value[2] * 255),
            ))
            if idx == 100:
                break
        f.write('</body></html>')


def color_too_close(color, colors, threshold=100):
    """
    For the random_color function, calculates the distance between
    two colors and returns False if they are closer than the threshold
    """
    for x in colors:
        distance = sum(abs(x[i] - color[i]) for i in xrange(3))
        if distance < threshold:
            return True
    return False


def random_color(seed=4545, max_iterations=15, threshold=100):
    """
    A Generator for random hex colors.
    Generates a sequence of colors that are different up to some threshold
    """
    random.seed(seed)
    colors = []
    iterations = 0
    while True:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if color_too_close(color, colors, threshold) and not iterations > max_iterations:
            iterations += 1
            continue
        else:
            colors.append(color)
            iterations = 0
        yield webcolors.rgb_to_hex(color)


# @chrisseto's super fast color generaor!
def colors(number):
    palette = COLORBREWER_COLORS
    while number > len(palette):
        new_palette = []
        color1 = palette[0]
        for color2 in palette[1:]:
            new_palette.extend((color1,
            (
                (color1[0] + color2[0]) / 2,
                (color1[1] + color2[1]) / 2,
                (color1[2] + color2[2]) / 2,
            ),
            color2))
            color1 = color2
        palette = new_palette

    return palette


if __name__ == "__main__":
    for i in xrange(5):
        color = generate_color(COLORBREWER_COLORS)
        print(color.next())
