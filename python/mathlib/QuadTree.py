
from typing import Union
from os import path as os_path
from sys import path as sys_path

FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))
sys_path.append( os_path.join(FILE_DIRECTORY, "../") )

from geometry.Rectangle import Rectangle
from geometry.Point import Point
from geometry.Circle import Circle

sys_path.pop()

DEFAULT_QUAD_TREE_CAPACITY = 4

QD_T_COMPONENTS = Union[Rectangle, Circle, Point]
VALID_CLASSES = [Rectangle.__class__, Circle.__class__, Point.__class__]
VALID_RANGE_CLASSES = [Rectangle.__class__, Circle.__class__]

class QuadTree:
	boundary=None
	capacity=-1
	points=[]

	_divided=False
	_northeast=None
	_northwest=None
	_southeast=None
	_southwest=None

	@staticmethod
	def is_shape_a_valid_shape(_shape) -> None:
		return VALID_CLASSES.count(_shape.__class__) != 0 and VALID_CLASSES.count(_shape.__class__) != 0

	@staticmethod
	def does_x_collide_with_y(value0 : QD_T_COMPONENTS, value1 : QD_T_COMPONENTS) -> bool:
		# if both are points, compare them
		if value0.__class__ == value1.__class__ == Point.__class__:
			return value0.x == value1.x and value0.y == value1.y

		# if first argument is a point, flip the input
		if value0.__class__ == Point.__class__:
			return QuadTree.does_x_collide_with_y(value1, value0)

		# passed value0 is a circle or rectangle
		# also they all share the same function names,
		# so we can keep it simple here
		if value1.__class__ == Rectangle.__class__:
			return value0.does_intersects_rectangle(value1)
		elif value1.__class__ == Circle.__class__:
			return value0.does_intersects_circle(value1)
		elif value1.__class__ == Point.__class__:
			return value0.does_contains_point(value1)

	def query(self, _range : Union[Rectangle, Circle], point_array : Union[list, None]) -> list:
		if VALID_RANGE_CLASSES.count(_range.__class__) == 0:
			raise ValueError("Invalid _range argument passed. Does not match the class of Rectangle or Circle.")
		if point_array == None:
			point_array = []
		if self.does_x_collide_with_y(_range, self.boundary):
			for p in self.points:
				if self.does_x_collide_with_y(_range, p): #if (p.__class__ == Point.__class__ and _range.does_contains_point(p)) or (p.__class__ == Rectangle.__class__ and _range.does_intersects_rectangle(p)):
					if point_array.count(p) == 0:
						point_array.append(p)
			if self._divided:
				self._northwest.query(_range, point_array)
				self._northeast.query(_range, point_array)
				self._southwest.query(_range, point_array)
				self._southeast.query(_range, point_array)
		return point_array

	def insert_single(self, shape : QD_T_COMPONENTS) -> bool:
		if not QuadTree.is_shape_a_valid_shape(shape):
			raise ValueError("Invalid object was passed into insert_single.")
		contains_shape = self.does_x_collide_with_y(self.boundary, shape) #(shape.__class__ == Point.__class__ and self.boundary.does_contain_point(shape)) or (shape.__class__ == Rectangle.__class__ and self.boundary.does_intersects_rectangle(shape))
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

	def insert_array(self, points : list[QD_T_COMPONENTS]) -> None:
		for shape in points:
			if not QuadTree.is_shape_a_valid_shape(shape):
				print(f"Invalid object was passed into insert_array at index {points.index(shape)}.")
				continue
			contains_shape = self.does_x_collide_with_y(self.boundary, shape) #(shape.__class__ == Point.__class__ and self.boundary.does_contain_point(shape)) or (shape.__class__ == Rectangle.__class__ and self.boundary.does_intersect_rectangle(shape))
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
		self._northeast = QuadTree( boundary = Rectangle( x + w/2, y - h/2, w/2, h/2 ), capacity = self.capacity )
		self._northwest = QuadTree( boundary = Rectangle( x - w/2, y - h/2, w/2, h/2 ), capacity = self.capacity )
		self._southeast = QuadTree( boundary = Rectangle( x + w/2, y + h/2, w/2, h/2 ), capacity = self.capacity)
		self._southwest = QuadTree( boundary = Rectangle( x - w/2, y + h/2, w/2, h/2 ), capacity = self.capacity )
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
