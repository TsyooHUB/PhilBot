import io
from PIL import Image

COORDS = [(631, 551), (990, 550), (634, 308), (980, 339)]
COEFFS = [0.6547747129877984, 0.008083638431858402, -1670.4677146851654, -0.05607509889913542,
          0.6258704586809742, -628.8659542867306, -7.95610829238863e-05, 4.137514033619954e-05]


def juan_processing(buffer):
    width, height = 1219, 684
    im = Image.open(buffer).convert(mode='RGBA')
    im = im.resize((width, height), resample=Image.ANTIALIAS)
    bg = Image.open('data/img/juan_bg.png').convert(mode='RGBA')
    im = im.transform((width * 4, height * 4), Image.PERSPECTIVE, COEFFS, Image.BICUBIC)
    im = im.resize((bg.width, bg.height), resample=Image.ANTIALIAS)

    bg = Image.alpha_composite(bg, im)

    fg = Image.open('data/img/juan_fg.png').convert(mode='RGBA')
    bg = Image.alpha_composite(bg, fg)

    output = io.BytesIO()
    bg.save(output, format='png')
    output.seek(0)
    return output