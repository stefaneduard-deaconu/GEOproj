"""
Here we have two utility functions, for y-decomposition (decomposing a
  polygon in y-monotone polygons), and the triangulation of a y-monotone
  polygon.
Plus the main() function, used throughout the project for testing:D
"""


def y_decompose(polygon):
    def sign(num):
        if num < 0:
            return -1
        elif num > 0:
            return 1
        else:
            return 0

    def trig_order(a, b, c):
        res = a[0] * b[1] + b[0] * c[1] + c[0] * a[1]
        res -= c[0] * b[1] + b[0] * a[1] + a[0] * c[1]
        if sign(res) == -1:
            return 'rightturn'
        else:
            return 'leftturn'

    def get_types(pts):
        # print('\n', [pts[-1]])
        # print('\n', pts)
        # print('\n', [pts[0]])
        aux = [pts[-1]] + [p for p in pts] + [pts[0]]
        # print('\n', aux)
        #
        types = {}
        for A, B, C in zip(aux, aux[1::], aux[2::]):
            if sign(B[1] - A[1]) != sign(B[1] - C[1]):
                types.update(dict({B: trig_order(A, B, C)}))
            elif trig_order(A, B, C) == 'rightturn':  # start or end
                if sign(B[1] - A[1]) == 1:  # start or end
                    types.update(dict({B: 'start'}))  # start
                else:
                    types.update(dict({B: 'end'}))  # end
            else:  # split or merge ----> 'leftturn'
                if sign(B[1] - A[1]) == 1:  # split or merge
                    types.update(dict({B: 'split'}))  # split
                else:
                    types.update(dict({B: 'merge'}))  # merge
        return [types[p] for p in pts]  # the order is odd
    from pprint import pprint
    pprint(get_types(polygon))


def triangulate(y_polygon):
    pass

# for testing:

def sign(num):
    if num < 0:
        return -1
    elif num > 0:
        return 1
    else:
        return 0

def trig_order(a, b, c):
    res = a[0] * b[1] + b[0] * c[1] + c[0] * a[1]
    res -= c[0] * b[1] + b[0] * a[1] + a[0] * c[1]
    if sign(res) == 1:
        return 'leftturn'
    else:
        return 'rightturn'

def main():
    polygons = [
        [(-124.0, 181.0), (-62.0, 103.0), (81.0, 181.0), (129.0, 22.0), (-37.0, 33.0), (80.0, -149.0), (-154.0, -166.0), (-203.0, 212.0), (-139.0, 62.0), (-37.0, 56.0), (-177.0, 205.0), (-48.0, 254.0)],
        [(115.0, -59.0), (142.0, 136.0), (9.0, 85.0), (-95.0, 176.0), (-82.0, -152.0), (71.0, 30.0)],
        [(-176.0, 140.0), (-186.0, 98.0), (55.0, 186.0), (14.0, 6.0), (184.0, 81.0), (234.0, -118.0), (-92.0, -116.0), (-31.0, 80.0), (-228.0, -149.0), (-245.0, 197.0)],
        [(-289.0, 194.0), (-182.0, 219.0), (24.0, 77.0), (117.0, 220.0), (162.0, 27.0), (307.0, 141.0), (215.0, -245.0), (88.0, 18.0), (-159.0, -208.0), (44.0, -141.0), (70.0, -263.0), (-239.0, -247.0), (-334.0, 153.0), (-259.0, 63.0), (-64.0, 51.0), (-226.0, -18.0), (-230.0, -114.0), (-6.0, 52.0)],
        [(-200, -200), (-200, 200), (200, 200), (200, -200)],
        [(0, 200), (200, 0), (0, -200), (-200, 0)],
        [(0, 200), (200, -200), (0, 0), (-200, -200)]
    ]

    def draw_poly(polygon):
        import turtle
        tad = turtle.Turtle()
        tad.penup()
        tad.goto(polygon[0])
        tad.pendown()
        for p in polygon + [polygon[0]]:
            tad.goto(p[0], p[1])
        tad.screen.mainloop()

    def reverse_trig_ordered(polygon):
        # function to test if the polygon's border order is in (app.) trig order
        index = polygon.index((max(polygon, key=lambda A: A[1])))
        A, B = polygon[index - 1], polygon[index]
        C = polygon[(index + 1) % len(polygon)]
        if trig_order(A, B, C) == 'leftturn':
            return True
        else:
            return False

    for poly in polygons:
        print(reverse_trig_ordered(poly))
        if reverse_trig_ordered(poly):
            print(poly[-len(poly):])
        else:
            print(poly)
    for poly in polygons[1:2]:
        draw_poly(poly)
        y_decompose(poly)

if __name__ == '__main__':
    main()
