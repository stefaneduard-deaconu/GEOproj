import tkinter as tk


def main():
    root = tk.Tk()
    grid = tk.Grid()

    import ctypes
    user32 = ctypes.windll.user32
    screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    window_width, window_height = 0.618 * screen_width, 0.8 * screen_height

    start_button = tk.Button(cnf={'text': 'Start', 'width': '25', 'height': '3'})
    reset_button = tk.Button(cnf={'text': 'Reset', 'width': '25', 'height': '3'})

    canvas = tk.Canvas(width=window_width, height=window_height)

    start_button.grid(row=0, column=0, rowspan=2, sticky='W')
    tk.Button(cnf={'text': '1', 'width': '10'}).grid(row=0, column=0, sticky='E')
    tk.Button(cnf={'text': '2', 'width': '10'}).grid(row=0, column=1, sticky='W')
    reset_button.grid(row=0, column=2, rowspan=2, sticky='E')

    tk.Button(cnf={'text': '3', 'width': '10'}).grid(row=1, column=0, sticky='E')
    tk.Button(cnf={'text': '4', 'width': '10'}).grid(row=1, column=1, sticky='W')

    canvas.grid(row=2, column=0, columnspan=2)

    print(root)

    root.mainloop()


if __name__ == '__main__':
    main()
