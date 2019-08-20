"""
Here we have two utility functions, for y-decomposition (decomposing a
  polygon in y-monotone polygons), and the triangulation of a y-monotone
  polygon.
Plus the main() function, used throughout the project for testing:D
"""
import ctypes
from pprint import pprint
import turtle
polygons = [
    [(-124.0, 181.0), (-62.0, 103.0), (81.0, 181.0), (129.0, 22.0), (-37.0, 33.0), (80.0, -149.0), (-154.0, -166.0), (-203.0, 212.0), (-139.0, 62.0), (-37.0, 56.0), (-177.0, 205.0), (-48.0, 254.0)],
    [(115.0, -59.0), (142.0, 136.0), (9.0, 85.0), (-95.0, 176.0), (-82.0, -152.0), (71.0, 30.0)],
    [(-176.0, 140.0), (-186.0, 98.0), (55.0, 186.0), (14.0, 6.0), (184.0, 81.0), (234.0, -118.0), (-92.0, -116.0), (-31.0, 80.0), (-228.0, -149.0), (-245.0, 197.0)],
    [(-308.0, 66.0), (-247.0, 200.0), (-193.0, 22.0), (-162.0, 80.0), (-189.0, 128.0), (-107.0, 205.0), (-94.0, 86.0), (-120.0, 39.0), (-74.0, -36.0), (-38.0, 52.0), (-56.0, 108.0), (347.0, 212.0), (23.0, 37.0), (39.0, 13.0), (75.0, 44.0), (-96.0, -267.0)],
    [(-289.0, 194.0), (-182.0, 219.0), (24.0, 77.0), (117.0, 220.0), (162.0, 27.0), (307.0, 141.0), (215.0, -245.0), (88.0, 18.0), (-159.0, -208.0), (44.0, -141.0), (70.0, -263.0), (-239.0, -247.0), (-334.0, 153.0), (-259.0, 63.0), (-64.0, 51.0), (-226.0, -18.0), (-230.0, -114.0), (-6.0, 52.0)],
    [(0, 200), (200, 0), (0, -200), (-200, 0)],
    [(0, 200), (200, -200), (0, 0), (-200, -200)],
    [(-239.0, 68.0), (-123.0, 247.0), (-96.0, 98.0), (-157.0, 92.0), (152.0, 15.0), (163.0, 249.0), (-6.0, 155.0), (124.0, 288.0), (370.0, 204.0), (251.0, -69.0), (254.0, 129.0), (70.0, -168.0), (-269.0, -91.0), (-10.0, 1.0), (-303.0, -10.0), (-320.0, 200.0)],
    [(19.0, 247.0), (-112.0, 113.0), (-162.0, 223.0), (-231.0, -35.0), (-307.0, 76.0), (-242.0, -207.0), (-14.0, -17.0), (-73.0, 51.0)],
    [(-197.0, 144.0), (-62.0, 239.0), (-58.0, 71.0), (-125.0, 134.0), (-95.0, -49.0), (190.0, 216.0), (34.0, 225.0), (24.0, 126.0), (-7.0, 250.0), (290.0, 265.0), (242.0, 199.0), (412.0, 242.0), (224.0, 79.0), (328.0, 80.0), (203.0, -60.0), (173.0, 93.0), (221.0, 139.0), (42.0, 33.0), (147.0, 13.0), (-25.0, -47.0), (-112.0, -108.0), (-171.0, 66.0), (-280.0, 41.0), (-343.0, -60.0), (-248.0, -141.0), (-215.0, -43.0), (-283.0, -17.0), (-216.0, 3.0), (-175.0, -77.0), (-205.0, -139.0), (-127.0, -136.0), (-242.0, -179.0), (-135.0, -236.0), (38.0, -103.0), (148.0, -214.0), (-58.0, -233.0), (-17.0, -189.0), (-164.0, -268.0), (-318.0, -161.0), (-360.0, -244.0), (-362.0, 135.0), (-295.0, 107.0), (-270.0, 253.0), (-241.0, 198.0), (-123.0, 237.0), (-251.0, 167.0), (-211.0, 79.0), (-160.0, 145.0)],
    [(56.0, 113.0), (111.0, 167.0), (131.0, 41.0), (180.0, 70.0), (241.0, -45.0), (75.0, -47.0), (91.0, 38.0), (-71.0, -195.0), (133.0, -147.0), (-122.0, -272.0), (-255.0, -128.0), (-40.0, -50.0), (-97.0, -113.0), (30.0, -9.0), (-234.0, 74.0), (-120.0, 223.0), (-96.0, 123.0), (68.0, 240.0), (85.0, 196.0), (-23.0, 109.0), (92.0, 113.0)],
    [(16.0, 71.0), (133.0, 159.0), (106.0, 43.0), (262.0, -84.0), (-131.0, -128.0), (33.0, 20.0), (-164.0, 34.0), (-34.0, 224.0), (-18.0, 157.0), (37.0, 213.0)],
[(16.0, 71.0), (133.0, 159.0), (106.0, 43.0), (262.0, -84.0), (-131.0, -128.0), (33.0, 20.0), (-164.0, 34.0), (-34.0, 224.0), (-18.0, 157.0), (37.0, 213.0)]
]
which_one = 9
tad = turtle.Turtle()
tad.speed(6)
tad.ht()
# using the turtle to first draw the 'coordinate axes' :D


