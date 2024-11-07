# Copyright © 2024 Ibrahim Almayyas
# All rights reserved.
#
# This library is licensed under the MIT License, which allows for use, modification, and distribution under the terms of the license.
# This software uses the following third-party libraries:
# - Pillow: https://github.com/python-pillow/Pillow/blob/main/LICENSE
# - Tkinter: Included with Python's standard library (https://docs.python.org/3/library/tkinter.html#license)
# - OpenCV (cv2): https://opencv.org/license/

import tkinter
from tkinter import messagebox as MessageBox
from tkinter import font
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageOps  # to modify images
global _globals
import cv2


def assign_key(key: str, todo):
    global _globals
    _globals['key binds'][key] = todo


def key_pressed(event):

    global _globals
    for key, value in _globals['key binds'].items():
        if event.keysym == key:
            value()


def show_messagebox(message: str, title: str = None):
    if title is None:
        global _globals
        title = _globals['root'].title
    MessageBox.showinfo(title=title, message=message)


def _from_rgb(rgb):
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'


def __init__(size: tuple = None, title: str = None, background_color: tuple = None):
    global _globals
    _globals = {
        "root": tkinter.Tk(screenName=title),
        "items": {},
        "images": {},
        "key binds": {}
    }
    if size is None:    size = (100, 100)
    _globals["root"].geometry(f"{size[0]}x{size[1]}")
    if title is not None:   _globals["root"].title(title)
    _globals["root"].bind("<KeyRelease>", key_pressed)
    if background_color is not None: _globals["root"].configure(bg=_from_rgb(background_color))


def create_window(size: tuple = None, title: str = None, background_color: tuple = None):
    global _globals, window_size, window_title, window_background_color
    _globals = {
        "root": tkinter.Tk(screenName=window_title),
        "items": {},
        "images": {},
        "key binds": {}
    }
    window(
        size if size is not None else window_size,
        title if title is not None else window_title,
        background_color if background_color is not None else window_background_color
    )


def window(size: tuple = None, title: str = None, background_color: tuple = None):
    global _globals
    if size is not None:    _globals["root"].geometry(f"{size[0]}x{size[1]}")
    if title is not None:   _globals["root"].title(title)
    if background_color is not None: _globals["root"].configure(bg=_from_rgb(background_color))


window_size = (200, 200)
window_background_color = (236, 236, 236)
window_title = "ICT KW"


def get_window_background_color() -> tuple:
    global _globals
    return (_globals['root'].winfo_width(), _globals['root'].winfo_height())


def run():
    tkinter.mainloop()


def create_image(file, size):
    img = Image.open(file).resize((int(size[0]), int(size[1])))
    return ImageTk.PhotoImage(img)


def new_ListBox(items: list | tuple = None, location: tuple = (0, 0), size: tuple = (100, 100), on_select=None):
    item = ListBox(selectmode='single')
    item.create(items, location, size, on_select)
    return item


class ListBox(tkinter.Listbox):

    def create(self, values: list | tuple = None, location: tuple = (0, 0), size: tuple = (100, 100), todo_on_select=None):
        global _globals
        self.master = _globals['root']
        self.todo_on_select = todo_on_select

        self.place(x=location[0], y=location[1], width=size[0], height=size[1])
        if values is not None:
            for n, value in enumerate(values):
                self.insert(n, value)

        def callback(event):
            if self.todo_on_select is not None:  self.todo_on_select()

        self.bind('<<ListboxSelect>>', callback)

    def edit(self, items: list | tuple = None, location: tuple = None, size: tuple = None, on_select=None):
        todo_on_select = on_select
        values = items
        if location is None:    location = (float(self.place_info()["x"]), float(self.place_info()["y"]))
        if size is None:        size = (float(self.place_info()["width"]), float(self.place_info()["height"]))
        self.place(x=location[0], y=location[1], width=size[0], height=size[1])
        if todo_on_select is not None:  self.todo_on_select = todo_on_select
        if values is not None:
            if self.get(0, 'end') != values:
                self.delete(0, 'end')
                for n, value in enumerate(values):
                    self.insert(n, value)

    def get_selected_item(self):
        index = self.get(0, 'end').index(self.get(self.curselection()))
        self.select_clear(0, 'end')
        self.selection_set(index)
        return self.get(self.curselection())


