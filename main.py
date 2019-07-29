"""
beginning of project application.
"""
import turtle


'''
global variables, used for events
- taking_input ----> true at the beginning,
    when we click the screen to get the input points :)
- points ----> the points of the geometrical figure :D
'''
taking_input = True
points = []


def screen_dimensions():
    # A simple function to compute the screen's dimensions.
    import ctypes
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


def main():
    """
    The starting function.
    lays down the ground for the app
    and sets the corresponding handlers
    """
    # setting the background color
    turtle.bgcolor('black')
    # getting the turtle
    print(turtle.getshapes())
    tad = turtle.Turtle(shape='triangle')
    tad.color('white', 'white')
    tad.speed(10)
    tad.shapesize(0.5, 0.5)
    # getting the screen
    window = tad.screen

    # setting the window dimensions:
    window.setup(width=0.618, height=0.8, startx=0, starty=0)
    screen_width, screen_height = screen_dimensions()
    window_width, window_height = 0.618 * screen_width, 0.8 * screen_height

    # now center the window:
    startx_centered = (screen_width - window_width) // 2
    starty_centered = (screen_height - window_height) // 2

    window.setup(width=0.618, height=0.8,
                 startx=startx_centered, starty=starty_centered)

    turtle.write('text', move=False, align='left', font=('Arial', 18, 'normal'))
    # tad.color('lime', 'lime')

    # using the turtle to first draw the 'buttons' :D

    def rectangle(A, B):
        x0, y0, x1, y1 = A[0], A[1], B[0], B[1]
        tads_position = tad.position()
        # we could check if the pen is down TODO
        if x0 < x1 or y0 < y1:  # sort them
            x0, y0, x1, y1 = x1, y1, x0, y0
        tad.penup()
        tad.goto(x0, y0)
        tad.pendown()
        for x, y in [(x0, y1), (x1, y1), (x1, y0), (x0, y0)]:
            tad.goto(x, y)
        tad.penup()
        tad.goto(tads_position)

    def line(A, B):
        x0, y0, x1, y1 =  A[0], A[1], B[0], B[1]
        tads_position = tad.position()
        tad.penup()
        tad.goto(x0, y0)
        tad.pendown()
        tad.goto(x1, y1)
        tad.penup()
        tad.goto(tads_position)

    line((-window_width * 0.9 // 2, 0), (window_width * 0.9 // 2, 0))
    tad.setheading(90)
    line((0, -window_height * 0.9 // 2), (0, window_height * 0.9 // 2))
    tad.color('lime', 'lime')

    # tad.penup()
    # tad.setheading(270)
    # tad.backward(window_height * 0.9 // 2)
    # tad.right(90)
    # tad.forward(window_width * 0.9 // 2)
    # rectangle(0, 0, 10, 10)
    # rectangle(100, 100, 110, 110)

    turtle.listen()

    start_button = ((-window_width * 0.9 // 2, window_height * 0.9 // 2 - 30),
                    (-window_width * 0.9 // 2 + 60, window_height * 0.9 // 2))
    reset_button = ((window_width * 0.9 // 2 - 60, window_height * 0.9 // 2 - 30),
                    (window_width * 0.9 // 2, window_height * 0.9 // 2))

    def draw_button(button, text):
        tads_position = tad.position()
        rectangle(button[0], button[1])
        turtle.color('lime', 'lime')
        turtle.penup()
        turtle.goto(button[0])
        turtle.write(text, align='left', font=('Arial', 18, 'normal'))
        tad.goto(tads_position)

    draw_button(start_button, 'start')
    draw_button(reset_button, 'stop')

    def inside(A, button):  # for us, a button is a pair of pairs (tuples)
        # is A inside of the button?
        (x0, y0), (x1, y1) = button[0], button[1]
        if x0 > x1 or y0 > y1:  # sort them
            x0, y0, x1, y1 = x1, y1, x0, y0
        if A[0] >= x0 and A[0] <= x1 and A[1] >= y0 and A[1] <= y1:
            print('true', A, x0, y0, x1, y1)
            return True
        else:
            print('false', A, x0, y0, x1, y1)
            return False

    def draw_to_point(x=None, y=None):
        if inside((x, y), start_button):  # so if it is inside the button
            taking_input = False
        tad.goto(x, y)
        if taking_input:
            points.append((x, y))
        else:
            pass

    def first_point(x=None, y=None):
        # TODO  if outside, better reset() everything
        print('first')
        tad.penup()
        tad.goto(x, y)
        tad.pendown()
        points.append((x, y))
        tad.screen.onclick(draw_to_point, btn=1)

    tad.screen.onclick(first_point)

    turtle.mainloop()

    # x, y = 0, 0
    # print(x, y)


if __name__ == '__main__':
    main()
