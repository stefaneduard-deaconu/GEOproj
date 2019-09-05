"""
Here we have two utility functions, for y-decomposition (decomposing a
  polygon in y-monotone polygons), and the triangulation of a y-monotone
  polygon.
Plus the main() function, used throughout the project for testing:D
"""

from pprint import pprint

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

    y_ordered_points = sorted(polygon, key=lambda A: -A[1])
    x_order = {
        point: index for index, point in enumerate(sorted(polygon, key=lambda A: A[0]))
    }

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

        def get_margins(self):
            # remember there must be at least one point
            if len(self.points) > 1:  # if there are multiple points, then
                return (self.points[-1], self.points[0])
            else:
                polygon_index = polygon.index(self.points[0])
                return (
                    polygon[(polygon_index + 1) % len(polygon)],
                    polygon[polygon_index - 1]
                    )

        def add_point(self, point, position):
            # we add the point so that self.points keeps the trig. order
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
                # print(points)
                left_points_index = len(right_comp.points) + 1
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
                    margin_left = comp.points[-1]
                    margin_right = comp.points[0]  # because it must be upper
                    #
                    # print(y_level, y_ordered_points.index(true_margin_left), y_ordered_points.index(true_margin_right), y_ordered_points.index(margin_left), y_ordered_points.index(margin_right))
                    first_turn = trig_order(true_margin_right, margin_right, cur_point)
                    second_turn = trig_order(margin_left, true_margin_left, cur_point)
                    # print(first_turn, second_turn)
                    # if true_margin_left[0] <= cur_point[0] and cur_point[0] <= true_margin_right[0]:  # insufficient to test if the 'split' is inside the comp :((
                    if first_turn == second_turn:
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
            dictionary = {'points': [(y_ordered_points.index(point), types[point]) for point in comp.points]}
            dictionary.update([
                ('margin', [y_ordered_points.index(point) for point in comp.get_margins()]),
                ('state', comp.state)
                ])
            pprint(dictionary)
        pprint([[y_ordered_points.index(point) for point in poly] for poly in  polys])
    return edges, polys


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
            self.points = sorted(y_polygon_trig, key=lambda point: -point[1])
            top_index, top = max(enumerate(y_polygon_trig), key=lambda point: point[1][1])
            bot_index, bot = min(enumerate(y_polygon_trig), key=lambda point: point[1][1])
            self.queue = self.points[0:2]
            self.points = self.points[2:]
            # print('\n\n', self.queue, self.points)
            self.types = {top: 'top', bot: 'bot'}
            # auxiliary, the len of the points
            p_len = len(y_polygon_trig)
            # getting the left part
            index = (top_index + 1) % p_len
            point = y_polygon_trig[index]
            while(point != bot):
                self.types[point] = 'left'
                index = (index + 1) % p_len
                point = y_polygon_trig[index]
            # getting the right part
            index = (bot_index + 1) % p_len
            point = y_polygon_trig[index]
            while(point != top):
                self.types[point] = 'right'
                index = (index + 1) % p_len
                point = y_polygon_trig[index]

        def get_triangles(self):
            triangles = []  # a work in progress, the class's 'main feature'
            # we for now settle for the lines we add for triangulating :D
            # return triangles
            lines = []
            while self.queue:  # while it's not empty,
                print(self.queue, self.points)
                if self.points:
                    next_point = self.points.pop(0)
                    # two cases, they have the same type, or they don't
                    # if they do are on the same side:
                    if self.types[next_point] == self.types[self.queue[-1]]:
                        print('SAME SIDE')
                        # ..then we check the trig order and eliminate
                        #   triangles, if any three consecutive points are
                        #   'leftturn's
                        # IMP ----> if the queue has only one item, we just add
                        #   the next_point
                        if len(self.queue) == 1:  # the easy case :D
                            self.queue.append(next_point)
                        else:
                            # we eliminate all leftturns, if there are any
                            trig = (trig_order(
                                next_point,
                                self.queue[-1], self.queue[-2]
                            ) == 'leftturn')
                            # we repeat elimination
                            c_1 = self.types[next_point] == 'right' and trig
                            c_2 = self.types[next_point] == 'left' and not trig
                            while c_1 or c_2:
                                # we extract a triangle
                                triangles.append((
                                    next_point,
                                    self.queue[-1], self.queue[-2]
                                ))
                                lines.append((next_point, self.queue[-2]))
                                # for testing:
                                # line(lines[-1][0], lines[-1][1], tad=tad, color='red')
                                self.queue.pop()
                                # important for indeces
                                if len(self.queue) == 1:
                                    break
                                trig = (trig_order(
                                    next_point,
                                    self.queue[-1], self.queue[-2]
                                ) == 'leftturn')
                                c_1 = self.types[next_point] == 'right' and trig
                                c_2 = self.types[next_point] == 'left' and not trig
                            # in every case, we add the next_point to the queue
                            self.queue.append(next_point)
                    else:
                        # if they are not on the same side, we make triangles
                        # or we just finished, and the types is 'bot'
                        print('DIFFERENT SIDE OR BOT')
                        # we add len(self.queue) - 1 triangles, and
                        #   len(self.queue) - 2 lines, if top
                        for index in range(1, len((self.queue))):
                            point_0 = self.queue[index - 1]
                            point_1 = self.queue[index]
                            lines.append((next_point, point_1))
                            # for testing:
                            # (*)
                            # if self.types[next_point] != 'bot' or index < len((self.queue)) - 1:
                            #     line(lines[-1][0], lines[-1][1], tad=tad, color='red')
                            triangles.append((next_point, point_0, point_1))
                        triangles.append((
                            next_point,
                            self.queue[-1], self.queue[-2]
                        ))
                        # if we got to the last point, don't add it. FINISH !!!
                        if self.types[next_point] != 'bot':
                            self.queue = [
                                self.queue[-1], next_point
                            ]
                        else:
                            self.queue.clear()
                            lines.pop()  # it was already drawn :D

                else:  # there aren't any points, so just check the queue
                    raise ValueError('there are remaining points in the queue')
            return (lines, triangles)

    # we presume the polygons' points are in trig order

    return TriangleQueue(y_polygon).get_triangles()


# for testing:

def sign(num):
    if num < 0:
        return -1
    elif num > 0:
        return 1
    else:
        return 0


def main():
    pass


if __name__ == '__main__':
    main()
