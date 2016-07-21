#! /bin/python3

from random import random, randrange

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


class Leaf(Rectangle):
	MIN_LEAF_SIDE = 4
	MIN_ROOM_SIDE = 3
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
		room_x = self._x + randrange(1, self._width - 1, 1)
		room_y = self._y + randrange(1, self._height - 1, 1)
		room_w = randrange(Leaf.MIN_ROOM_SIDE, self._width - room_x - 2, 1)
		room_h = randrange(Leaf.MIN_ROOM_SIDE, self._height - room_y - 2, 1)
		self.room = Rectangle(room_x, room_y, room_w, room_h)

class Tree:
	def __init__(self, x, y, width, height):
		self._root = Leaf(x, y, width, height)

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

	def create_rooms(self):
		pass

	def split(self):
		Tree.split_space(self._root)

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
	T = Tree(0,0,10,10)
	T.split()
	T.printt()
	print()
	T.t_print()


