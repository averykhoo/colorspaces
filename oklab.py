import json
import math


def linear_srgb_to_srgb(x):
    # https://bottosson.github.io/posts/colorwrong/#what-can-we-do?
    if x >= 0.0031308:
        return (1.055) * x ** (1.0 / 2.4) - 0.055
    else:
        return 12.92 * x


def srgb_to_linear_srgb(x):
    # https://bottosson.github.io/posts/colorwrong/#what-can-we-do?
    if x >= 0.04045:
        return ((x + 0.055) / (1 + 0.055)) ** 2.4
    else:
        return x / 12.92


def srgb_to_oklab(r, g, b):
    # https://bottosson.github.io/posts/oklab/#converting-from-linear-srgb-to-oklab
    r = srgb_to_linear_srgb(r / 255)
    g = srgb_to_linear_srgb(g / 255)
    b = srgb_to_linear_srgb(b / 255)

    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b

    l_ = math.pow(l, 1 / 3)
    m_ = math.pow(m, 1 / 3)
    s_ = math.pow(s, 1 / 3)

    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
            )


def oklab_to_srgb(L, a, b):
    # https://bottosson.github.io/posts/oklab/#converting-from-linear-srgb-to-oklab
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b

    l = l_ * l_ * l_
    m = m_ * m_ * m_
    s = s_ * s_ * s_

    r = +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s

    r = linear_srgb_to_srgb(r) * 255
    g = linear_srgb_to_srgb(g) * 255
    b = linear_srgb_to_srgb(b) * 255

    return int(max(min(r, 255), 0)), int(max(min(g, 255), 0)), int(max(min(b, 255), 0))


def toe(x):
    # https://bottosson.github.io/posts/colorpicker/#intermission---a-new-lightness-estimate-for-oklab
    # https://bottosson.github.io/posts/colorpicker/#common-code
    k_1 = 0.206
    k_2 = 0.03
    k_3 = (1. + k_1) / (1. + k_2)
    return 0.5 * (k_3 * x - k_1 + math.sqrt((k_3 * x - k_1) * (k_3 * x - k_1) + 4 * k_2 * k_3 * x))


def toe_inv(x):
    # https://bottosson.github.io/posts/colorpicker/#intermission---a-new-lightness-estimate-for-oklab
    # https://bottosson.github.io/posts/colorpicker/#common-code
    k_1 = 0.206
    k_2 = 0.03
    k_3 = (1. + k_1) / (1. + k_2)
    return (x * x + k_1 * x) / (k_3 * (x + k_2))


def ok_distance(rgb_1, rgb_2):
    l1, a1, b1 = srgb_to_oklab(*rgb_1)
    l1 = toe(l1)
    l2, a2, b2 = srgb_to_oklab(*rgb_2)
    l2 = toe(l2)
    # return 400 * ((1 - (1 - (l1 - l2) ** 2) ** 0.5) + (a1 - a2) ** 2 + (b1 - b2) ** 2) ** 0.5
    return 200 * (((l1 - l2) / 2) ** 2 + (a1 - a2) ** 2 + (b1 - b2) ** 2) ** 0.5


def interpolate(x, y, steps):
    delta = (y - x) / (steps - 1)
    out = [x + i * delta for i in range(steps)]
    out[-1] = y
    return out


def ok_interpolate(rgb_1, rgb_2, steps):
    assert steps >= 2
    l1, a1, b1 = srgb_to_oklab(*rgb_1)
    l1 = toe(l1)
    l2, a2, b2 = srgb_to_oklab(*rgb_2)
    l2 = toe(l2)

    l_s = interpolate(l1, l2, steps)
    a_s = interpolate(a1, a2, steps)
    b_s = interpolate(b1, b2, steps)

    return [oklab_to_srgb(toe_inv(l), a, b)
            for l, a, b in zip(l_s, a_s, b_s)]


def rgb_to_hex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'


def hex_to_rgb(code):
    if code[0] == '#':
        code = code[1:]
    assert len(code) == 6
    return int(code[:2], 16), int(code[2:4], 16), int(code[4:], 16)


def interpolate_hex(hex_1, hex_2, steps):
    print(hex_1, hex_2)
    return list(rgb_to_hex(*rgb) for rgb in ok_interpolate(hex_to_rgb(hex_1), hex_to_rgb(hex_2), steps))


if __name__ == '__main__':
    # white = hex_to_rgb('#ffffff')
    # black = hex_to_rgb('#000000')
    # red = hex_to_rgb('#ff0000')
    # green = hex_to_rgb('#00ff00')
    # blue = hex_to_rgb('#0000ff')
    # aqua = hex_to_rgb('#00ffff')
    # teal = hex_to_rgb('#008080')
    # print(ok_distance(white, black))
    # print(ok_distance(red, green))
    # print(ok_distance(blue, green))
    # print(ok_distance(blue, aqua))
    # print(ok_distance(blue, teal))
    # print(ok_distance(green, aqua))
    # print(ok_distance(green, teal))
    #
    with open('actual-colors.json') as f:
        all_colors = json.load(f)

    out = dict()
    color_names = list(all_colors.keys())
    for i, color_1 in enumerate(color_names[1:]):
        for color_2 in color_names[1:]:
            if color_1!=color_2:
                palette_name = f'{color_1}-{color_2}'
                print(palette_name)
                palette_colors = interpolate_hex(all_colors[color_1][2], all_colors[color_2][2], 11)
                print(palette_colors)
                out[palette_name] = palette_colors

    with open('interpolated-colors.json', 'w') as f:
        json.dump(out, f, indent=4)
