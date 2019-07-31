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

    def reverse_trig_order(polygon):
        # function to test if the polygon's point order is in (app.) trig order
        index = polygon.index((max(polygon, key=lambda A: A[1])))
        A, B = polygon[index - 1], polygon[index]
        C = polygon[(index + 1) % len(polygon)]
        if trig_order(A, B, C) == 'leftturn':
            return True
        else:
            return False

    if (reverse_trig_order(polygon)):
        polygon = polygon[-len(polygon):]

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
        return types  # we return a dictionary, that says the types of the pts.

    def get_fathers(pts):
        """
        We practically return the neighbor points.
        In the pts, the points are the one of a polygon, so for each index
            the neighbors are the left and right indexed items.
        Only that we only catalogue as 'father' the items with a greate y-coord
        """
        fathers = {}
        for p in pts:
            index = pts.index(p)
            left, right = pts[index - 1], pts[(index + 1) % len(pts)]
            if left[0] > right[0]:  # keep them left to left and right to right
                left, right = right, left
            if types[p] in ['end', 'merge']:  # two fathers
                fathers[p] = [left, right]
            elif types[p] in ['leftturn', 'rightturn']:  # one father; find it
                if left[1] >= right[1]:  # one of them must be so -> the father
                    fathers[p] = [left]
                else:
                    fathers[p] = [right]
        return fathers

    # from pprint import pprint
    types = get_types(polygon)
    fathers = get_fathers(polygon)  # we don't check the trig. order here :D
    # pprint(types)
    # pprint(fathers)
    y_ordered_points = sorted(polygon, key=lambda A: -A[1])
    x_order = {
        point: index for index, point in enumerate(sorted(polygon, key=lambda A: A[0]))
    }
    # pprint(y_ordered_points)

    class Comp(object):
        def __init__(self, given_points, given_state=(None, None)):
            if isinstance(points, tuple):  # first time, just a 'start' !!!!!!!
                # we created a new component from a set of points
                self.points = [given_points]
                self.state = given_state  # given state has state and point
            if isinstance(points, list):
                # we created a new component from a set of points
                self.points = given_points
                self.state = given_state  # given state has state and point
            else:
                print('NOT A LIST - problem with a Comp initialization')

        def get_margins(self):
            if len(points) >= 3:
                return (points[0], points[-1])
            else:
                polygon_index = None
                if types[points[0]] == 'start':
                    polygon_index = polygon.index(points[0])
                else:
                    polygon_index = polygon.index(points[1])
                return (polygon[polygon_index - 1], polygon[polygon_index + 1])

        def turn_to_poly(self):  # TODO
            # we know that every point must have a father, except for the sole
            #   'start' one
            pass

        def add_point(self, point):  # point is a tuple with 2 items
            # we presume there already are points. From the __init__
            # and it's father must be here
            # but we don't place it like in a graph, we only arrange them
            #   when using turn_to_poly
            # (*) does it have a merge? -> NO
            # we update minmax_order
            if self.minmax_order[0] > x_order[point]:
                self.minmax_order = (x_order[point], self.minmax_order[1])
            elif self.minmax_order[1] < x_order[point]:
                self.minmax_order = (self.minmax_order[0], x_order[point])
            self.points.append(point)

        def solve_merge(self, comp):  # used just after we got into a merge state
            print('solving merge')
            pass  # here we merge using a point ,be it middle, merge, split or anything

        # def __str__(self):  # for the pprint
        #     if self.points:
        #         pprint(points)
        #     else:
        #         pprint('no points yet')
        #     if self.state:
        #         pprint(state)
        #     if self.minmax_order:
        #         pprint(minmax_order)
    comps = []
    polys = []  # we can get the polys with a function inside Comp :D
    for cur_index, (x, y) in enumerate(y_ordered_points):
        cur_point = (x, y)

        from pprint import pprint
        print('-' * 50)
        print(cur_point, '\'{}\', x_order={}'.format(types[cur_point], x_order[cur_point]), '----> point {}'.format(cur_index))

        if types[cur_point] == 'start':
            comps.append(
                Comp([cur_point], given_minmax=(
                    x_order[cur_point],
                    x_order[cur_point]
                ))
            )
        else:
            if types[cur_point] == 'merge':
                left_index, right_index = None, None
                left_father, right_father = fathers[cur_point]
                for comp_index, comp in enumerate(comps):
                    if left_father in comp.points:  # right half
                        left_index = comp_index
                    elif right_father in comp.points:  # left half
                        right_index = comp_index
                # we always have two corresponding components when not 'starting' a
                #   new merge
                print(left_index, right_index)
                if left_index < right_index:
                    right_comp = comps.pop(right_index)
                    left_comp = comps.pop(left_index)
                else:
                    left_comp = comps.pop(left_index)
                    right_comp = comps.pop(right_index)
                points = [cur_point]  # (*) forgot about it
                # (*0) we use the previous two components to merge them into one
                # TODO  but in the future we also eliminate from the comps
                # (*1) we get the points
                points += left_comp.points
                points += right_comp.points
                # (*2) we merge extra merge's (left or right or both Comp's)
                if (left_comp.state[0] == 'merge'):
                    # we use the fathers object to get the poly's points
                    from_lt = [left_comp.state[1]]
                    while types[from_lt[-1]] != 'start':  # (*)
                        from_lt.append(fathers[from_lt[-1]][-1])  # rightmost
                    from_rt = [cur_point]
                    while types[from_rt[-1]] != 'start':  # (*)
                        from_rt.append(fathers[from_rt[-1]][0])  # lefttmost
                    polys.append(
                        from_rt + from_lt[:len(from_lt) - 1][::-1]
                    )
                    print(polys[-1])
                    # update the type of the point:
                    types[left_comp.state[1]] = 'leftturn'
                    # delete the points from the poly, except from the bottom
                    #   two
                    for point in polys[-1][1:len(polys[-1]) - 1]:
                        print(point)
                        points.pop(points.index(point))
                if (right_comp.state[0] == 'merge'):
                    # we use the fathers object to get the poly's points
                    from_lt = [cur_point]
                    while types[from_lt[-1]] != 'start':  # (*)
                        from_lt.append(fathers[from_lt[-1]][-1])  # rightmost
                    from_rt = [right_comp.state[1]]
                    while types[from_rt[-1]] != 'start':  # (*)
                        from_rt.append(fathers[from_rt[-1]][0])  # lefttmost
                    polys.append(
                        from_rt + from_lt[:len(from_lt) - 1][::-1]
                    )
                    print(polys[-1])
                    # update the type of the point:
                    types[left_comp.state[1]] = 'leftturn'
                    # delete the points from the poly, except from the bottom
                    #   two
                    for point in polys[-1][1:len(polys[-1]) - 1]:
                        print(point)
                        points.pop(points.index(point))
                # update minmax_order (*)
                # (*) if merged == True, then do like below. otherwise compare.
                minn, maxx = len(polygon), 0
                for p in points:
                    if x_order[p] < minn:
                        minn = x_order[p]
                    elif x_order[p] > maxx:
                        maxx = x_order[p]
                comps.append(
                    Comp(points, ('merge', cur_point), (minn, maxx))
                    )
            elif types[cur_point] == 'split':  # the last case is a 'middle', so we only check if we can solve
                # we find the component that splits
                #   find its y-lowest point, and use for splitting into 2 Comps
                # we solve it like this -> we check for each component if its
                #   upcoming points will enfence this split :D
                wrap_comp = None
                for comp in comps:
                    if
                #
                if wrap_comp is None:
                    print("SOMETHING UNEXPECTED HAPPENED -",
                          "couldn't find the component to split")
                pass
            elif types[cur_point] == 'end':
                # there must be a Comp to end - so turn into one or two polys
                #   2 if it has a merge state
                pass
                pass
            elif types[cur_point] in ['rightturn', 'leftturn']:
                # find the father (only one)
                father = fathers[cur_point][0]
                print('middle; point and father are:', cur_point, father)
                for comp in comps:
                    if father in comp.points:
                        # the function automatically checks for previous merges
                        if comp.state[0] == 'merge':
                            #
                            pass
                        else:
                            # we add the son the to comp
                            comp.add_point(cur_point)
                        break
        # no matter what, we print the components
        for comp in comps:
            print('Comp {}:'.format(comps.index(comp)))
            dictionary = {point: types[point] for point in comp.points}
            dictionary.update([('minmax', comp.minmax_order), ('state', comp.state)])
            pprint(dictionary)



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


