from re import findall, DOTALL
from math import hypot
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter, PillowWriter

path = fd.askopenfile(filetypes=[("HPGL", "*.plt")])
patterns = {
    'LT_SP': r"(LT;|SP\d+;)(.*?)(LT;|SP\d+;$)",
    'PU_PD': r"(PU|PD)(-?\d+)\s(-?\d+)"
}


def get_length(file_path: str, points_per_mm: float) -> int:
    with open(file_path, 'rb') as file:
        hpgl = file.read().decode('utf-8')
        objects = findall(patterns['LT_SP'], hpgl, DOTALL)

        total = 0
        for obj in objects:
            c = obj[1]
            points = findall(patterns['PU_PD'], c)

            length = 0
            prev_x, prev_y = map(int, points[0][1:])
            for i in range(len(points)):
                command, x, y = points[i]
                x, y = map(int, (x, y))

                if command == "PD":
                    length += hypot(x - prev_x, y - prev_y)
                    prev_x, prev_y = x, y
                elif command == "PU":
                    continue

            total += length

    return int(total / (points_per_mm * 1000))


def draw(file_path: str):
    plt.clf()
    plt.autoscale()
    plt.axis('off')
    plt.gca().set_aspect('equal')
    with open(file_path, 'rb') as file:
        hpgl = file.read().decode('utf-8')
        objects = findall(patterns['LT_SP'], hpgl, DOTALL)

        for obj in objects:
            c = obj[1]
            x_ = []
            y_ = []

            points = findall(patterns['PU_PD'], c)
            for i in range(len(points)):
                _, x, y = points[i]
                x, y = map(int, (x, y))
                x_.append(x)
                y_.append(y)

            plt.plot(x_, y_, '-b')

    plt.show()


def visualization_mp4(file_path: str, fps: int = 15, dpi: int = 100, output_name: str = "visual"):
    plt.clf()
    l, = plt.plot([], [], 'k-')
    plt.autoscale()
    plt.axis('off')
    plt.gca().set_aspect('equal')
    fig = plt.gcf()
    with open(file_path, 'rb') as file:
        metadata = dict(title='Vector objects visualization | by richard')
        writer = FFMpegWriter(fps=fps, metadata=metadata)

        hpgl = file.read().decode('utf-8')
        objects = findall(patterns['LT_SP'], hpgl, DOTALL)
        objects_total = len(objects)
        objects_list = __create_list_of_objects(objects)

        with writer.saving(fig, output_name + ".mp4", dpi):
            for num, obj in enumerate(objects_list):
                print(f"[MP4] Drawing {num + 1}/{objects_total}")
                x = objects_list[obj]['x']
                y = objects_list[obj]['y']
                plt.plot(x, y, '-b')
                l.set_data(x, y)
                writer.grab_frame()


def visualization_gif(file_path: str, fps: int = 15, dpi: int = 100, output_name: str = "visual"):
    plt.clf()
    l, = plt.plot([], [], 'k-')
    plt.autoscale()
    plt.axis('off')
    plt.gca().set_aspect('equal')
    fig = plt.gcf()
    with open(file_path, 'rb') as file:
        metadata = dict(title='Vector objects visualization | by richard')
        writer = PillowWriter(fps=fps, metadata=metadata)

        hpgl = file.read().decode('utf-8')
        objects = findall(patterns['LT_SP'], hpgl, DOTALL)
        objects_total = len(objects)
        objects_list = __create_list_of_objects(objects)

        with writer.saving(fig, output_name + ".gif", dpi):
            for num, obj in enumerate(objects_list):
                print(f"[GIF] Drawing {num + 1}/{objects_total}")
                x = objects_list[obj]['x']
                y = objects_list[obj]['y']
                plt.plot(x, y, '-b')
                l.set_data(x, y)
                writer.grab_frame()


def __create_list_of_objects(list_of_objects) -> dict:
    objects = {}
    for num, obj in enumerate(list_of_objects):
        c = obj[1]
        x_ = []
        y_ = []
        points = findall(patterns['PU_PD'], c)
        for i in range(len(points)):
            _, x, y = points[i]
            x, y = map(int, (x, y))
            x_.append(x)
            y_.append(y)

        objects[f'object_{num}'] = dict(x=x_, y=y_)
    print(objects)
    return objects


# here I set 0.04 because this is for CorelDraw '.plt' files
print(get_length(path.name, 0.04))

draw(path.name)
visualization_gif(path.name)
visualization_mp4(path.name)
