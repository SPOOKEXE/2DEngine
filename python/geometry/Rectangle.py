from geometry import Intersect

from typing import Union
FLOAT_TUP = tuple[float, float]

class Rectangle:
	x = y = w = h = None

	def does_contain_point(self, point) -> bool:
		return Intersect.does_rectangle_contain_point(self, point)

	def does_intersect_rectangle(self, rect) -> bool:
		return Intersect.does_rectangle_intersect_rectangle(self, rect)

	def does_intersect_circle(self, circle) -> bool:
		return Intersect.does_circle_intersect_rectangle(circle, self)

	def does_intersect_line_segment(self, line_seg) -> bool:
		return Intersect.does_line_intersect_rectangle(line_seg, self)

	def get_line_rectangle_intersection(self, line_seg) -> Union[FLOAT_TUP, None]:
		return Intersect.get_line_rectangle_intersection(line_seg, self)

	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