def new_Label(location: tuple = None, size: tuple = None, text: str = None, background_color: tuple = None, fore_color: tuple = None, font_size: int = None, bold: bool = None,
              font_style: str = None, align: str = None):
    item = Label()
    item.create(location, size, text, background_color, fore_color, font_size, bold, font_style, align)
    return item


class Label(tkinter.Label):

    def create(self, location: tuple = None, size: tuple = None, text: str = None, background_color: tuple = None, fore_color: tuple = None, font_size: int = None, bold: bool = None,
               font_style: str = None, align: str = None):
        global _globals

        self.master = _globals['root']
        if font_size is None:
            self.font_size = 10
        else:
            self.font_size = font_size

        if bold is not None:
            self.bold = bold
        else:
            self.bold = 'normal'

        if font_style is None:
            self.font_style = 'Arial'
        else:
            self.font_style = font_style

        if text is not None:    self.configure(text=text)
        if location is None:    location = (0, 0)
        if size is None:        size = (100, 25)

        self.place(x=location[0], y=location[1], width=size[0], height=size[1])
        if background_color is not None: self.configure(bg=_from_rgb(background_color))
        if fore_color is not None: self.configure(fg=_from_rgb(fore_color))
        if align is not None:
            if align.lower() in ('left', 'l'):    self.configure(anchor='w', justify='left')
            if align.lower() in ('right', 'r'):   self.configure(anchor='e', justify='right')
            if align.lower() in ('center', 'c'):  self.configure(anchor='center', justify='center')

        font_ = []
        # font_.append(font_style) if font_style is not None else font_.append(self.font_style)
        # font_.append(font_size) if font_size is not None else font_.append(self.font_size)
        font_.append(self.font_style)
        font_.append(self.font_size)
        font_.append(self.bold)
        # font_.append(bold) if bold else font_.append(self.bold)
        # self.configure(font=(font_style, 20))
        font_ = tuple(font_)
        self.configure(font=font_)

    def edit(self, location: tuple = None, size: tuple = None, text: str = None, background_color: tuple = None, fore_color: tuple = None, font_size: int = None, bold: bool = None,
             font_style: str = None, align: str = None):
        if text is not None:    self.configure(text=text)
        if location is None:    location = (float(self.place_info()["x"]), float(self.place_info()["y"]))
        if size is None:        size = (float(self.place_info()["width"]), float(self.place_info()["height"]))

        self.place(x=location[0], y=location[1], width=size[0], height=size[1])
        if background_color is not None: self.configure(bg=_from_rgb(background_color))
        if fore_color is not None: self.configure(fg=_from_rgb(fore_color))
        if align is not None:
            if align.lower() in ('left', 'l'):  self.configure(justify='left')
            if align.lower() in ('right', 'r'):  self.configure(justify='right')
            if align.lower() in ('center', 'c'):  self.configure(justify='center')
        if font_style is not None:
            self.font_style = font_style
        if font_size is not None:
            self.font_size = font_size
        if bold is not None:
            self.bold = bold

        font_ = []
        # font_.append(font_style) if font_style is not None else font_.append(self.font_style)
        font_.append(self.font_style)
        font_.append(self.font_size)
        font_.append(self.bold)
        # font_.append(font_size) if font_size is not None else font_.append(self.font_size)
        # font_.append(bold) if bold else font_.append(self.bold)
        #self.configure(font=(font_style, 20))
        font_ = tuple(font_)
        self.configure(font=font_)

    def get_text(self):
        return self.cget("text")


def new_Timer(seconds: float, repeat: bool = False, on_tick=None):
    item = Timer()
    item.create(seconds, repeat, on_tick)
    return item


