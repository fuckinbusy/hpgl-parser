from re import findall, DOTALL
from math import hypot
from tkinter import filedialog as fd
import matplotlib.pyplot as plt

path = fd.askopenfile(filetypes=[("HPGL", "*.plt")])

def getLength(filePath: str, pointsPerMm: int) -> int:
    with open(filePath, 'rb') as file:
        hpgl = file.read().decode('utf-8')

        pattern = r"(LT;|SP\d+;)(.*?)(LT;|SP\d+;$)" 
        objects = findall(pattern, hpgl, DOTALL)

        total = 0
        for obj in objects:
            c = obj[1]

            code_pattern = r'(PU|PD)(-?\d+)\s(-?\d+)'
            points = findall(code_pattern, c)

            length = 0
            prev_x, prev_y = map(int, points[0][1:])
            for i in range(len(points)):
                command, x, y = points[i]
                x, y = map(int, (x, y))

                if command == "PD":
                    length += hypot(x-prev_x, y-prev_y)
                    prev_x, prev_y = x, y
                elif command == "PU":
                    continue

            total += length

    return int(total/(pointsPerMm*1000))

def draw(filePath: str):
    with open(filePath, 'rb') as file:
        hpgl = file.read().decode('utf-8')

        pattern = r"(LT;|SP\d+;)(.*?)(LT;|SP\d+;$)" 
        objects = findall(pattern, hpgl, DOTALL)
        
        total = 0
        for obj in objects:
            c = obj[1]
            x_ = []
            y_ = []

            code_pattern = r'(PU|PD)(-?\d+)\s(-?\d+)'
            points = findall(code_pattern, c)

            length = 0
            prev_x, prev_y = map(int, points[0][1:])
            for i in range(len(points)):
                command, x, y = points[i]
                x, y = map(int, (x, y))
                x_.append(x)
                y_.append(y)
            plt.plot(x_, y_)


    plt.show()

print(getLength(path.name, 0.04))
draw(path.name)