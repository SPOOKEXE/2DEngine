
from os import path as os_path
from sys import path as sys_path

FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))
sys_path.append( os_path.join(FILE_DIRECTORY, "../") )

from geometry import Intersect
from geometry.Rectangle import Rectangle
from geometry.Point import Point
from geometry.Circle import Circle
from geometry.LineSegment import LineSegment
from mathlib import QuadTree

sys_path.pop()

class SimulationMethods:
	def dist_sqrd(x0, y0, x1, y1) -> float:
		dx = x1 - x0
		dy = y1 - y0
		return (dx * dx) + (dy * dy)

	# def raycast( object_array : list[Object], ox, oy, dx, dy ):
	# 	hit = point = None
	# 	dist = -1
	# 	start_p = (ox, oy)
	# 	finish_p = (ox + dx, oy + dy)
	# 	def check_closest(hitt, pointt):
	# 		nonlocal hit, dist, point
	# 		distt = SimulationMethods.dist_sqrd( start_p[0], start_p[1], pointt[0], pointt[1] )
	# 		if (hit == None) or (distt < dist):
	# 			hit = hitt
	# 			dist = distt
	# 			point = pointt
	# 	for obj in object_array:
	# 		if obj.isA( Square ):
	# 			ix, iy = Intersect.line_rect_intersect( start_p, finish_p, (obj.x, obj.y), (obj.x + obj.w, obj.y + obj.h) )
	# 			if ix != None:
	# 				check_closest(obj, (ix, iy))
	# 		elif obj.isA( Circle ):
	# 			dat = Intersect.line_circle_intersection( (obj.x, obj.y), obj.radius, start_p, finish_p )
	# 			if dat != None:
	# 				check_closest(obj, type(dat) == list and dat[0] or dat)
	# 	return hit, dist, point

class Simulation:
	pass
