import colorio

if __name__ == '__main__':

    colorspace_names = [
        # 'cam02lcd',
        # 'cam02scd',
        # 'cam02ucs',
        # 'cam16ucs',
        # 'cielab',
        # 'cieluv',
        # 'ciehcl',
        # 'cielch',
        # 'din99',
        # 'din99b',
        # 'din99c',
        # 'din99d',
        # 'hdrlinear',
        # 'ictcp',
        'ipt',
        'jzazbz',
        'oklab',
        # 'osaucs',  # error
        'prolab',
        # 'rlab',
        # 'srgblinear',  # error
        # 'srgb1',  # error
        # 'srgb255',  # error
        # 'srgbhex',  # error
        'srlab2',
        # 'xyy1',
        # 'xyy100',
        # 'xyz1',
        # 'xyz100',
    ]

    # for cs_name in colorspace_names:
    #     print(cs_name)
    #     # plt = colorio.plot_primary_srgb_gradients(name)
    #     plt = colorio.plot_rgb_gamut(name)
    #     plt.show()

    colorspaces = [
        colorio.cs.IPT,
        colorio.cs.JzAzBz,
        colorio.cs.OKLAB,
        colorio.cs.PROLAB,
        colorio.cs.SRLAB2,
    ]

    for cs in colorspaces:
        print(cs.name)
        plt = colorio.data.HungBerns().plot(cs)
        plt.show()

        plt = colorio.data.Xiao().plot(cs)
        plt.show()

        plt = colorio.data.EbnerFairchild().plot(cs)
        plt.show()

        # plt = colorio.data.LuoRigg(4).plot(cs)  # error
        # plt.show()

        plt = colorio.data.Munsell().plot(cs, V=5)
        plt.show()

        plt = colorio.data.MacAdam1974().plot(cs)
        plt.show()