def screen_dimensions():
    # A simple function to compute the screen's dimensions.
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


screen_width, screen_height = screen_dimensions()
window_width, window_height = 0.618 * screen_width, 0.8 * screen_height
print(844, 614)
# window = turtle.Screen
turtle.setup(window_width, window_height)
print(turtle.screensize())

# turtle.Screen.setup(width=screen_width, height=screen_height)

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


line((-window_width * 0.9 // 2, 0), (window_width * 0.9 // 2, 0), tad, 'lime')
tad.setheading(90)
line((0, -window_height * 0.9 // 2), (0, window_height * 0.9 // 2), tad, 'lime')


def draw_poly(polygon, tad, color='lime'):
    tad.penup()
    tad.goto(polygon[0])
    tads_color = tad.color()
    tad.color(color, color)
    tad.pendown()
    for p in polygon + [polygon[0]]:
        tad.goto(p[0], p[1])
    tad.color(tads_color[0], tads_color[1])
    tad.penup()
    tad.goto(0, 0)


draw_poly(polygons[which_one], tad, color='black')
tad.pensize(2)
tad.speed(3)

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
        if sign(res) == 1:
            return 'leftturn'
        elif sign(res) == -1:
            return 'rightturn'
        else:
            raise ValueError('You have three consecutive points that form a line!!!')
            # we could solve this issue here, by just eliminating the middle one :D

    def trig_order_poly(polygon):
        # function to test if the polygon's point order is in trig order
        index = polygon.index((max(polygon, key=lambda A: A[1])))
        A, B = polygon[index - 1], polygon[index]
        C = polygon[(index + 1) % len(polygon)]
        print(A, B, C, trig_order(A, B, C))
        if trig_order(A, B, C) == 'leftturn':
            return True
        else:
            return False

    # print(trig_order((0, 0), (0, 1), (1, -1)))
    if not trig_order_poly(polygon):
        polygon = polygon[-1::-1]

    def get_types(pts):
        aux = [pts[-1]] + [p for p in pts] + [pts[0]]
        types = {}
        for A, B, C in zip(aux, aux[1::], aux[2::]):
            if sign(B[1] - A[1]) != sign(B[1] - C[1]):
                types.update(dict({B: trig_order(A, B, C)}))
            elif trig_order(A, B, C) == 'leftturn':  # start or end
                if sign(B[1] - A[1]) == 1:  # start or end
                    types.update(dict({B: 'start'}))  # start
                else:
                    types.update(dict({B: 'end'}))  # end
            else:  # split or merge ----> 'leftturn', otherwise trig_order raises ValueError
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

    types = get_types(polygon)
    fathers = get_fathers(polygon)  # we don't check the trig. order here :D
    # print({point: types[point] for point in polygon})

    y_ordered_points = sorted(polygon, key=lambda A: -A[1])
    x_order = {
        point: index for index, point in enumerate(sorted(polygon, key=lambda A: A[0]))
    }
    # pprint(y_ordered_points)

    class Comp(object):
        def __init__(self, given_points, given_state=(None, None)):
            if isinstance(given_points, list):
                # we created a new component from a set of points
                self.points = given_points
                self.state = given_state  # given state has state and point
            else:  # isinstance(given_points, tuple):  # first time, just a 'start' !!!!!!!
                # we created a new component from a set of points
                self.points = [given_points]
                self.state = given_state  # given state has state and point
            # else:
            #     print('NOT A LIST - problem with a Comp initialization')

        def get_margins(self):
            # remember there must be at least one point
            if len(self.points) > 1:  # if there are multiple points, then
                return (self.points[-1], self.points[0])
            else:
                # polygon_index = None
                # if types[self.points[0]] == 'start':  # we get the start
                #     polygon_index = polygon.index(self.points[0])
                # else:
                #     polygon_index = polygon.index(self.points[1])
                polygon_index = polygon.index(self.points[0])
                return (
                    polygon[(polygon_index + 1) % len(polygon)],
                    polygon[polygon_index - 1]
                    )

        def add_point(self, point, position):
            # we add the point so that self.points keep the trig. order
            if position == 0:
                self.points = [point] + self.points
            elif position == -1:
                self.points.append(point)
            else:
                print("VALUE ERROR - the side should be 0 or -1")
    comps = []
    polys = []  # we can get the polys with a function inside Comp :D
    edges = []  # edges are the lines we add while decomposing
    for cur_index, (x, y) in enumerate(y_ordered_points):
        cur_point = (x, y)

        print('-' * 50)
        print(cur_point, '\'{}\', x_order={}'.format(types[cur_point], x_order[cur_point]), '----> point {}'.format(cur_index))
        # if cur_index == 25:
        #     tad.screen.mainloop()

        if types[cur_point] == 'start':
            comps.append(
                Comp(cur_point)
                )
        else:
            if types[cur_point] == 'merge':
                left_index, right_index = None, None
                # the fathers are taken as to keep trig order:
                this_index = polygon.index(cur_point)
                left_father = polygon[(this_index + 1) % len(polygon)]
                right_father = polygon[this_index - 1]
                print('MERGE:')
                print(polygon)
                print('Fathers ----> {} {}'.format(left_father, right_father))
                # line(cur_point, left_father, tad, 'green')
                # line(cur_point, right_father, tad, 'green')
                for comp_index, comp in enumerate(comps):
                    if left_father in [comp.points[0], comp.points[-1]]:  # beginning of poly
                        left_index = comp_index
                    # could be an elif, if desired:
                    elif right_father in [comp.points[0], comp.points[-1]]:  # ending of poly
                        right_index = comp_index
                # # testing:
                # print('FATHERS are as it comes:', fathers[cur_point])
                # print('POINTS are as it comes:', comps[left_index].points, comps[right_index].points)
                # we always have two corresponding components when not 'starting' a
                #   new merge
                print('Components to merge indexes --->', left_index, right_index)
                if left_index < right_index:
                    right_comp = comps.pop(right_index)
                    left_comp = comps.pop(left_index)
                else:
                    left_comp = comps.pop(left_index)
                    right_comp = comps.pop(right_index)

                # (*0) we get the points for both the Comps:
                print(right_comp.points)
                print(left_comp.points)
                print([cur_point])
                points = right_comp.points + [cur_point] + left_comp.points
                print(points)
                left_points_index = len(right_comp.points) + 1
                # print(points)
                # (*!)The order of the next two it's is essential when both Comp's
                #   are in the 'merge' state
                # (*1) we merge extra 'merge's (left or right or both Comp's)
                print('LEFT')
                if (left_comp.state[0] == 'merge'):
                    # find the position of this Comp's merge
                    left_merge_point = left_comp.state[1]
                    left_merge_index = points.index(left_merge_point)
                    # get the polygon
                    polys.append(
                        points[left_points_index - 1:left_merge_index + 1]
                        )
                    # update the type of the cur_point:
                    types[left_comp.state[1]] = 'leftturn'  # (*is it right?)
                    # delete the points from the poly's middle part
                    # print('POLYGON ----> ', polys[-1])
                    edges.extend([(points[left_points_index - 1], points[left_merge_index])])
                    line(edges[-1][0], edges[-1][1], tad, 'red')
                    for i in range(left_points_index, left_merge_index):
                        points.pop(left_points_index)
                print('RIGHT')
                if (right_comp.state[0] == 'merge'):
                    # find the position of this Comp's merge
                    right_merge_point = right_comp.state[1]
                    right_merge_index = points.index(right_merge_point)
                    # get the polygon
                    polys.append(
                        points[right_merge_index:left_points_index]
                        )
                    # update the type of the cur_point:
                    types[right_comp.state[1]] = 'rightturn'  # (*is it right?)
                    # delete the points from the poly's middle part
                    # print('POLYGON ----> ', polys[-1])
                    edges.extend([(points[right_merge_index], points[left_points_index - 1])])
                    line(edges[-1][0], edges[-1][1], tad, 'red')
                    for i in range(right_merge_index + 1, left_points_index - 1):
                        points.pop(right_merge_index + 1)
                comps.append(
                    Comp(points, ('merge', cur_point))
                    )
            elif types[cur_point] == 'split':  # the last case is a 'middle', so we only check if we can solve
                # we find the component that splits.
                # there are two cases. Either a component with multiple points
                #   or a component with one point that has the upcoming margins
                #   (from get_margins) so as to enclose the 'split'
                # just a test
                # (*) if 0, then there must be
                # We find the enclosing component:
                for comp in comps:
                    margin_left, margin_right = comp.get_margins()
                    # the true margins are the first points below cur_point
                    y_level = cur_point[1]
                    #   we find the margin to the left that does so
                    index_left = polygon.index(margin_left)
                    while polygon[index_left][1] > y_level:
                        index_left = (index_left + 1) % len(polygon)
                    #   we find the margin to the right that does so
                    index_right = polygon.index(margin_right)
                    while polygon[index_right][1] > y_level:
                        index_right -= 1  # it may get negative,
                        # but Python handles it for us
                    # getting the true margins:
                    true_margin_left = polygon[index_left]
                    true_margin_right = polygon[index_right]
                    if true_margin_left[0] <= cur_point[0] and cur_point[0] <= true_margin_right[0]:
                        print("SPLIT ----> comp number {}".format(comps.index(comp)))
                        # we check if the Comp has multiple points
                        # (*if there's a merge, it's also the lowest point :D)
                        # (*we don't use fathers anymore as a binary tree,
                        #   so we don't to update the 'types' for cur_point, as
                        #   it will only be used for the future points)
                        if len(comp.points) > 1:  # can be a merge
                            if comp.state[0] == 'merge':
                                # we split using the merge
                                merge_point = comp.state[1]
                                merge_index = comp.points.index(merge_point)
                                #   we create and add a new comp:
                                new_comp_points = comp.points[:merge_index + 1]
                                # we add the edge:
                                edges.extend([(new_comp_points[-1], cur_point)])
                                line(edges[-1][0], edges[-1][1], tad, 'red')
                                #
                                new_comp_points.extend([cur_point])
                                comps.append(
                                    Comp(new_comp_points)
                                    )
                                #   we modify the old comp's points
                                comp.points = [cur_point] + comp.points[merge_index:]
                                # at the end, we eliminate the state
                                comp.state = (None, None)
                                break
                            # otherwise:
                            # we use the rightmost point to split the Comp
                            # doesn't solve the 'merge'. We treat is separately
                            other_point = comp.points[0]  # "right"most point
                            # now we split into two comps
                            #   we create the poly for the new one
                            new_comp_points = [other_point, cur_point]
                            # we add the extra edge:
                            edges.extend([tuple(new_comp_points)])
                            line(edges[-1][0], edges[-1][1], tad, 'red')
                            comps.append(
                                Comp(new_comp_points)
                                )
                            #   and we 'extend' the old one
                            comp.points = [cur_point] + comp.points  # a new []

                        else:
                            # there is only a start we turn into 'two' starts:D
                            #   we create the new comp:
                            # we add the extra edge:
                            edges.extend([(comp.points[0], cur_point)])
                            line(edges[-1][0], edges[-1][1], tad, 'red')
                            # and then we finish the comp
                            new_comp_points = comp.points + [cur_point]
                            comps.append(
                                Comp(new_comp_points)
                                )
                            #   we modify the old comp:
                            comp.points = [cur_point] + comp.points
                        break
            elif types[cur_point] == 'end':
                # in this case,
                #   if 'merging' we just turn the 'end' into two ends => 2 poly
                #   otherwise we just get a poly (comp.points)
                # First we find the corresponding component (there must be!)
                #   but it gets tricky. its order must respect not the one of the polygon (because there can be a 'leap' somewhere, cause by a split or such stuff)
                #    We solve this by finding not the pair to fit the end,
                #       but a component with a margin as to fit the order
                for index, comp in enumerate(comps):
                    # print(comp.points)
                    print('END')
                    # we first find the comp:
                    # we check if the upcoming point for the comp, in the polygon's order,
                    #   is actually our 'end'
                    upcoming_point_index = polygon.index(comp.points[-1]) + 1
                    upcoming_point_index %= len(polygon)
                    upcoming_point = polygon[upcoming_point_index]
                    if upcoming_point == cur_point:
                        if comp.state[0] == 'merge':
                            # if there's a 'merge' state, we create two polys:
                            merge_point = comp.state[1]
                            merge_index = comp.points.index(merge_point)
                            polys.append(
                                comp.points[merge_index:] + [cur_point]
                                )
                            polys.append(
                                comp.points[:merge_index + 1] + [cur_point]
                                )
                            # we add the edge:
                            edges.extend([(comp.points[merge_index], cur_point)])
                            line(edges[-1][0], edges[-1][1], tad, 'red')
                        else:
                            # if there's no state, we just add the cur_point
                            #   to the comp's points to get the final polygon
                            polys.append(
                                comp.points + [cur_point]
                                )

                        # at the end, we remove (pop) the Comp
                        comps.pop(index)
                        break
            elif types[cur_point] in ['rightturn', 'leftturn']:
                # find the father (only one)
                polygon_index = polygon.index(cur_point)
                father = fathers[cur_point][0]
                downwards = None
                if father == polygon[polygon_index - 1]:
                    downwards = True
                elif father == polygon[(polygon_index + 1) % len(polygon)]:
                    downwards = False
                print('middle, father ----> {}, {}'.format(cur_point, father))
                print(downwards)
                for comp in comps:
                    case_1 = comp.points[0] == father and not downwards
                    case_2 = comp.points[-1] == father and downwards
                    if case_1 or case_2:
                        # the function automatically checks for previous merges
                        if comp.state[0] == 'merge':
                            print('merge from a middle')
                            merge_point = comp.state[1]
                            merge_index = comp.points.index(merge_point)
                            # we see which ear do we clip :D (ear-clipping)
                            if downwards:  # same sense as the polygon
                                print('left')
                                polys.append(
                                    comp.points[merge_index:] + [cur_point]
                                    )
                                comp.points = comp.points[:merge_index + 1]
                                comp.points.extend([cur_point])
                            else:
                                print('right')
                                polys.append(
                                    comp.points[:merge_index + 1] + [cur_point]  # end-effect says the end can be at the end or at the beginning of its poly
                                    )
                                comp.points = [cur_point] + comp.points[merge_index:]
                            # we unset the state:
                            comp.state = (None, None)
                            # and we add the edge:
                            edges.extend([(cur_point, merge_point)])
                            line(edges[-1][0], edges[-1][1], tad, 'red')
                        else:
                            # we add the son the to comp
                            if father == comp.points[0]:  # be careful
                                # if there's only one point in the Comp,
                                #   we get position from the point's x coord
                                if len(comp.points) == 1:
                                    if cur_point[0] > father[0]:  # to the rt
                                        comp.add_point(cur_point, 0)
                                    else:  # >=2, clearly to the left
                                        comp.add_point(cur_point, -1)
                                else:
                                    comp.add_point(cur_point, 0)  # to the rt
                            else:
                                comp.add_point(cur_point, -1)  # to the lt
                        break
        # no matter what, we print the components ----> for testing
        print("COMPS:")
        for comp in comps:
            print('Comp {}:'.format(comps.index(comp)))
            dictionary = {'points': [(point, types[point]) for point in comp.points]}
            dictionary.update([
                ('margin', comp.get_margins()),
                ('state', comp.state)
                ])
            pprint(dictionary)
        pprint(polys)
        # line(edges[-1][0], edges[-1][1], tad, 'red')
    return polys


def triangulate(y_polygon):

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
        elif sign(res) == -1:
            return 'rightturn'
        else:
            raise ValueError('You have three consecutive points that form a line!!!')
            # we could solve this issue here, by just eliminating the middle one :D

    class TriangleQueue(object):

        def __init__(self, y_polygon_trig):
            points = sorted(y_polygon_trig, key=lambda point: -point[1])[1:]
            top_index, top = max(enumerate(y_polygon_trig), key=lambda point: point[1][1])
            bot_index, bot = min(enumerate(y_polygon_trig), key=lambda point: point[1][1])
            queue = points[0:2]
            types = {top: 'top'}
            # auxiliary, the len of the points
            p_len = len(y_polygon_trig)
            # getting the left part
            index = (top_index + 1) % p_len
            point = y_polygon_trig[index]
            while(point != bot):
                index = (index + 1) % p_len
                point = y_polygon_trig[index]
            # getting the right part
            index = (bot_index + 1) % p_len
            point = y_polygon_trig[index]
            while(point != bot):
                index = (index + 1) % p_len
                point = y_polygon_trig[index]
            # first turn:
            last_turn = 'top'

        # member functions that act as auxiliaries, for better code

        def get_next_point(self):
            # we set the next one into the queue, and we return it
            pass
        # the function we call after instantiating an object -> returns the
        #   triangles

        def get_triangles(self):
            triangles = []
            return triangles





# for testing:


def sign(num):
    if num < 0:
        return -1
    elif num > 0:
        return 1
    else:
        return 0


def main():
    for polygon in polygons[which_one:which_one + 1]:
        polys = y_decompose(polygon)
        print()
        print('*' * len('* In the end we\'ve got: *'))
        print('* In the end we\'ve got: *')
        print('*' * len('* In the end we\'ve got: *'))
        print()
        pprint(polys)
        # drawing them:
        # draw the y-monotone polys:
        # draw_poly(polygon, tad, color='red')
        tad.pensize(2)
        tad.speed(5)
        for poly in polys:
            draw_poly(poly, tad, color='blue')
        tad.screen.mainloop()


if __name__ == '__main__':
    main()
