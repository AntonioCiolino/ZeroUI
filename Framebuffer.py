import os
import mmap
import numpy as np
from PIL import Image, ImageDraw, ImageFont

class Framebuffer:
    def __init__(self, fb_path="/dev/fb0"):
        self.fb_path = fb_path
        self.fb = os.open(self.fb_path, os.O_RDWR)
        self.screen_width = 320
        self.screen_height = 240
        self.bpp = 16
        self.screen_size = self.screen_width * self.screen_height * self.bpp // 8
        self.fbuf = mmap.mmap(self.fb, self.screen_size, mmap.MAP_SHARED, mmap.PROT_WRITE, offset=0)

    def display_image(self, image):
        img = image.convert("RGB")
        arr = np.array(img, dtype=np.uint16)
        arr = ((arr[:, :, 0] >> 3) << 11) | ((arr[:, :, 1] >> 2) << 5) | (arr[:, :, 2] >> 3)
        self.fbuf.seek(0)
        self.fbuf.write(arr.tobytes())
