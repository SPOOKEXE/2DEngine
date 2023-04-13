
from math import sqrt
from typing import Union

FLOAT_TUP = tuple[float, float]

def does_circle_contain_point(circle, point) -> bool:
	dx = (point.x - circle.x)
	dy = (point.y - circle.y)
	r = circle.radius
	return (dx*dx + dy*dy) <= (r*r)

def does_circle_intersect_rectangle(circle, rectangle) -> bool:
	right = (rectangle.x + rectangle.w)
	bottom = (rectangle.y + rectangle.h)
	
	closestX = circle.x
	if circle.x < rectangle.x:
		closestX = rectangle.x
	elif circle.x > right:
			closestX = right

	closestY = circle.y
	if circle.y < rectangle.y:
		closestY = rectangle.y
	elif circle.y > bottom:
		closestY = bottom

	#closestX = (circle.x < rectangle.x and rectangle.x or (circle.x > right and right or circle.x))
	#closestY = (circle.y < rectangle.y and rectangle.y or (circle.y > bottom and bottom or circle.y))
	dx = closestX - circle.x
	dy = closestY - circle.y
	return ( dx * dx + dy * dy ) <= (circle.radius * circle.radius)

def does_circle_intersect_circle(circle0, circle1) -> bool:
	dx = circle1.x - circle0.x
	dy = circle1.y - circle0.y
	r = circle0.radius + circle1.radius
	return (dx*dx + dy*dy) <= (r * r)

def does_rectangle_intersect_rectangle(rect0, rect1) -> bool:
	self_1 = (rect0.x + rect0.w, rect0.y + rect0.h)
	range_1 = (rect1.x + rect1.w, rect1.y + rect1.h)
	return not ( self_1[0] < rect1.x or range_1[0] < rect0.x or self_1[1] < rect1.y or range_1[1] < rect0.y )

def does_rectangle_contain_point(rectangle, point) -> bool:
	right = (rectangle.x + rectangle.w)
	bottom = (rectangle.y + rectangle.h)
	return (rectangle.x <= point.x and point.x <= right and rectangle.y <= point.y and point.y <= bottom)

def does_line_intersect_line(line_seg0, line_seg1) -> bool:
	dy1 = (line_seg1.y1-line_seg1.y0)
	dy0 = (line_seg0.y1-line_seg0.y0)
	dx1 = (line_seg1.x0-line_seg1.x1)
	d = (line_seg0.x1-line_seg0.x0) * dy1 + dy0 *  dx1
	if d == 0:
		return None
	dx01 = (line_seg1.x0-line_seg0.x0)
	dy10 = (line_seg1.y0-line_seg0.y0)
	t = (dx01 * dy1 + dy10 * dx1) / d
	u = (dx01 * dy0 + dy10 * (line_seg0.x0-line_seg0.x1)) / d
	return (0 <= t <= 1) and (0 <= u <= 1)

def does_line_intersect_rectangle(line_seg, rect) -> bool:
	rect_topLeft = (rect.x, rect.y)
	rect_bottomLeft = (rect.x, rect.y + rect.h)
	rect_topRight = (rect.x + rect.w, rect.y)
	rect_bottomRight = (rect.x + rect.w, rect.y + rect.h)
	line0 = (line_seg.x0, line_seg.y0)
	line1 = (line_seg.x1, line_seg.y1)
	return does_line_intersect_line( line0, line1, rect_topLeft, rect_topRight ) or does_line_intersect_line( line0, line1, rect_bottomLeft, rect_bottomRight ) or does_line_intersect_line( line0, line1, rect_topLeft, rect_bottomLeft ) or does_line_intersect_line( line0, line1, rect_topRight, rect_bottomRight ) or False

def does_line_intersect_circle(line, circle) -> bool:
	p1x, p1y = line.x0, line.y0
	p2x, p2y = line.x1, line.y1
	cx, cy = circle.x, circle.y
	(x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
	dx, dy = (x2 - x1), (y2 - y1)
	dr = sqrt(dx * dx + dy * dy)
	big_d = x1 * y2 - x2 * y1
	discriminant = (circle.radius * circle.radius * dr * dr) - (big_d * big_d)
	if discriminant < 0:
		return False
	return True

def get_line_line_intersection(line_seg0, line_seg1) -> Union[FLOAT_TUP, None]:
	dy1 = (line_seg1.y1-line_seg1.y0)
	dy0 = (line_seg0.y1-line_seg0.y0)
	dx1 = (line_seg1.x0-line_seg1.x1)
	d = (line_seg0.x1-line_seg0.x0) * dy1 + dy0 *  dx1
	if d == 0:
		return None
	dx01 = (line_seg1.x0-line_seg0.x0)
	dy10 = (line_seg1.y0-line_seg0.y0)
	t = (dx01 * dy1 + dy10 * dx1) / d
	u = (dx01 * dy0 + dy10 * (line_seg0.x0-line_seg0.x1)) / d
	if (0 <= t <= 1) and (0 <= u <= 1):
		return round(line_seg0.x1 * t + line_seg0.x0 * (1-t)), round(line_seg0.y1 * t + line_seg0.y0 * (1-t))
	return None

def get_line_rectangle_intersection(line_seg, rectangle) -> Union[FLOAT_TUP, None]:
	line0 = (line_seg.x0, line_seg.y0)
	line1 = (line_seg.x1, line_seg.y1)
	rect_topLeft = (rectangle.x, rectangle.y)
	rect_topRight = (rectangle.x + rectangle.w, rectangle.y)
	rect_bottomRight = (rectangle.x + rectangle.w, rectangle.y + rectangle.h)
	rect_bottomLeft = (rectangle.x, rectangle.y + rectangle.h)
	return get_line_line_intersection( line0, line1, rect_topLeft, rect_topRight ) or get_line_line_intersection( line0, line1, rect_bottomLeft, rect_bottomRight ) or get_line_line_intersection( line0, line1, rect_topLeft, rect_bottomLeft ) or get_line_line_intersection( line0, line1, rect_topRight, rect_bottomRight ) or None

def get_line_circle_intersection(line, circle, is_segment_line=True, tangent_tol=1e-9) -> Union[FLOAT_TUP, list[FLOAT_TUP], None]:
	p1x, p1y = line.x0, line.y0
	p2x, p2y = line.x1, line.y1
	cx, cy = circle.x, circle.y
	(x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
	dx, dy = (x2 - x1), (y2 - y1)
	dr = sqrt(dx * dx + dy * dy)
	big_d = (x1 * y2) - (x2 * y1)
	discriminant = (circle.radius * circle.radius * dr * dr) - (big_d * big_d)
	if discriminant < 0:
		return None
	intersections = [
		(
			cx + (big_d * dy + sign * (-1 if dy < 0 else 1) * dx * sqrt(discriminant)) / (dr * dr),
			cy + (-big_d * dx + sign * abs(dy) * sqrt(discriminant)) / (dr * dr)
		)
		for sign in ((1, -1) if dy < 0 else (-1, 1))
	]
	if is_segment_line:
		fraction_along_segment = [(xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy for xi, yi in intersections]
		intersections = [pt for pt, frac in zip(intersections, fraction_along_segment) if 0 <= frac <= 1]
	if len(intersections) == 2 and abs(discriminant) <= tangent_tol: # If line is tangent to circle, return just one point (as both intersections have same location)
		return intersections[0]
	return intersections