def main():
    polygons = [
        [(-124.0, 181.0), (-62.0, 103.0), (81.0, 181.0), (129.0, 22.0), (-37.0, 33.0), (80.0, -149.0), (-154.0, -166.0), (-203.0, 212.0), (-139.0, 62.0), (-37.0, 56.0), (-177.0, 205.0), (-48.0, 254.0)],
        [(115.0, -59.0), (142.0, 136.0), (9.0, 85.0), (-95.0, 176.0), (-82.0, -152.0), (71.0, 30.0)],
        [(-176.0, 140.0), (-186.0, 98.0), (55.0, 186.0), (14.0, 6.0), (184.0, 81.0), (234.0, -118.0), (-92.0, -116.0), (-31.0, 80.0), (-228.0, -149.0), (-245.0, 197.0)],
        [(-308.0, 66.0), (-247.0, 200.0), (-193.0, 22.0), (-162.0, 80.0), (-189.0, 128.0), (-107.0, 205.0), (-94.0, 86.0), (-120.0, 39.0), (-74.0, -36.0), (-38.0, 52.0), (-56.0, 108.0), (347.0, 212.0), (23.0, 37.0), (39.0, 13.0), (75.0, 44.0), (-96.0, -267.0)],
        [(-289.0, 194.0), (-182.0, 219.0), (24.0, 77.0), (117.0, 220.0), (162.0, 27.0), (307.0, 141.0), (215.0, -245.0), (88.0, 18.0), (-159.0, -208.0), (44.0, -141.0), (70.0, -263.0), (-239.0, -247.0), (-334.0, 153.0), (-259.0, 63.0), (-64.0, 51.0), (-226.0, -18.0), (-230.0, -114.0), (-6.0, 52.0)],
        [(-200, -200), (-200, 200), (200, 200), (200, -200)],
        [(0, 200), (200, 0), (0, -200), (-200, 0)],
        [(0, 200), (200, -200), (0, 0), (-200, -200)]
    ]

    def draw_poly(polygon):
        def screen_dimensions():
            # A simple function to compute the screen's dimensions.
            import ctypes
            user32 = ctypes.windll.user32
            return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        screen_width, screen_height = screen_dimensions()
        window_width, window_height = 0.618 * screen_width, 0.8 * screen_height
        import turtle
        tad = turtle.Turtle()

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
        tad.penup()
        tad.goto(polygon[0])
        tad.pendown()
        for p in polygon + [polygon[0]]:
            tad.goto(p[0], p[1])
        # using the turtle to first draw the 'coordinate axes' :D
        line((-window_width * 0.9 // 2, 0), (window_width * 0.9 // 2, 0), tad, 'lime')
        tad.setheading(90)
        line((0, -window_height * 0.9 // 2), (0, window_height * 0.9 // 2), tad, 'lime')
        tad.color('lime', 'lime')
        tad.goto(0, 0)
        tad.screen.mainloop()

    for poly in polygons[3:4]:
        # draw_poly(poly)
        y_decompose(poly)


if __name__ == '__main__':
    main()
