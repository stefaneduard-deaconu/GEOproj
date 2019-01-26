from graphics import *

def getWin() :
    win = GraphWin("GEOproj", 500, 500)
    win.setBackground("black")
    return win

def getInput(win) :
    pts = []
    pt = win.getMouse()
    #
    while not (pt.getX() < 25 and pt.getY() < 25) :
        pt.setFill(color_rgb(0, 255, 0))
        pts.append(pt)
        cir = Circle(pt, 3)
        cir.setFill("white")
        cir.setOutline(color_rgb(0, 255, 0))
        cir.draw(win)
        pt = win.getMouse()
    return pts

def sign(x) :
    if x < 0 :
        return -1
    elif x == 0 :
        return 0
    return 1
def trig_order(a, b, c) :
    #
    res = a.getX() * b.getY() + b.getX() * c.getY() + c.getX() * a.getY() - c.getX() * b.getY() - b.getX() * a.getY() - a.getX() * c.getY()
    return sign(res)
def get_types(pts) :
    aux = [pts[len(pts) - 1]]
    for p in pts :
        aux.append(p)
    aux.append(pts[0])
    print(aux)
    # 
    types = {}
    for i, j, k in zip(aux, aux[1::], aux[2::]) :
        if sign(j.getY() - i.getY()) != sign(j.getY() - k.getY()) :
            # they are y-monotone
            types.update(dict({j : 0}))
        # elif trig_order(i, j, k) :
        #     pass
        elif trig_order(i, j, k) == -1 : # start or end
            if sign(j.getY() - i.getY()) == -1 : # start or end
                types.update(dict({j : 1})) # start
            else :
                types.update(dict({j : 2})) # end
        else : # split or merge
            if sign(j.getY() - i.getY()) == 1 : # split or merge, i compared to 1 to keep the up->down order/logic
                types.update(dict({j : 3})) # split
            else :
                types.update(dict({j : 4})) # merge
    return types # the order is odd 

def draw_line(p0, p1, win) :
    ln = Line(p0, p1)
    ln.setFill(color_rgb(0, 255, 0))
    ln.draw(win)

