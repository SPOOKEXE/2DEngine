
import pygame
import Intersect

from os import path as os_path
from sys import path as sys_path

# FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))
# sys_path.append( os_path.join(FILE_DIRECTORY, "../") )

# from mathlib import QuadTree

# sys_path.pop()

def dist_sqrd(x0, y0, x1, y1) -> float:
	dx = x1 - x0
	dy = y1 - y0
	return (dx * dx) + (dy * dy)

class Object:
	zIndex = 0
	x = y = 0
	vx = vy = 0
	def step(self, delta : float):
		self.x += (self.vx * delta)
		self.y += (self.vy * delta)
	def isA(self, _class) -> bool:
		return self.__class__ == _class or issubclass(self.__class__, _class)
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Square(Object):
	w = h = 1
	def __init__(self, x, y, w, h):
		super().__init__(x, y)
		self.w = w
		self.h = h

class Circle(Object):
	radius = 1
	def __init__(self, x, y, radius):
		super().__init__(x, y)
		self.radius = radius

class Agent(Circle):
	brain_uuid = None
	def __init__(self, x, y, radius):
		super().__init__(x, y, radius)

class SimulationMethods:

	@staticmethod
	def raycast( object_array : list[Object], ox, oy, dx, dy ):
		hit = point = None
		dist = -1
		start_p = (ox, oy)
		finish_p = (ox + dx, oy + dy)
		def check_closest(hitt, pointt):
			nonlocal hit, dist, point
			distt = dist_sqrd( start_p[0], start_p[1], pointt[0], pointt[1] )
			if (hit == None) or (distt < dist):
				hit = hitt
				dist = distt
				point = pointt
		for obj in object_array:
			if obj.isA( Square ):
				ix, iy = Intersect.line_rect_intersect( start_p, finish_p, (obj.x, obj.y), (obj.x + obj.w, obj.y + obj.h) )
				if ix != None:
					check_closest(obj, (ix, iy))
			elif obj.isA( Circle ):
				dat = Intersect.line_circle_intersection( (obj.x, obj.y), obj.radius, start_p, finish_p )
				if dat != None:
					check_closest(obj, type(dat) == list and dat[0] or dat)
		return hit, dist, point

	@staticmethod
	def get_circle_collisions(objects : list[Object], ref : Circle) -> list[Object]:
		intersecting = []
		for objectt in objects:
			if ref == objectt:
				continue
			if objectt.isA( Circle ) and Intersect.circle_circle_intersect( (ref.x, ref.y), ref.radius, (objectt.x, objectt.y), objectt.radius ):
				intersecting.append( objectt )
			if objectt.isA( Square ) and Intersect.rect_circle_intersect( (objectt.x, objectt.y), (objectt.x + objectt.w, objectt.y + objectt.h), (ref.x, ref.y), ref.radius ):
				intersecting.append( objectt )
		return intersecting

	@staticmethod
	def get_rect_collisions( objects : list[Object], ref : Square ) -> list[Object]:
		intersecting = []
		for objectt in objects:
			if ref == objectt:
				continue
			if objectt.isA( Circle ):
				if Intersect.rect_circle_intersect( (ref.x, ref.y), (ref.x + ref.w, ref.y + ref.h), (objectt.x, objectt.y), objectt.radius ):
					intersecting.append( objectt )
			elif objectt.isA( Square ):
				if Intersect.rect_rect_intersect( (ref.x, ref.y), (ref.x + ref.w, ref.y + ref.h), (objectt.x, objectt.y), (objectt.x + objectt.w, objectt.y + objectt.h) ):
					intersecting.append( objectt )
		return intersecting

class Simulation:
	_objects : list[Object] = []
	boundaries : list[Object] = []
	
	agents : list[Agent] = []
	#quad_tree : QuadTree = QuadTree.QuadTree( boundary=QuadTree.Rectangle(0, 0, 1280, 720) )
	#agent_to_quadtree_point = { }
	# point = QuadTree.Point(agent.x, agent.y, agent)
	# self.agent_to_quadtree_point[agent] = point
	# for agent, p in self.agent_to_quadtree_point.values():
	# 	p.x = agent.x
	# 	p.y = agent.y

	def __append_object(self, obj : Object):
		self._objects.append(obj)

	def append_boundary(self, obj : Object):
		self.__append_object(obj)
		self.boundaries.append(obj)

	def append_agent(self, agent : Agent):
		self.__append_object(agent)
		self.agents.append(agent)

	def __extend_object(self, objects : list[Object]):
		self._objects.extend(objects)

	def extend_boundary(self, objects : list[Object]):
		self.__extend_object(objects)
		self.boundaries.extend(objects)

	def extend_agent(self, objects : list[Object]):
		self.__extend_object(objects)
		self.agents.extend(objects)

	def get_agents(self) -> list[Agent]:
		return self.agents

	def step_simulation(self, delta_time : float):
		for agent in self.agents:
			agent.step(delta_time)

	def get_collisions(self, obj : Object) -> list[Object]:
		if obj.isA(Circle):
			return SimulationMethods.get_circle_collisions(self._objects, obj)
		return SimulationMethods.get_rect_collisions(self._objects, obj)

	def raycast(self, ox, oy, dx, dy) -> Object:
		return SimulationMethods.raycast(self._objects, ox, oy, dx, dy)

	def __init__(self):
		pass

if __name__ == '__main__':

	from random import randint

	resolution_tuple = (1280, 720)
	total_boundaries = 100
	total_agent = 20

	sim = Simulation()
	sim.extend_boundary([
		Square(
			randint(0, resolution_tuple[0] - 50),
			randint(0, resolution_tuple[1] - 50),
			randint(5, 50), randint(5, 50)
		) for _ in range(total_boundaries)
	])

	sim.extend_agent([
		Agent(randint(0, resolution_tuple[0] - 50), randint(0, resolution_tuple[0] - 50), randint(5, 30)) for _ in range(total_agent)
	])

	import pygame

	BLACK_COLOR_CONST = pygame.colordict.THECOLORS['black']
	WHITE_COLOR_CONST = pygame.colordict.THECOLORS['white']

	pygame.init()
	screen = pygame.display.set_mode(resolution_tuple)
	clock = pygame.time.Clock()

	delta = 0
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		screen.fill(BLACK_COLOR_CONST)

		# UPDATE ENTITIES IN THE GAME
		sim.step_simulation(delta)

		# RENDER YOUR GAME HERE
		def render_objects(array_of_objects, color=WHITE_COLOR_CONST):
			for obj in array_of_objects:
				if obj.isA( Square ):
					pygame.draw.rect(screen, color, pygame.Rect( obj.x, obj.y, obj.w, obj.h ))
				elif obj.isA( Circle ):
					pygame.draw.circle( screen, color, (obj.x, obj.y), obj.radius )

		render_objects(sim.boundaries)
		render_objects(sim.agents, color=pygame.colordict.THECOLORS['aqua'])

		intersects = []
		for obj in sim._objects:
			if intersects.count(obj) != 0:
				continue
			items = sim.get_collisions( obj )
			if len(items) > 0:
				intersects.extend( items )
				intersects.append( obj )
		render_objects(intersects, color=pygame.colordict.THECOLORS['burlywood'])

		pygame.display.flip()
		delta = clock.tick(60)

	pygame.quit()