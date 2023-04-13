from geometry import Intersect

from typing import Union
FLOAT_TUP = tuple[float, float]

class LineSegment:
	x0 = y0 = None
	x1 = y1 = None

	def does_intersects_line_segment(self, line_seg) -> bool:
		return Intersect.does_line_intersect_line(self, line_seg)

	def does_intersects_rectangle(self, rectangle) -> bool:
		return Intersect.does_line_intersect_rectangle(self, rectangle)

	def does_intersects_circle(self, circle) -> bool:
		return Intersect.does_line_intersect_circle(self, circle)

	def get_line_line_intersection(self, line_seg) -> FLOAT_TUP:
		return Intersect.get_line_line_intersection(self, line_seg)

	def get_line_circle_intersection(self, circle) -> Union[FLOAT_TUP, list[FLOAT_TUP], None]:
		return Intersect.get_line_circle_intersection(self, circle)

	def get_line_rectangle_intersection(self, rectangle) -> Union[FLOAT_TUP, None]:
		return Intersect.get_line_rectangle_intersection(self, rectangle)

	def __init__(self, x0, y0, x1, y1):
		self.x0 = x0
		self.y0 = y0
		self.x1 = x1
		self.y1 = y1
