
from math import ceil
from os import path as os_path
from sys import path as sys_path
from typing import Union

FLOAT_TUP = tuple[float, float]

FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))
sys_path.append( os_path.join(FILE_DIRECTORY, "../") )

from geometry import Intersect
from geometry.Rectangle import Rectangle
from geometry.Point import Point
from geometry.Circle import Circle
from geometry.LineSegment import LineSegment
from mathlib import QuadTree

sys_path.pop()

class Agent(Circle):
	vx = vy = 0 # velocity
	rad = 0 # current facing angle
	turn_rad = 0 # delta turn angle
	def __init__(self, x, y, radius):
		super().__init__(x, y, radius)

class Simulation:
	__objects = []
	__agents = []

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

	def step_physics(self):
		# for agent in self.__agents:
		# 	break
		pass

	def __construct_quad_trees(self) -> None:
		bounds = Rectangle(0, 0, self.__simulation_bounds[0], self.__simulation_bounds[1])

		self.__objects_quadtree = QuadTree.QuadTree(boundary=bounds)
		self.__objects_quadtree.insert_array(self.__objects)

		self.__agent_quadtree = QuadTree.QuadTree(boundary=bounds)
		self.__agent_quadtree.insert_array(self.__agents)

	def __init__(self, simulation_bounds=(1280, 720)):
		self.__simulation_bounds = ( int(simulation_bounds[0]), int(simulation_bounds[1]) )
		self.__construct_quad_trees()
