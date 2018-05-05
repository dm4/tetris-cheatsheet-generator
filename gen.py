#!/usr/bin/env python

import re
import functools
from PIL import Image, ImageDraw

# canvas data
all_data = [
"""
L  ZZ S
L   ZZSSOO
LL IIIISOO
""",
"""
L  ZZ   OO
L   ZZ JOO
LL IIIIJJJ
""",
"""
        LL
         L
     TTT L
OO   ZT  J
OO  ZZSS J
IIIIZSS JJ
""",
"""
        LL
         L
  Z  LLL L
 ZZSSLT  J
 ZSSOOTT J
IIIIOOT JJ
""",
]

# initialize
sub_images = []
blocks = {}
block_names = ['I', 'O', 'T', 'J', 'L', 'S', 'Z', 'X', 'B']
(block_width, block_height) = (18, 18)
for block in block_names:
    blocks[block] = Image.open('images/' + block + '.png')
    assert blocks[block].size[0] == block_width and blocks[block].size[1] == block_height, 'Block size mismatch!'

for canvas_data in all_data:
    # remove empty lines
    lines = canvas_data.split('\n')
    lines = list(filter(lambda x: not re.match(r'^$', x), lines))

    # canvas size
    canvas_size = (block_width * 10, block_height * len(lines))

    # init canvas
    im = Image.new('RGBA', canvas_size, (0, 0, 0, 255))

    # draw blocks
    for h in range(len(lines)):
        line = lines[h]
        assert not len(line) > 10, 'every line should < 10 blocks'
        line = line + ' ' * (10 - len(line))
        for w in range(10):
            b = line[w]
            if b == ' ':
                b = 'B'
            im.paste(blocks[b], (w * block_width, h * block_height))

    # save image
    sub_images.append(im)

# generate output image
(margin_width, margin_height) = (20, 20)
sub_images_height = functools.reduce(lambda x, y: x + y, map(lambda x: x.size[1], sub_images))
output_size = (10 * block_width + 2 * margin_width, sub_images_height + (len(sub_images) + 1) * margin_height)
output = Image.new('RGBA', output_size, (0, 0, 0, 255))
current_height = margin_height
for im in sub_images:
    output.paste(im, (margin_width, current_height))
    current_height += (im.size[1] + margin_height)

output.save('output.png')
