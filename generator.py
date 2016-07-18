#! /bin/python3

class Point:
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

	@.setter
	def y(self, value):
		self._y = value
	@property
	def width(self):
		return self._width

	@.setter
	def width(self, value):
		self._width = value
	@property
	def height(self):
		return self._height

	@.setter
	def height(self, value):
		self._height = value


class Rectangle:
	def __init__:
		pass

class Leaf:
	def __init__:
		pass


if __name__ == '__main__':
	print("Hello world.")
