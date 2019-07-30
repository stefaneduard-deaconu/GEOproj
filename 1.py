import tkinter as tk


def main():
    root = tk.Tk()

    import ctypes
    user32 = ctypes.windll.user32
    screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    window_width, window_height = 0.618 * screen_width, 0.8 * screen_height

    canvas = tk.Canvas(width=window_width, height=window_height)

    start_button = tk.Button(cnf={'text': 'Start', 'width': '25', 'height': '3'})
    start_button.grid(row=0, column=0, rowspan=2, sticky='W')
    reset_button = tk.Button(cnf={'text': 'Reset', 'width': '25', 'height': '3'})
    reset_button.grid(row=0, column=2, rowspan=2, sticky='E')

    button_1 = tk.Button(cnf={'text': '1', 'width': '10'})
    button_1.grid(row=0, column=0, sticky='E')
    button_2 = tk.Button(cnf={'text': '2', 'width': '10'})
    button_2.grid(row=0, column=1, sticky='W')
    button_3 = tk.Button(cnf={'text': '3', 'width': '10'})
    button_3.grid(row=1, column=0, sticky='E')
    button_4 = tk.Button(cnf={'text': '4', 'width': '10'})
    button_4.grid(row=1, column=1, sticky='W')

    canvas.grid(row=2, column=0, columnspan=2)

    root.mainloop()


if __name__ == '__main__':
    main()
