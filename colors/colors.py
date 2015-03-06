import webcolors


COLORBREWER_COLORS = [(166, 206, 227), (31, 120, 180), (178, 223, 138), (51, 160, 44), (251, 154, 153), (227, 26, 28), (253, 191, 111), (255, 127, 0), (202, 178, 214), (106, 61, 154), (255, 255, 153), (177, 89, 40)]


def generate_color(initial_color_list):
    colors_to_generate = initial_color_list
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
        new_colors.append(calculate_distance_between_colors(colors_used[i], colors_used[i+1]))

    return new_colors

if __name__ == "__main__":
    for i in xrange(5):
        color = generate_color(COLORBREWER_COLORS)
        print(color.next())