# new_list = list(filter(lambda x: (x%2 == 0) , my_list))
# new_list = list(map(lambda x: x * 2 , my_list)) (**)
def main() :
    win = getWin()
    pts = getInput(win)
    print(pts)
    # I can cheat the user and create another window:
    win.close()
    if len(pts) > 2 :
        import pprint
        pp = pprint.PrettyPrinter(indent = 4)
        win = getWin()
        typ = get_types(pts)
        for p in pts :
            print(str(p) + " : " + str(typ[p]))
        # pp.pprint(typ) #
        #
        for i, k in zip(pts, pts[1::]) :
            draw_line(i, k, win)
        draw_line(pts[0], pts[len(pts) - 1], win)
        cir = Circle(pts[0], 4)
        cir.setFill(color_rgb(0, 255, 0))
        cir.draw(win)
        # wait = win.getMouse()
        # win.close()
        ##
        from binarytree import tree, bst, heap # change later
        from binarytree import Node
        
        def sort_key(x) :
            if type(x) == type(Point(0, 0)) :
                return x.getY()
            else :
                raise TypeError("It should have been a point")
        def new_key(x) : # local function
            return pts[x.value].getY()
        #
        # new strategy : we do have trinodes, yet they are separated in starts and splits
        # we could use a different strategy, building using the reverse order, so that we know we don't use anymore
        #   what we already built
        # make a pot; see that you have no merge's

        # finally:
        # we get the trinodes, but we also combine them, so that as soon as a node appears twice
        # we "bind them"

        # if you get to implement a sweep line variant, 
        # you could make it easier by omitting the separation of finding starts, ends, splits, merge's
        # (*) ^
        # def new_key(x) : # local function (**) this is for brute force way
        #     return pts[x.value].getY()
        # pts2 = pts.copy()
        # pts2.sort(key = sort_key)
        # def get_tree(p) :
        #     r = Node(p[0]) # always, thanks to the sorting, a start
        #     free = [r]
        #     for next in p[1::] :
        #         for f in free :
        #             pass
        #     #
        #     return r
        # root = get_tree(pts2)
        # win.getMouse()

        # quit()
        apar = [0] * len(pts)
        
        aux = pts.copy()
        aux.insert(0, pts[len(pts) - 1])
        aux.append(pts[0])
        trinodes = [] # approximatively
        it = iter(aux[1:len(aux) - 1])
        for p in it :
            # print(p)
            i = pts.index(p)
            if (typ[p] == 1 or typ[p] == 4) :
                trinodes.append(Node(
                    i,
                    Node((i - 1 + len(pts)) % len(pts)),
                    Node((i + 1) % len(pts))
                ))
                apar[i] = 1 
                if apar[i - 1] > 0: # simulating a circular list --> already implemented in the language
                    # on the left => you should look for the other to have this son on the right
                    for tri in trinodes :
                        if tri.right and tri.right.value == (i - 1 + len(pts)) % len(pts) :
                            tri.right = trinodes.pop()
                            print(tri)
                        break
                else :
                    apar[i - 1] = 1 # samed :)
                if apar[(i + 1) % len(pts)] > 0:
                    for tri in trinodes :
                        if tri.left and tri.left.value == (i - 1 + len(pts)) % len(pts) :
                            tri.left = trinodes.pop()
                            print(tri)
                        break
                else :
                    apar[(i + 1) % len(pts)] = 1
                next(it, 0)
            # now, if it is not with prev and next as the sons, we verify not to be the son of some other (prev or next) vortex
            else:
                if apar[i] == 0 : # we have
                    trinodes.append(Node(i))
                    apar[i] = 0
            print(trinodes[-1])
        pp.pprint(trinodes)
        pp.pprint(typ)
        # for n in trinodes :
        #     print(n)
        win.getMouse()
        # alrighty, when I got here i have the trinodes and I also have all other nodes
        # ! I don't eliminate the node that is part of a next trinode
        # remember how you could use the previous to last course to find the triangle you're interested in :)
        # ENDGAME - i keep a list of where every "element" ends, an ending list
        nxt = []
        prv = []
        prv.append(pts[-1])
        for p in pts[0::] :
            prv.append(p)
        prv.pop()
        for p in pts[1::] :
            nxt.append(p)
        nxt.append(pts[0])
        nt = {}
        pv = {}
        for i in range(0, len(pts)) :
            nt.update(dict({pts[i] : nxt[i]}))
            pv.update(dict({pts[i] : prv[i]}))
        # print(nt)
        # print(pv)

        # quit()
        
        
        # trinodes.sort(key = new_key)
        pts2 = pts.copy()
        pts2.sort(key = sort_key)
        # pp.pprint(trinodes)
        pp.pprint(pts2)
        # win.getMouse()
        pol = [] # auxiliary thingies
        ypol = []
        end = [0] # to get the thingies' ends
        for p in pts2 :
            if typ[p] == 4 :
                pol.append([p])
            elif typ[p] == 3 :
                for i in range(1, len(end)) : # yet we only remove a sublist
                    for j in range(end[i - 1], end[i]) :
                        if (pol[j] == pv[p] or pol[j] == nt[p]) :
                            y = []
                            for x in range(end[i - 1], end[i]) :
                                y.append(pol[x])
                            for x in range(end[i - 1], end[i]) :
                                pol.remove(pol[x])
                            ypol.append(y)
                            break
            # elif typ[p] == 0 : # continue
            #     ind = pol.index(nv[p])
            #     if ind
            elif typ[p] == 2 or typ[p] == 0 : # split , even if the cases could be treated differently, to optimise the program
                # pvind = pol.index(pv[p])
                # ntind = pol.index(nt[p])
                # if pvind  
                index = -1
                for i in range(0, len(pol)) :
                    if nt[pol[i]] == p or pv[pol[i]] == p :
                        if p.getX() < pol[i].getX() :
                            pol.insert(i, p)
                            index = i
                        else :
                            pol.insert(i + 1, p)
                            index = i + 1
                        break
                if typ[p] == 2 : # we unite the ends -- this is the IMP/critical part
                    end.remove(index + 1) # because end retains where is the first element of a figure
                    
            elif typ[p] ==  1 : # merge, the things that split the figures we work with while line sweeping
                # we unite this one with all the previous 2's from the piece (cause we can't have more) with a previous merge (typ == 1)
                # and we split the ends
                ind = []
                for i in pol :
                    if type[pol[i]] == 2 :
                        ind.append(i)
                # so we interchange a figure with this element, and we add the figure to the ypol list
                # but we keep he leftmost and rightmost resulting figures !!!
                # a split should always be the left or right of a figure to be!!!!
                aux = []
                aux = pol[pol.index()::pol.index()]
                
                # and then we remove the "end" of the figure

                print(None)
        quit()


        # index = 0
        # lengt = len(pts)
        # trinodes = []
        # if typ[pts[0]] == 1 or typ[pts[0]] == 4 :
        #     trinodes.append(
        #         Node(
        #             0,
        #             Node(
        #                 1
        #             ),
        #             Node(
        #                 1
        #             )
        #         )
        #     )
        #     index = index + 2
        #     lengt = lengt - 1
        # elif typ[pts[lengt - 1]] == 1 or typ[pts[lengt - 1]] == 4 :
        #     trinodes.append(
        #         Node(
        #             lengt - 1,
        #             Node(
        #                 lengt - 2
        #             ),
        #             Node(
        #                 0
        #             )
        #         )
        #     )
        #     index = index + 1
        #     lengt = lengt - 2
        # while index < lengt - 1 :
        #     if typ[aux[index]] == 1 or typ[aux[index]] == 4 :
        #         lt = Node(index - 1)
        #         rt = Node(index + 1)
        #         ft = Node(index, lt, rt)
        #         index = index + 2
        #     else :
        #         index = index + 1
        # pp.pprint(trinodes)
        win.getMouse()
        quit()
        #
        
        pp.pprint(pts)
        pts.sort(key = sort_key, reverse = False)
        pp.pprint(pts)
        def left(x, y) : # x is to the left of y ??
            if sign(y.getX() - x.getX()) > 0 :
                return True
            return False
        

        # for p, t in pts[1::], typ[1::] :
        #     new_node = Node(p, t)
        #     for node in root.preorder() :
        #         if(node.value[1]) :
        #             pass

                


main() # now you only have to solve the trig order
