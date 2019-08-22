"""
beginning of project application.
"""
import turtle
import tkinter as tk
import time

'''
global variables, used for events
- taking_input ----> true at the beginning,
    when we click the screen to get the input points :)
- points ----> the points of the geometrical figure :D
'''
taking_input = True
polygon = []


def screen_dimensions():
    # A simple function to compute the screen's dimensions.
    import ctypes
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


def line(A, B, tad, color):
    x0, y0, x1, y1 = A[0], A[1], B[0], B[1]
    tads_position = tad.position()
    tads_color = tad.color()
    tad.color(color, color)
    tad.penup()
    tad.goto(x0, y0)
    tad.pendown()
    tad.goto(x1, y1)
    tad.penup()
    tad.goto(tads_position)
    tad.color(tads_color[0], tads_color[1])


"""
###############
Event handlers.
###############
"""


def draw_to_point(x=None, y=None):
    # if we presses the start button, then ...
    #
    print('draw:')
    tad.goto(x, y)
    polygon.append((x, y))
    # print(polygon)


def first_point(x=None, y=None):
    # TODO  if outside, better reset() everything
    print('first:')
    tad.penup()
    tad.goto(x, y)
    tad.pendown()
    polygon.clear()
    polygon.append((x, y))  # first point
    # print(polygon)
    tad.screen.onclick(draw_to_point, btn=1)


def start(event):
    """
    This even happens after giving the input.
    The target is to triangulate the polygon
    """
    print('you pressed "Start"')
    print(polygon)
    # finish the polygon:
    tad.goto(polygon[0][0], polygon[0][1])
    print(polygon)
    # Tad. Go sit
    tad.penup()
    tad.shapesize(3, 3)
    tad.setheading(90)
    screen_width, screen_height = screen_dimensions()
    window_width, window_height = 0.618 * screen_width, 0.8 * screen_height
    tad.goto(window_width * 0.9 // 2, window_height * 0.9 // 2)
    #
    quit()
    from triangles import y_decompose
    """
    Function that given the border of a polygon, generates a decomposition
        of it as y-monotone polygons.
    """
    from triangles import triangulate
    """
    Function that given a y-monotone polygon,
        returns one of its triangulations, as a list of triangles.
    """
    y_polygons = y_decompose(polygon)
    # triangles = []
    # for poly in y_polygons:
    #     triangles += triangulate(poly)

    def draw_triangles():
        pass


def exercise_1(event):
    print('you presses button "1"')


def exercise_2(event):
    print('you presses button "2"')


def exercise_3(event):
    print('you presses button "3"')


def exercise_4(event):
    print('you presses button "4"')


def reset_canvas(event):
    print('you pressed "Reset"')
    tad.clear()
    tad.shapesize(1)
    screen_width, screen_height = screen_dimensions()
    window_width, window_height = 0.618 * screen_width, 0.8 * screen_height
    # using the turtle to first draw the 'coordinate axes' :D
    line((-window_width * 0.9 // 2, 0), (window_width * 0.9 // 2, 0), tad, 'white')
    tad.setheading(90)
    line((0, -window_height * 0.9 // 2), (0, window_height * 0.9 // 2), tad, 'white')
    tad.color('lime', 'lime')
    tad.goto(0, 0)
    # rebind the event handler for capturing the polygon

    tad.screen.onclick(first_point, btn=1)

def set_gui():
    """
    The starting function.
    lays down the ground for the app
    and sets the corresponding handlers
    """
    # # setting the background color
    # turtle.bgcolor('black')
    # # getting the turtle
    #
    screen_width, screen_height = screen_dimensions()
    window_width, window_height = 0.618 * screen_width, 0.8 * screen_height
    #
    root = tk.Tk(screenName='turtle', baseName='turtle')
    canvas = tk.Canvas(width=window_width, height=window_height)

    # creating the grid:
    start_button = tk.Button(cnf={'text': 'Start', 'width': '25', 'height': '3'})
    start_button.grid(row=0, column=0, rowspan=2, sticky='W')
    reset_button = tk.Button(cnf={'text': 'Reset', 'width': '25', 'height': '3'})
    reset_button.grid(row=0, column=1, rowspan=2, sticky='E')

    button_1 = tk.Button(cnf={'text': '1', 'width': '10'})
    button_1.grid(row=0, column=0, sticky='E')
    button_2 = tk.Button(cnf={'text': '2', 'width': '10'})
    button_2.grid(row=0, column=1, sticky='W')
    button_3 = tk.Button(cnf={'text': '3', 'width': '10'})
    button_3.grid(row=1, column=0, sticky='E')
    button_4 = tk.Button(cnf={'text': '4', 'width': '10'})
    button_4.grid(row=1, column=1, sticky='W')

    canvas.grid(row=2, column=0, columnspan=2)

    tad = turtle.RawTurtle(canvas)
    tad.color('white', 'white')
    tad.speed(10)
    tad.shapesize(1)

    # now center the window:
    root.resizable(0, 0)
    # the first one must be -7 as to be leftmost on windows 10 :))
    x_centered = int((screen_width - window_width) // 2)
    y_first_fifth = int((screen_height - window_height) // 5)
    root.geometry('+{}+{}'.format(x_centered, y_first_fifth))  # these correspond
    # to xstart and ystart in turtle.screen.setup :D
    canvas.config(bg='black')
    tad.color('lime', 'lime')

    # using the turtle to first draw the 'coordinate axes' :D

    line((-window_width * 0.9 // 2, 0), (window_width * 0.9 // 2, 0), tad, 'white')
    tad.setheading(90)
    line((0, -window_height * 0.9 // 2), (0, window_height * 0.9 // 2), tad, 'white')
    tad.color('lime', 'lime')

    start_button.bind('<Button-1>', start)
    reset_button.bind('<Button-1>', reset_canvas)
    button_1.bind('<Button-1>', exercise_1)
    button_2.bind('<Button-1>', exercise_2)
    button_3.bind('<Button-1>', exercise_3)
    button_4.bind('<Button-1>', exercise_4)

    tad.screen.onclick(first_point)

    return root, tad


root, tad = set_gui()


def main():
    root.mainloop()


if __name__ == '__main__':
    main()


    # list(map(int, input('Enter numbers: ').split())) ---> for later
