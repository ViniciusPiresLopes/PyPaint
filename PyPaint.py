import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pygame
import time
import os

pygame.init()

# Defining window
window_size = width, height = 600, 600,
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("PyPaint")
window_color = (255, 255, 255)
window.fill(window_color)


class Mouse:
    def __init__(self):
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]

    def is_clicked(self, button):
        return pygame.mouse.get_pressed()[button]

    def get_x(self):
        self.x = pygame.mouse.get_pos()[0]
        return self.x

    def get_y(self):
        self.y = pygame.mouse.get_pos()[1]
        return self.y


class Brush():
    def __init__(self, inital_RGB, radius):
        self.RGB = inital_RGB
        self.radius = radius
        self.speed = 0.1
        self.max = 30
        self.min = 3
        self.last_RGB = None

    def draw(self, x, y):
        pygame.draw.circle(window, self.RGB, (x, y), round(self.radius))

    def draw_new_brush(self, x, y, RGB, radius):
        pygame.draw.circle(window, RGB, (x, y), round(radius))


# Main variables
quad_lenght = 50
quad_x = 0
quad_y = window_size[1] - quad_lenght
quad_sep = 10
list_brushes_positions = []
list_brushes_RGBs = []
list_brushes_sizes = []
saved_file = False

# Main objects (classes: ColorQuad, Mouse)
mouse = Mouse()
brush = Brush((0, 0, 0), 5)


def open_file():
    global list_brushes_positions
    global list_brushes_RGBs
    global list_brushes_sizes

    print("Loading...")

    root = tk.Tk()

    my_file_types = [("PyPaint files", ".pypnt")]

    file_path = filedialog.askopenfilename(parent=root, initialdir=os.getcwd(), title="Select PyPaint file:", filetypes=my_file_types)

    root.destroy()

    if file_path == "":
        print("Open file was cancelled!")
        return False

    print("Opening from: ", file_path)

    try:
        file = open(file_path, "r")
    except FileNotFoundError:
        print(f"{file_path} does not exist!")
        return False

    content = file.readlines()
    list_brushes_positions.clear()
    list_brushes_RGBs.clear()
    list_brushes_sizes.clear()

    element1 = content[0]
    element1 = element1.split(";")
    element1.pop(-1)

    for i in range(len(element1)):
        coordinates = element1[i]
        coordinates = coordinates.split(",")
        coordinates = (int(coordinates[0]), int(coordinates[1]))

        list_brushes_positions.append(coordinates)

    element2 = content[1]
    element2 = element2.split(";")
    element2.pop(-1)

    for i in range(len(element2)):
        RGB = element2[i]
        RGB = RGB.split(",")
        RGB = (int(RGB[0]), int(RGB[1]), int(RGB[2]))

        list_brushes_RGBs.append(RGB)

    element3 = content[2]
    element3 = element3.split(";")
    element3.pop(-1)

    for i in range(len(element3)):
        brush_size = element3[i]
        brush_size = brush_size.split(",")
        brush_size = int(float(brush_size[0]))

        list_brushes_sizes.append(brush_size)

    file.close()
    print("Done!")
    return True


def save_file():
    print(f"{len(list_brushes_positions)} circles on this file.")
    print("Loading...")

    root = tk.Tk()

    my_file_types = [("PyPaint files", ".pypnt")]

    file_path = filedialog.asksaveasfilename(parent=root, initialdir=os.getcwd(), title="Save PyPaint file:", filetypes=my_file_types)

    root.destroy()

    if file_path == "":
        print("Save file was cancelled!")
        return False

    print("Saving on: ", file_path)

    file = open(file_path + ".pypnt", "w")

    for element in list_brushes_positions:
        file.write(str(element[0]) + "," + str(element[1]) + ";")
    file.write("\n")

    for element in list_brushes_RGBs:
        file.write(str(element[0]) + "," + str(element[1]) + "," + str(element[2]) + ";")
    file.write("\n")

    for element in list_brushes_sizes:
        file.write(str(element) + ";")
    file.write("\n")

    file.close()
    print("Done!")
    return True


def undo(speed=1):
    try:
        for i in range(speed):
            list_brushes_positions.pop(-1)
            list_brushes_RGBs.pop(-1)
            list_brushes_sizes.pop(-1)
    except IndexError:
        print("Can not undo anymore!")


