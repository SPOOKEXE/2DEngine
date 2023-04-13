
from typing import Union

FLOAT_TUP = tuple[float, float]

from os import path as os_path
from sys import path as sys_path

FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))
sys_path.append( os_path.join(FILE_DIRECTORY, "../") )

from geometry.Rectangle import Rectangle
from geometry.Point import Point
from geometry.Circle import Circle
from geometry.LineSegment import LineSegment

sys_path.pop()

DEFAULT_QUAD_TREE_CAPACITY = 16
MAX_QUAD_TREE_DEPTH = 6

QD_T_COMPONENTS = Union[Rectangle, Circle, Point]
QD_RANGE_COMPONENTS = Union[Rectangle, Circle]

VALID_CLASSES = [Rectangle , Circle , Point ]
VALID_RANGE_CLASSES = [Rectangle , Circle ]

class QuadTree:
	depth = 0
	boundary : Rectangle = None
	capacity = -1
	shapes : list[QD_T_COMPONENTS] = []

	_divided=False
	_northeast=None
	_northwest=None
	_southeast=None
	_southwest=None

	@staticmethod
	def is_shape_a_valid_shape(_shape) -> bool:
		# if the class is directly found in the valid classes, return true
		if VALID_CLASSES.count(_shape.__class__) != 0:
			return True
		# if the class is not, check if the class is a subclass of any of the valid ones (inheriting it)
		for base in VALID_CLASSES:
			if issubclass(_shape.__class__, base):
				return True
		return False

	@staticmethod
	def is_shape_a_valid_range(_shape) -> bool:
		# if the class is directly found in the valid classes, return true
		if VALID_RANGE_CLASSES.count(_shape.__class__) != 0:
			return True
		# if the class is not, check if the class is a subclass of any of the valid ones (inheriting it)
		for base in VALID_RANGE_CLASSES:
			if issubclass(_shape.__class__, base):
				return True
		return False

	@staticmethod
	def find_ray_collision_with_y(ray : LineSegment, value1 : Union[Rectangle, Circle, LineSegment]) -> Union[FLOAT_TUP, tuple[FLOAT_TUP, FLOAT_TUP]]:
		if issubclass(value1.__class__, Rectangle):
			return ray.get_line_rectangle_intersection(value1)
		elif issubclass(value1.__class__, Circle):
			return ray.get_line_circle_intersection(value1)
		elif issubclass(value1.__class__, LineSegment):
			return ray.get_line_line_intersection(value1)
		print("invalid collidable class was passed in.")
		return None

	@staticmethod
	def does_x_collide_with_y(value0 : QD_T_COMPONENTS, value1 : QD_T_COMPONENTS) -> bool:
		# if both are points, compare them
		if value0.__class__ == value1.__class__ == Point.__class__:
			return (value0.x == value1.x) and (value0.y == value1.y)

		# passed value0 is a circle or rectangle
		# also they all share the same function names,
		# so we can keep it simple here
		if issubclass(value1.__class__, Rectangle):
			return value0.does_intersect_rectangle(value1)
		elif issubclass(value1.__class__, LineSegment):
			return value0.does_intersect_line_segment(value1)
		elif issubclass(value1.__class__, Circle):
			return value0.does_intersect_circle(value1)
		elif issubclass(value1.__class__, Point):
			return value0.does_contain_point(value1)
		print("invalid class was passed in.")
		return False

	def query(self, _range : Union[Rectangle, Circle], shape_array : Union[list, None]) -> list:
		if not QuadTree.is_shape_a_valid_range(_range):
			print("Invalid _range argument passed. Does not match the class of Rectangle or Circle.")
			return None
		if shape_array == None:
			shape_array = []
		if self.does_x_collide_with_y(_range, self.boundary):
			for shape in self.shapes:
				if self.does_x_collide_with_y(_range, shape):
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
			return False
		contains_shape = self.does_x_collide_with_y(self.boundary, shape)
		if not contains_shape:
			#print('does not contain')
			return False
		if (self.depth==MAX_QUAD_TREE_DEPTH) or len(self.shapes) < self.capacity:
			#print('append')
			self.shapes.append(shape)
			return True
		if not self._divided:
			#print('subdivide')
			self._subdivide()
		if self._northeast.insert_single(shape):
			#print('ne')
			return True
		if self._northwest.insert_single(shape):
			#print('nw')
			return True
		if self._southeast.insert_single(shape):
			#print('se')
			return True
		if self._southwest.insert_single(shape):
			#print('sw')
			return True
		#print('fail')
		return False

	def insert_array(self, shapes : list[QD_T_COMPONENTS]) -> None:
		for shape in shapes:
			self.insert_single(shape)

	def _subdivide(self) -> None:
		w = self.boundary.w
		h = self.boundary.h
		self._northeast = QuadTree(boundary=Rectangle( self.boundary.x+w/4, self.boundary.y-h/4, w/2, h/2 ), capacity=self.capacity, depth=self.depth+1)
		self._northwest = QuadTree(boundary=Rectangle( self.boundary.x-w/4, self.boundary.y-h/4, w/2, h/2 ), capacity=self.capacity, depth=self.depth+1)
		self._southeast = QuadTree(boundary=Rectangle( self.boundary.x+w/4, self.boundary.y+h/4, w/2, h/2 ), capacity=self.capacity, depth=self.depth+1)
		self._southwest = QuadTree(boundary=Rectangle( self.boundary.x-w/4, self.boundary.y+h/4, w/2, h/2 ), capacity=self.capacity, depth=self.depth+1)
		self._divided = True

	def get_shapes(self, array=[] ) -> list:
		for shape in self.shapes:
			if array.count(shape) == 0:
				array.append(shape)
		if self._divided:
			self._northeast.get_shapes(array=array)
			self._northwest.get_shapes(array=array)
			self._southeast.get_shapes(array=array)
			self._southwest.get_shapes(array=array)
		return array

	def find_quadtree_from_point(self, point : Point):
		if not self.boundary.does_contain_point( point ):
			return None
		if self._divided:
			return self._northeast.find_quadtree_from_point(point) or self._northwest.find_quadtree_from_point(point) or self._southeast.find_quadtree_from_point(point) or self._southwest.find_quadtree_from_point(point) or None
		return self

	def brute_raycast(self, line_seg : LineSegment) -> tuple[QD_RANGE_COMPONENTS, tuple[float, float], None]:
		def dist_sqrd(x0, y0, x1, y1) -> float:
			dx = (x1 - x0)
			dy = (y1 - y0)
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
			dat = self.find_ray_collision_with_y(line_seg, obj)
			#print(dat)
			if type(dat) == list:
				dat = dat[0]
			if dat != None:
				check_closest(obj, dat)
		return hit, dist, point

	def __init__(self, boundary=None, capacity=DEFAULT_QUAD_TREE_CAPACITY, depth=0):
		self.boundary = boundary
		self.capacity = capacity
		self.depth = depth
		print(depth)
