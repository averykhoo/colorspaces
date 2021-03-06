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

    return r, g, b


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


if __name__ == '__main__':
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    aqua = (0, 255, 255)
    teal = (0, 128, 128)

    print(ok_distance(white, black))
    print(ok_distance(red, green))
    print(ok_distance(blue, green))
    print(ok_distance(blue, aqua))
    print(ok_distance(blue, teal))
    print(ok_distance(green, aqua))
    print(ok_distance(green, teal))
