
from typing import Union

INT_TUPLE = tuple[int, int]
FLOAT_TUPLE = tuple[float, float]

def circle_circle_intersect( circle0_xy : FLOAT_TUPLE, circle0_radius : float, circle1_xy : FLOAT_TUPLE, circle1_radius : float ):
	dx = circle1_xy[0] - circle0_xy[0]
	dy = circle1_xy[1] - circle0_xy[1]
	r = circle0_radius + circle1_radius
	return (dx*dx + dy*dy) <= (r * r)

def line_line_intersect(P0 : FLOAT_TUPLE, P1 : FLOAT_TUPLE, Q0 : FLOAT_TUPLE, Q1 : FLOAT_TUPLE) -> Union[FLOAT_TUPLE, None]:
	d = (P1[0]-P0[0]) * (Q1[1]-Q0[1]) + (P1[1]-P0[1]) * (Q0[0]-Q1[0]) 
	if d == 0:
		return None
	t = ((Q0[0]-P0[0]) * (Q1[1]-Q0[1]) + (Q0[1]-P0[1]) * (Q0[0]-Q1[0])) / d
	u = ((Q0[0]-P0[0]) * (P1[1]-P0[1]) + (Q0[1]-P0[1]) * (P0[0]-P1[0])) / d
	if (0 <= t <= 1) and (0 <= u <= 1):
		return round(P1[0] * t + P0[0] * (1-t)), round(P1[1] * t + P0[1] * (1-t))
	return None

def line_rect_intersect( line0 : FLOAT_TUPLE, line1 : FLOAT_TUPLE, rect_topLeft: FLOAT_TUPLE, rect_bottomRight : FLOAT_TUPLE ) -> Union[FLOAT_TUPLE, None]:
	rect_bottomLeft = (rect_topLeft[0], rect_topLeft[0] + (rect_topLeft[0] - rect_bottomRight[0]))
	rect_topRight = (rect_topLeft[0] + (rect_topLeft[0] - rect_bottomRight[0]), rect_topLeft[0])
	return line_line_intersect( line0, line1, rect_topLeft, rect_topRight ) or line_line_intersect( line0, line1, rect_bottomLeft, rect_bottomRight ) or line_line_intersect( line0, line1, rect_topLeft, rect_bottomLeft ) or line_line_intersect( line0, line1, rect_topRight, rect_bottomRight ) or None

def rect_rect_intersect( self_0 : FLOAT_TUPLE, self_1 : FLOAT_TUPLE, range_0 : FLOAT_TUPLE, range_1 : FLOAT_TUPLE ) -> FLOAT_TUPLE:
	return not ( self_1[0] < range_0[0] or range_1[0] < self_0[0] or self_1[1] < range_0[1] or range_1[1] < self_0[1] )

def line_circle_intersection(circle_center : FLOAT_TUPLE, circle_radius : float, pt1 : FLOAT_TUPLE, pt2 : FLOAT_TUPLE, full_line=False, tangent_tol=1e-9):
	(p1x, p1y), (p2x, p2y), (cx, cy) = pt1, pt2, circle_center
	(x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
	dx, dy = (x2 - x1), (y2 - y1)
	dr = (dx ** 2 + dy ** 2)**.5
	big_d = x1 * y2 - x2 * y1
	discriminant = circle_radius ** 2 * dr ** 2 - big_d ** 2
	if discriminant < 0: # No intersection between circle and line
		return None
	# There may be 0, 1, or 2 intersections with the segment
	intersections = [
		(
			cx + (big_d * dy + sign * (-1 if dy < 0 else 1) * dx * discriminant**.5) / dr ** 2,
			cy + (-big_d * dx + sign * abs(dy) * discriminant**.5) / dr ** 2
		)
		for sign in ((1, -1) if dy < 0 else (-1, 1))
	] # This makes sure the order along the segment is correct
	if not full_line:  # If only considering the segment, filter out intersections that do not fall within the segment
		fraction_along_segment = [(xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy for xi, yi in intersections]
		intersections = [pt for pt, frac in zip(intersections, fraction_along_segment) if 0 <= frac <= 1]
	if len(intersections) == 2 and abs(discriminant) <= tangent_tol:  # If line is tangent to circle, return just one point (as both intersections have same location)
		return intersections[0]
	return intersections

def rect_circle_intersect( topLeft : FLOAT_TUPLE, bottomRight : FLOAT_TUPLE, center : FLOAT_TUPLE, radius : float ) -> FLOAT_TUPLE:
	cx = center[0]
	cy = center[1]
	left = topLeft[0]
	top = topLeft[1]
	right = bottomRight[0]
	bottom = bottomRight[1]
	closestX = (cx < left and left or (cx > right and right or cx))
	closestY = (cy < top and top or (cy > bottom and bottom or cy))
	dx = closestX - cx
	dy = closestY - cy
	return ( dx * dx + dy * dy ) <= (radius * radius)