class Timer:

    def __int__(self, seconds, repeat, todo_on_tick):
        self.seconds = seconds
        self.repeat = repeat
        self.todo_on_tick = todo_on_tick
        self._stop = False
        self.ticking = False

    def create(self, seconds: int, repeat: bool = False, todo_on_tick=None):
        self.__int__(seconds, repeat, todo_on_tick)

    def edit(self, seconds: int = None, repeat: bool = None, on_tick=None):
        todo_on_tick = on_tick
        if seconds is not None:    self.seconds = seconds
        if repeat is not None:    self.repeat = repeat
        if todo_on_tick is not None: self.todo_on_tick = todo_on_tick

    def start(self):
        global _globals

        def tick():
            if self.todo_on_tick is not None:   self.todo_on_tick()

            if self._stop:
                self._stop = False
                return

            if self.repeat:
                global _globals
                _globals["root"].after(int(self.seconds * 1000), tick)

        if self.ticking: return

        _globals["root"].after(int(self.seconds * 1000), tick)
        self.ticking = True

    def stop(self):
        self._stop = True
        self.ticking = False


def new_Button(location: tuple = None, size: tuple = None, text: str = None, todo=None, image_file_path: str = None, background_color: tuple = None, destroy_on_click: bool = None):
    item = Button(bd=0)
    if destroy_on_click is None:
        destroy_on_click = False
    else:
        destroy_on_click = True
    item.create(location, size, text, todo, image_file_path, background_color, destroy_on_click)
    return item


class Button(tkinter.Button):

    def __int__(self, todo_on_click, destroy_on_click):
        self.todo_on_click = todo_on_click
        self.destroy_on_click = destroy_on_click

    def create(self, location: tuple = None, size: tuple = None, text: str = None, todo_on_click=None, image_file_path: str = None, background_color: tuple = None, destroy_on_click: bool = None):
        global _globals
        self.__int__(todo_on_click, destroy_on_click)
        self.master = _globals["root"]
        if text is not None:
            self.configure(text=text)
        else:
            self.configure(text="Button")

        if location is None:
            self.location = (0, 0)
        else:
            self.location = location

        if size is None:
            self.size = (100, 25)
        else:
            self.size = size

        if image_file_path is None:
            self.image_file_path = ""
        else:
            self.image_file_path = create_image(image_file_path, (self.size[0], self.size[1]))

        if background_color is not None: self.configure(bg=_from_rgb(background_color))
        if background_color is not None: self.configure(highlightbackground=_from_rgb(background_color))

        self.place(x=self.location[0], y=self.location[1], width=self.size[0], height=self.size[1])

        def callback():
            if self.todo_on_click is not None:
                self.todo_on_click()
            if self.destroy_on_click:
                self.destroy()

        self.configure(command=callback, image=self.image_file_path)
        # self.configure(image=self.image_file_path)
        # self.bind('<Button-1>', callback)

    def edit(self, location: tuple = None, size: tuple = None, text: str = None, todo=None, image_file_path: str = None, background_color: tuple = None, destroy_on_click: bool = None):
        todo_on_click = todo
        if text is not None:    self.configure(text=text)
        if location is None:    self.location = (float(self.place_info()["x"]), float(self.place_info()["y"]))
        if size is None:        self.size = (float(self.place_info()["width"]), float(self.place_info()["height"]))
        if background_color is not None: self.configure(bg=_from_rgb(background_color))
        if destroy_on_click is not None: self.destroy_on_click = destroy_on_click
        self.place(x=self.location[0], y=self.location[1], width=self.size[0], height=self.size[1])
        if todo_on_click is not None: self.configure(command=todo_on_click)
        if todo_on_click is not None: self.todo_on_click = todo_on_click
        if image_file_path is not None:
            self.image_file_path = create_image(image_file_path, (self.size[0], self.size[1]))

        def callback():
            if self.todo_on_click is not None:
                self.todo_on_click()

        self.configure(command=callback, image=self.image_file_path)


def new_Image(image_file_path: str = None, location: tuple = None, size: tuple = None, text: str = None, background_color: tuple = None, image_from_cv2 = None):
    item = IImage()
    item.create(image_file_path, location, size, text, background_color, image_from_cv2)
    return item


