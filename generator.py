#! /usr/bin/python3

from random import random, randrange
from PIL import Image, ImageDraw

class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @x.setter
    def y(self, value):
        self._y = value


class Rectangle:
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @x.setter
    def y(self, value):
        self._y = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def square(self):
        return self._height * self._width

    def __str__(self):
        return "x=" + str(self._x) + " y=" + str(self._y) + " width=" + str(self._width) + " height=" + str(self._height)

    def get_xy(self):
    	return [self._x, self._y, self._x + self._width, self._y + self._height]    


class Leaf(Rectangle):
    MIN_LEAF_SIDE = 10
    MIN_ROOM_SIDE = 5
    def __init__(self, x, y, width, heigh):
        super(Leaf, self).__init__(x, y, width, heigh)
        self.leftChild = None
        self.rightChild = None
        self.room = None
        self.halls = []
    
    def split(self):
        if self.leftChild != None or self.rightChild != None:
            # print(1)
            return False
        splitH = self._height > self._width #random() > 5.0
        maxSide = self._height if splitH else self._width
        if maxSide <= Leaf.MIN_LEAF_SIDE * 2:
            # print(2)
            return False

        split = randrange(Leaf.MIN_LEAF_SIDE, maxSide - Leaf.MIN_LEAF_SIDE, 1)
        if splitH:
            self.leftChild = Leaf(self._x, self._y, self._width, split)
            self.rightChild = Leaf(self._x, self._y + split, self._width, self._height - split)
        else:
            self.leftChild = Leaf(self._x, self._y, split, self._height)
            self.rightChild = Leaf(self._x + split, self._y, self._width - split, self._height)

        return True

    def create_room(self):
        room_x = self._x + randrange(1, self._width - Leaf.MIN_ROOM_SIDE, 1)
        room_y = self._y + randrange(1, self._height - Leaf.MIN_ROOM_SIDE, 1)
        room_w = randrange(Leaf.MIN_ROOM_SIDE, self._width - Leaf.MIN_ROOM_SIDE + 1, 1)
        room_h = randrange(Leaf.MIN_ROOM_SIDE, self._height - Leaf.MIN_ROOM_SIDE + 1, 1)
        self.room = Rectangle(room_x, room_y, room_w, room_h)

    def get_room(self):
    	return self.room.get_xy()

class Tree:
    def __init__(self, x, y, width, height):
        self._root = Leaf(x, y, width, height)
        self.rooms = None

    @staticmethod
    def print_tree(leaf):
        print(leaf)
        if leaf.leftChild:
            Tree.print_tree(leaf.leftChild)
        if leaf.rightChild:
            Tree.print_tree(leaf.rightChild)

    @staticmethod
    def split_space(leaf):
        if leaf.leftChild == None and leaf.rightChild == None:
            leaf.split()
            if leaf.leftChild:
                Tree.split_space(leaf.leftChild)
            if leaf.rightChild:
                Tree.split_space(leaf.rightChild)

    # def create_rooms(self):
    #     current_leaf = self._root
    #     reviewed_leafs = set()
    #     last_leafs = []

    #     while current_leaf != None:
    #         if current_leaf not in reviewed_leafs \
    #                 and current_leaf.room == None \
    #                 and current_leaf.leftChild == None \
    #                 and current_leaf.rightChild == None:
    #             current_leaf.create_room()
    #             print(current_leaf.room)
    #         if current_leaf.leftChild and current_leaf.leftChild not in reviewed_leafs:
    #             last_leafs.append(current_leaf)
    #             current_leaf = current_leaf.leftChild
    #         elif current_leaf.rightChild and current_leaf.rightChild not in reviewed_leafs:
    #             last_leafs.append(current_leaf)
    #             current_leaf = current_leaf.rightChild
    #         else:
    #             current_leaf = last_leafs.pop() if len(last_leafs) else None

    # def get_rooms(self):
    #     def func(leaf):
    #         if leaf.room:
    #             print(leaf.room)
    #     self.map(func)

    def create_rooms(self):
    	Tree.leaf_map(self._root, Leaf.create_room)

    @staticmethod
    def leaf_map(leaf, func):
        if leaf.leftChild == None and leaf.rightChild == None:
            func(leaf)
        if leaf.leftChild:
            Tree.leaf_map(leaf.leftChild, func)
        if leaf.rightChild:
            Tree.leaf_map(leaf.rightChild, func)

    def map(self, func):
        current_leaf = self._root
        reviewed_leafs = set()
        last_leafs = []

        while current_leaf != None:
            func(current_leaf)
            reviewed_leafs.add(current_leaf)

            if current_leaf.leftChild and current_leaf.leftChild not in reviewed_leafs:
                last_leafs.append(current_leaf)
                current_leaf = current_leaf.leftChild
            elif current_leaf.rightChild and current_leaf.rightChild not in reviewed_leafs:
                last_leafs.append(current_leaf)
                current_leaf = current_leaf.rightChild
            else:
                current_leaf = last_leafs.pop() if len(last_leafs) else None


    def split(self):
        Tree.split_space(self._root)

    def draw_map(self, name):
        im = Image.new('RGB', (self._root.width, self._root.height))
        draw = ImageDraw.Draw(im)

        current_leaf = self._root
        reviewed_leafs = set()
        last_leafs = []
        print('+')

        while current_leaf != None:
            if current_leaf.leftChild == None and current_leaf.rightChild == None:
                draw.rectangle(current_leaf.get_room(), fill=0xFFFFFF)
                # import pdb
                # pdb.set_trace()
            
            reviewed_leafs.add(current_leaf)

            if current_leaf.leftChild and current_leaf.leftChild not in reviewed_leafs:
                last_leafs.append(current_leaf)
                current_leaf = current_leaf.leftChild
            elif current_leaf.rightChild and current_leaf.rightChild not in reviewed_leafs:
                last_leafs.append(current_leaf)
                current_leaf = current_leaf.rightChild
            else:
                current_leaf = last_leafs.pop() if len(last_leafs) else None
        del draw
        im.save(name)

    def printt(self):
        Tree.print_tree(self._root)

    def t_print(self):
        leaf = self._root
        printed_points = set()
        last_point = []
        while leaf != None:
            if leaf not in printed_points:
                print(leaf)
                printed_points.add(leaf)

            if leaf.leftChild and leaf.leftChild not in printed_points:
                last_point.append(leaf)
                leaf = leaf.leftChild
            elif leaf.rightChild and leaf.rightChild not in printed_points:
                last_point.append(leaf)
                leaf = leaf.rightChild
            else:
                leaf = last_point.pop() if len(last_point) else None


if __name__ == '__main__':
    T = Tree(0,0,100,100)
    T.split()
    # T.printt()
    # print()
    # T.t_print()
    # import pdb
    # pdb.set_trace()
    print()
    T.create_rooms()
    print("+")
    T.leaf_map(T._root, print)
    T.draw_map('map.jpg')
