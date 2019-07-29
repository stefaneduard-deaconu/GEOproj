"""
beginning of project application.
"""
from turtle import Turtle


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


def click_event(x_coord, y_coord):
    if taking_input:
        points.append((x_coord, y_coord))
    else:
        pass


def enter_event():
    print('enter was pressed :D')


def game():
    pass


def main():
    """
    The starting function.
    lays down the ground for the app
    and sets the corresponding handlers
    """
    # getting the turtle
    t = Turtle()
    t.hideturtle()
    # getting the screen
    window = t.screen

    # setting the window dimensions:
    window.setup(width=0.618, height=0.8, startx=0, starty=0)
    screen_width, screen_height = screen_dimensions()
    window_width, window_height = 0.618 * screen_width, 0.8 * screen_height

    # now center the window:
    startx_centered = (screen_width - window_width) // 2
    starty_centered = (screen_height - window_height) // 2

    window.setup(width=0.618, height=0.8,
              startx=startx_centered, starty=starty_centered)

    # True because we want to add multiple handlers, not replace them :)
    t.onclick(click_event, btn=1, add=True)
    window.onkey(enter_event, 'enter')

    # game()
    window.mainloop()


if __name__ == '__main__':
    main()
