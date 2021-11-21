"""
字符图片
"""
import tkinter
import tkinter.font as font

import numpy as np
from PIL import ImageGrab

ROOT = tkinter.Tk()


def list_availabel_font_names():
    a = font.names()
    return a


def list_available_fonts():
    a = font.families(ROOT)
    return a


def measure_text(s: str, ft: font.Font):
    width = ft.measure(s)
    height = ft.metrics("linespace")
    return width, height


def draw_text(s, ft: font.Font, color='black', background_color='white'):
    width, height = measure_text(s, ft)
    c = tkinter.Canvas(width=width, height=height, bg=background_color)
    # reminder = g.create_text(g.winfo_width() / 2, g.winfo_height() / 2, text='Press up,down,left,right arrow to move',
    #                      fill='purple', font=('Concolas', 30))
    c.create_text(width / 2, height / 2, text=s, fill=color, font=ft)
    c.pack()
    c.update()
    x = ROOT.winfo_rootx() + c.winfo_x()
    y = ROOT.winfo_rooty() + c.winfo_y()
    x1 = x + c.winfo_width()
    y1 = y + c.winfo_height()
    print(x, y, x1, y1)
    img = ImageGrab.grab().crop((x, y, x1, y1))
    print(img)
    return np.ndarray(img)


def test_draw_text():
    # print(list_available_fonts())
    # print(list_availabel_font_names())
    ft = font.Font(family="HanziPen SC", size=20, weight=font.BOLD)
    img = draw_text("魏印福", ft)
    import pylab as plt

    plt.imshow(img)
    plt.show()


if __name__ == '__main__':
    pass
