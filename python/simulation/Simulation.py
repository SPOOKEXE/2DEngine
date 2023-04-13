
from math import cos, sin, sqrt
from numpy import array, ndarray
from typing import Union
from os import path as os_path
from sys import path as sys_path

FLOAT_TUP = tuple[float, float]

FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))
sys_path.append( os_path.join(FILE_DIRECTORY, "../") )

from geometry import Intersect
from geometry.Rectangle import Rectangle
from geometry.Point import Point
from geometry.Circle import Circle
from geometry.LineSegment import LineSegment
from mathlib.Vector2 import Vector2
from mathlib import QuadTree

sys_path.pop()

class Agent(Circle):
	speed = 1 # speed
	vel = Vector2(0,0)
	def __init__(self, x, y, radius):
		super().__init__(x, y, radius)

class Simulation:
	__objects = []
	__agents : list[Agent] = []

	__simulation_bounds = None
	__agent_quadtree = None
	__objects_quadtree = None

	def get_objects(self) -> list:
		return self.__objects

	def get_agents(self) -> list:
		return self.__agents

	def get_simulation_bounds(self) -> tuple[int, int]:
		return self.__simulation_bounds
	
	def get_agent_quad_tree(self) -> QuadTree.QuadTree:
		return self.__agent_quadtree
	
	def get_object_quad_tree(self) -> QuadTree.QuadTree:
		return self.__objects_quadtree

	def append_object(self, obj) -> None:
		self.__objects.append(obj)
		self.__objects_quadtree.insert_single(obj)
	
	def bulk_append_objects(self, objects : list) -> None:
		self.__objects.extend(objects)
		self.__objects_quadtree.ins

	def append_agent(self, agent) -> None:
		self.__agents.append(agent)
		self.__agent_quadtree.insert_single(agent)

	def bulk_append_agents(self, agents : list) -> None:
		self.__agents.extend(agents)
		self.__agent_quadtree.insert_array(agents)

	def get_agent_tree_collisions(self, ref : QuadTree.QD_RANGE_COMPONENTS) -> list[QuadTree.QD_T_COMPONENTS]:
		return self.__agent_quadtree.query(ref)

	def get_object_tree_collisions(self, ref : QuadTree.QD_RANGE_COMPONENTS) -> list[QuadTree.QD_T_COMPONENTS]:
		return self.__objects_quadtree.query(ref)

	def raycast_objects( self, line_seg : LineSegment ):
		return self.__objects_quadtree.brute_raycast( line_seg )
	
	def raycast_agents( self, line_seg : LineSegment ):
		return self.__agent_quadtree.brute_raycast( line_seg )

	def _check_bounds_wrap(self, agent):
		if agent.x < 0:
			agent.x = self.__simulation_bounds[0]
		elif agent.x > self.__simulation_bounds[0]:
			agent.x = 0
		if agent.y < 0:
			agent.y = self.__simulation_bounds[1]
		elif agent.y > self.__simulation_bounds[1]:
			agent.y = 0

	def step_physics(self, delta_time : float, wrap_bounds=True, epsilon_v = 1e-3):
		# step physics
		for agent in self.__agents:
			speed_delta = agent.speed * delta_time
			agent.x += agent.vel.x * speed_delta
			agent.y += agent.vel.y * speed_delta
			if wrap_bounds:
				self._check_bounds_wrap(agent)

		# bounce off each other, separate positions, reflect direction
		for agent in self.get_agents():
			nearby = self.__agent_quadtree.query( Circle(agent.x, agent.y, agent.radius), None )
			if len(nearby) == 0:
				continue
			for near in nearby:

				midpoint = Vector2( (near.x + agent.x) / 2, (near.y + agent.y) / 2 )
				delta = Vector2(near.x - agent.x, near.y - agent.y)

				dist = delta.magnitude()
				if dist < 1e-3:
					dist = 1e-3
				agent.x = midpoint.x - (agent.radius * delta.x) / dist
				agent.y = midpoint.y - (agent.radius * delta.y) / dist
				near.x = midpoint.x + (near.radius * delta.x) / dist
				near.y = midpoint.y + (near.radius * delta.y) / dist

				agent.vel *= -1
				near.vel *= -1
				# normal = delta.unit()
				# agent.vel = agent.vel.reflect(normal).unit()
				# near.vel = near.vel.reflect(normal).unit()

	def __construct_quad_trees(self) -> None:
		bounds = Rectangle(0, 0, self.__simulation_bounds[0], self.__simulation_bounds[1])

		self.__objects_quadtree = QuadTree.QuadTree(boundary=bounds)
		self.__objects_quadtree.insert_array(self.__objects)

		self.__agent_quadtree = QuadTree.QuadTree(boundary=bounds)
		self.__agent_quadtree.insert_array(self.__agents)

	def __init__(self, simulation_bounds=(1280, 720)):
		self.__simulation_bounds = ( int(simulation_bounds[0]), int(simulation_bounds[1]) )
		self.__construct_quad_trees()