def open_RGB_menu():
    colors = {"white": (255, 255, 255), "red": (255, 0, 0), "blue": (0, 0, 255),
              "green": (0, 204, 0), "pink": (255, 51, 255), "brown": (51, 25, 0),
              "yellow": (255, 255, 51), "grey": (128, 128, 128), "orange": (255, 128, 0),
              "purple": (102, 0, 204), "black": (0, 0, 0)}

    def set_brush_RGB():
        color = input_color.get().strip()

        if colors.get(color) is not None:
            RGB = colors.get(color)
            R = RGB[0]
            G = RGB[1]
            B = RGB[2]

        else:
            R = input_R.get()
            G = input_G.get()
            B = input_B.get()

        brush.RGB = (R, G, B)
        root.destroy()

    def display_preview():
        R = input_R.get()
        G = input_G.get()
        B = input_B.get()
        colorval = "#%02x%02x%02x" % (R, G, B)
        canvas.itemconfig(rectangle, fill=colorval)

    # Window
    root = tk.Tk()
    root.geometry("250x150")
    root.resizable(0, 0)
    root.title("Set RGB")

    # Text
    text = tk.Label(root, text="R  G  B")
    text.pack()

    # Entry
    input_color = tk.Entry(root, justify="center")
    input_color.pack()

    # Input scales
    input_R = tk.Scale(root, from_=0, to=255)
    input_R.pack(side=tk.LEFT)

    input_G = tk.Scale(root, from_=0, to=255)
    input_G.pack(side=tk.LEFT)

    input_B = tk.Scale(root, from_=0, to=255)
    input_B.pack(side=tk.LEFT)

    # Canvas
    canvas = tk.Canvas(root, width=50, height=60)
    canvas.pack()
    rectangle = canvas.create_rectangle(50, 50, 25, 25)

    # Button to preview the color
    button_preview = tk.Button(root, text="PREVIEW", width=10, command=display_preview)
    button_preview.pack()

    # Button to set the color
    button_close = tk.Button(root, text="OK", width=10, command=set_brush_RGB, pady=5)
    button_close.pack()

    # Main loop tkinter
    root.mainloop()


def draw():
    """
    Draw Everything on the screen
    """
    if mouse.is_clicked(0):
        if (mouse.get_x(), mouse.get_y()) in list_brushes_positions:
            index = list_brushes_positions.index((mouse.get_x(), mouse.get_y()))
            list_brushes_RGBs[index] = brush.RGB
            list_brushes_sizes[index] = brush.radius
        else:
            list_brushes_positions.append((mouse.get_x(), mouse.get_y()))
            list_brushes_RGBs.append(brush.RGB)
            list_brushes_sizes.append(brush.radius)

    else:
        brush.draw(mouse.get_x(), mouse.get_y())

    for i in range(len(list_brushes_positions)):
        brush.draw_new_brush(list_brushes_positions[i][0], list_brushes_positions[i][1], list_brushes_RGBs[i], list_brushes_sizes[i])

    pygame.display.update()
    window.fill(window_color)


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            if not saved_file and len(list_brushes_positions) + len(list_brushes_RGBs) + len(list_brushes_sizes) > 0:
                root = tk.Tk()
                answer = messagebox.askyesnocancel("Warning", "Do you want to save the file, before closing?")
                root.destroy()

                if answer:
                    save_file()

            running = False

    key = pygame.key.get_pressed()

    if key[pygame.K_LSHIFT]:
        if brush.radius <= brush.max:
            brush.radius += brush.speed

    if key[pygame.K_LALT]:
        if brush.radius >= brush.min:
            brush.radius -= brush.speed

    if key[pygame.K_LCTRL] and key[pygame.K_z]:
        undo()

    if key[pygame.K_LCTRL] and key[pygame.K_s]:
        saved_file = save_file()

    if key[pygame.K_LCTRL] and key[pygame.K_o]:
        open_file()

    if key[pygame.K_LCTRL] and key[pygame.K_n]:
        list_brushes_positions.clear()
        list_brushes_RGBs.clear()
        list_brushes_sizes.clear()

    if key[pygame.K_LCTRL] and key[pygame.K_r]:
        open_RGB_menu()

    draw()

pygame.quit()
