
from typing import Union

DEFAULT_QUAD_TREE_CAPACITY = 4

class Point:
	x = y = 0
	dat = None
	def __init__(self, x, y, dat=None):
		self.x = x
		self.y = y
		self.dat = dat

class Rectangle:
	x = y = w = h = None

	def contains(self, point) -> bool:
		right = (self.x + self.w)
		bottom = (self.y + self.h)
		return (self.x <= point.x and point.x <= right and self.y <= point.y and point.y <= bottom)

	def intersects(self, rect) -> bool:
		right = (self.x + self.w)
		bottom = (self.y + self.h)
		rangeright = rect.x + rect.w
		rangebottom = rect.y + rect.h
		return not (right < rect.x or rangeright < self.x or bottom < rect.y or rangebottom < self.y )

	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

class QuadTree:
	boundary=None
	capacity=-1
	points=[]

	_divided=False
	_northeast = None
	_northwest = None
	_southeast = None
	_southwest = None

	def query(self, _range : Rectangle, point_array : Union[list, None]) -> list:
		if point_array == None:
			point_array = []
		if _range.intersects(self.boundary):
			for p in self.points:
				if (p.__class__ == Point.__class__ and _range.contains(p)) or (p.__class__ == Rectangle.__class__ and _range.intersects(p)):
					if point_array.count(p) == 0:
						point_array.append(p)
			if self._divided:
				self._northwest.query(_range, point_array)
				self._northeast.query(_range, point_array)
				self._southwest.query(_range, point_array)
				self._southeast.query(_range, point_array)
		return point_array

	def insert_single(self, shape) -> bool:
		contains_shape = (shape.__class__ == Point.__class__ and self.boundary.contains(shape)) or (shape.__class__ == Rectangle.__class__ and self.boundary.intersects(shape))
		if not contains_shape:
			return False
		
		if len(self.points) < self.capacity:
			self.points.append(shape)
			return True

		if not self._divided:
			self._subdivide()

		if self._northeast.insert_single(shape) or self._northwest.insert_single(shape) or self._southeast.insert_single(shape) or self._southwest.insert_single(shape):
			return True
		return False

	def insert(self, points : list[Rectangle, Point]) -> None:
		for shape in points:
			contains_shape = (shape.__class__ == Point.__class__ and self.boundary.contains(shape)) or (shape.__class__ == Rectangle.__class__ and self.boundary.intersects(shape))
			if not contains_shape:
				continue

			if len(self.points) < self.capacity:
				self.points.append(shape)
				continue

			if not self._divided:
				self._subdivide()

			if self._northeast.insert_single(shape) or self._northwest.insert_single(shape) or self._southeast.insert_single(shape) or self._southwest.insert_single(shape):
				continue

	def _subdivide(self) -> None:
		x = self.boundary.x
		y = self.boundary.y
		w = self.boundary.w
		h = self.boundary.h

		self._northeast = QuadTree(
			boundary = Rectangle( x + w/2, y - h/2, w/2, h/2 ),
			capacity = self.capacity
		)

		self._northwest = QuadTree(
			boundary = Rectangle( x - w/2, y - h/2, w/2, h/2 ),
			capacity = self.capacity
		)

		self._southeast = QuadTree(
			boundary = Rectangle( x + w/2, y + h/2, w/2, h/2 ),
			capacity = self.capacity
		)

		self._southwest = QuadTree(
			boundary = Rectangle( x - w/2, y + h/2, w/2, h/2 ),
			capacity = self.capacity
		)

		self._divided = True

	def get_points(self, points_array ) -> list:
		if points_array == None:
			points_array = []
		for p in self.points:
			if points_array.count(p) == 0:
				points_array.append(p)
		if self._divided:
			self._northeast.get_points(points_array)
			self._northwest.get_points(points_array)
			self._southeast.get_points(points_array)
			self._southwest.get_points(points_array)
		return points_array

	def __init__(self, boundary=None, capacity=DEFAULT_QUAD_TREE_CAPACITY, points=[]):
		self.boundary = boundary
		self.capacity = capacity
