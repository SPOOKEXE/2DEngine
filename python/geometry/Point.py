from geometry import Intersect

class Point:
	x = y = 0
	data = None

	def does_intersect_rectangle(self, rect) -> bool:
		return Intersect.does_rectangle_contain_point(rect, self)

	def does_intersect_circle(self, circle) -> bool:
		return Intersect.does_circle_contain_point(circle, self)

	def __init__(self, x, y, data=None):
		self.x = x
		self.y = y
		self.data = data
