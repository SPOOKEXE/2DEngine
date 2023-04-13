
from geometry import Intersect

from typing import Union
FLOAT_TUP = tuple[float, float]

class Circle:
	x = y = radius = None

	def does_contain_point(self, point) -> bool:
		return Intersect.does_circle_contain_point(self, point)

	def does_intersect_rectangle(self, rectangle) -> bool:
		return Intersect.does_circle_intersect_rectangle(self, rectangle)

	def does_intersect_circle(self, circle) -> bool:
		return Intersect.does_circle_intersect_circle(self, circle)

	def does_intersect_line_segment(self, line_seg) -> bool:
		return Intersect.does_line_intersect_circle(line_seg, self)

	def get_line_circle_intersection(self, line_seg) -> Union[FLOAT_TUP, list[FLOAT_TUP], None]:
		return Intersect.get_line_circle_intersection(line_seg, self)

	def __init__(self, x, y, radius):
		self.x = x
		self.y = y
		self.radius = radius