def resizeImage(img, newWidth, newHeight):
    oldWidth = img.width()
    oldHeight = img.height()
    newPhotoImage = PhotoImage(width=newWidth, height=newHeight)
    for x in range(newWidth):
        for y in range(newHeight):
            xOld = int(x * oldWidth / newWidth)
            yOld = int(y * oldHeight / newHeight)
            rgb = '#%02x%02x%02x' % img.get(xOld, yOld)
            newPhotoImage.put(rgb, (x, y))
    return newPhotoImage


class IImage(tkinter.Label):
    def __int__(self):
        self.image = None

    def create(self, image_file_path: str = None, location: tuple = None, size: tuple = None, text: str = None, background_color: tuple = None, image_from_cv2 = None):
        global _globals
        # default
        self.__int__()
        self.master = tkinter.Label(_globals["root"])
        if text is not None:        self.configure(text=text)
        if location is None:        location = (0, 0)
        if size is None:            size = (100, 100)
        # if image_file_path is None:
        #     image_file_path = "default.png"
        # _globals["images"][name] = create_image(image_location, size)
        if background_color is not None: self.configure(bg=_from_rgb(background_color))
        if image_file_path is not None:
            self.image = create_image(image_file_path, size)
            self.configure(image=self.image)
        if image_from_cv2 is not None:
            image_from_cv2 = cv2.resize(image_from_cv2, (int(size[0]), int(size[1])), interpolation=cv2.INTER_LINEAR)
            b, g, r = cv2.split(image_from_cv2)
            # cv2.resize(image_from_cv2, (int(size[0]), int(size[1])), interpolation=cv2.INTER_LINEAR)
            im = cv2.merge((r, g, b))
            im = Image.fromarray(im)
            img_tk = ImageTk.PhotoImage(image=im)
            self.image = img_tk
            self.configure(image=img_tk)
        self.place(x=location[0], y=location[1], width=size[0], height=size[1])

    def edit(self, image_file_path: str = None, location: tuple = None, size: tuple = None, text: str = None, background_color: tuple = None, image_from_cv2 = None):
        global _globals
        # default
        if text is not None:    self.configure(text=text)
        if location is None:    location = (float(self.place_info()["x"]), float(self.place_info()["y"]))
        if size is None:        size = (float(self.place_info()["width"]), float(self.place_info()["height"]))
        if background_color is not None: self.configure(bg=_from_rgb(background_color))
        # if image_file_path is None:
        #     image_file_path = "default.jpg"

        if image_file_path is not None:
            self.image = create_image(image_file_path, size)
            self.configure(image=self.image)
        if image_from_cv2 is not None:
            image_from_cv2 = cv2.resize(image_from_cv2, (int(size[0]), int(size[1])), interpolation=cv2.INTER_LINEAR)
            b, g, r = cv2.split(image_from_cv2)
            # cv2.resize(image_from_cv2, (int(size[0]), int(size[1])), interpolation=cv2.INTER_LINEAR)
            im = cv2.merge((r, g, b))
            im = Image.fromarray(im)
            img_tk = ImageTk.PhotoImage(image=im)
            self.image = img_tk
            self.configure(image=img_tk)

        self.place(x=location[0], y=location[1], width=size[0], height=size[1])

    def get_location(self) -> list:
        return [float(self.place_info()["x"]), float(self.place_info()["y"])]


def new_TextBox(location: tuple = None, size: tuple = None, text: str = None):
    item = Text()
    item.create(location, size, text)
    return item


class Text(tkinter.Text):

    def create(self, location: tuple = None, size: tuple = None, text: str = None):
        global _globals

        self.master = _globals['root']

        # if text is not None:    self.configure(text=text)
        if location is None:    location = (0, 0)
        if size is None:        size = (100, 25)

        self.place(x=location[0], y=location[1], width=size[0], height=size[1])

    def edit(self, location: tuple = None, size: tuple = None, text: str = None):
        if text is not None:
            self.delete(0.0, float(len(self.get_text())))
            self.insert(0.0, text)
        if location is None:    location = (float(self.place_info()["x"]), float(self.place_info()["y"]))
        if size is None:        size = (float(self.place_info()["width"]), float(self.place_info()["height"]))

        self.place(x=location[0], y=location[1], width=size[0], height=size[1])

    def get_text(self) -> str:
        return str(self.get(1.0, "end-1c"))

create_window()
