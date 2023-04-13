
from typing import Union
from os import path as os_path
from sys import path as sys_path

FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))
sys_path.append( os_path.join(FILE_DIRECTORY, "../") )

from geometry.Rectangle import Rectangle
from geometry.Point import Point
from geometry.Circle import Circle
from geometry.LineSegment import LineSegment

sys_path.pop()

DEFAULT_QUAD_TREE_CAPACITY = 4

QD_T_COMPONENTS = Union[Rectangle, Circle, Point]
QD_RANGE_COMPONENTS = Union[Rectangle, Circle]

VALID_CLASSES = [Rectangle , Circle , Point ]
VALID_RANGE_CLASSES = [Rectangle , Circle ]

class QuadTree:
	boundary : Rectangle = None
	capacity = -1
	shapes : list[QD_T_COMPONENTS] = []

	_divided=False
	_northeast=None
	_northwest=None
	_southeast=None
	_southwest=None

	@staticmethod
	def is_shape_a_valid_shape(_shape) -> None:
		# if the class is directly found in the valid classes, return true
		if VALID_CLASSES.count(_shape.__class__) != 0:
			return True
		# if the class is not, check if the class is a subclass of any of the valid ones (inheriting it)
		for base in VALID_CLASSES:
			if issubclass(_shape.__class__, base):
				return True
		return False

	@staticmethod
	def does_x_collide_with_y(value0 : QD_T_COMPONENTS, value1 : QD_T_COMPONENTS) -> bool:
		# if both are points, compare them
		if value0.__class__ == value1.__class__ == Point.__class__:
			return (value0.x == value1.x) and (value0.y == value1.y)

		# if first argument is a point, flip the input
		if value0.__class__ == Point.__class__:
			return QuadTree.does_x_collide_with_y(value1, value0)

		# passed value0 is a circle or rectangle
		# also they all share the same function names,
		# so we can keep it simple here
		if value1.__class__ == Rectangle.__class__:
			return value0.does_intersect_rectangle(value1)
		elif value1.__class__ == LineSegment.__class__:
			return value0.does_intersect_line_segment(value1)
		elif value1.__class__ == Circle.__class__:
			print('c')
			return value0.does_intersect_circle(value1)
		elif value1.__class__ == Point.__class__:
			return value0.does_contain_point(value1)

	def query(self, _range : Union[Rectangle, Circle], shape_array : Union[list, None]) -> list:
		if VALID_RANGE_CLASSES.count(_range.__class__) == 0:
			raise ValueError("Invalid _range argument passed. Does not match the class of Rectangle or Circle.")
		if shape_array == None:
			shape_array = []
		if self.does_x_collide_with_y(_range, self.boundary):
			for shape in self.shapes:
				if self.does_x_collide_with_y(_range, shape): #if (p.__class__ == Point.__class__ and _range.does_contains_point(p)) or (p.__class__ == Rectangle.__class__ and _range.does_intersects_rectangle(p)):
					if shape_array.count(shape) == 0:
						shape_array.append(shape)
			if self._divided:
				self._northwest.query(_range, shape_array)
				self._northeast.query(_range, shape_array)
				self._southwest.query(_range, shape_array)
				self._southeast.query(_range, shape_array)
		return shape_array

	def insert_single(self, shape : QD_T_COMPONENTS) -> bool:
		if not QuadTree.is_shape_a_valid_shape(shape):
				print("Invalid object was passed into insert_single.")
		contains_shape = self.does_x_collide_with_y(self.boundary, shape)
		if not contains_shape:
			return False
		if len(self.shapes) < self.capacity:
			self.shapes.append(shape)
			return True
		if not self._divided:
			self._subdivide()
		if self._northeast.insert_single(shape) or self._northwest.insert_single(shape) or self._southeast.insert_single(shape) or self._southwest.insert_single(shape):
			return True
		return False

	def insert_array(self, shapes : list[QD_T_COMPONENTS]) -> None:
		for shape in shapes:
			if not QuadTree.is_shape_a_valid_shape(shape):
				print(f"Invalid object was passed into insert_array at index {shapes.index(shape) + 1}.")
				continue
			contains_shape = self.does_x_collide_with_y(self.boundary, shape)
			if not contains_shape:
				print('boundary does not contain shape')
				continue
			if len(self.shapes) < self.capacity:
				self.shapes.append(shape)
				continue
			if not self._divided:
				self._subdivide()
			print('insert in depth')
			if self._northeast.insert_single(shape) or self._northwest.insert_single(shape) or self._southeast.insert_single(shape) or self._southwest.insert_single(shape):
				continue

	def _subdivide(self) -> None:
		x = self.boundary.x
		y = self.boundary.y
		w = self.boundary.w
		h = self.boundary.h
		self._northeast = QuadTree( boundary = Rectangle( x + w/4, y - h/4, w/2, h/2 ), capacity = self.capacity )
		self._northwest = QuadTree( boundary = Rectangle( x - w/4, y - h/4, w/2, h/2 ), capacity = self.capacity )
		self._southeast = QuadTree( boundary = Rectangle( x + w/4, y + h/4, w/2, h/2 ), capacity = self.capacity)
		self._southwest = QuadTree( boundary = Rectangle( x - w/4, y + h/4, w/2, h/2 ), capacity = self.capacity )
		self._divided = True

	def get_shapes(self, shapes_array=None ) -> list:
		if shapes_array == None:
			shapes_array = []
		for shape in self.shapes:
			if shapes_array.count(shape) == 0:
				shapes_array.append(shape)
		if self._divided:
			self._northeast.get_shapes(shapes_array=shapes_array)
			self._northwest.get_shapes(shapes_array=shapes_array)
			self._southeast.get_shapes(shapes_array=shapes_array)
			self._southwest.get_shapes(shapes_array=shapes_array)
		return shapes_array

	def find_quadtree_from_point(self, point : Point):
		if not self.boundary.does_contain_point( point ):
			return None
		if self._divided:
			return self._northeast.find_quadtree_from_point(point) or self._northwest.find_quadtree_from_point(point) or self._southeast.find_quadtree_from_point(point) or self._southwest.find_quadtree_from_point(point) or None
		return self

	def brute_raycast(self, line_seg : LineSegment) -> tuple[QD_RANGE_COMPONENTS, tuple[float, float], None]:
		def dist_sqrd(x0, y0, x1, y1) -> float:
			dx = x1 - x0
			dy = y1 - y0
			return (dx * dx) + (dy * dy)
		hit = point = None
		dist = -1
		def check_closest(hitt, pointt):
			nonlocal hit, dist, point
			distt = dist_sqrd( line_seg.x0, line_seg.y0, pointt[0], pointt[1] )
			if (hit == None) or (distt < dist):
				hit = hitt
				dist = distt
				point = pointt
		for obj in self.get_shapes():
			dat = self.does_x_collide_with_y(obj, line_seg)
			if dat != None:
				check_closest(obj, dat)
		return hit, dist, point

	def __init__(self, boundary=None, capacity=DEFAULT_QUAD_TREE_CAPACITY, shapes=[]):
		self.boundary = boundary
		self.capacity = capacity
		if len(shapes) > 0:
			self.insert_array(shapes)
