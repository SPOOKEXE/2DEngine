
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
from mathlib import QuadTree, Mathf

sys_path.pop()

class Agent(Circle):
	speed = 1 # speed
	rad = 0 # current facing angle
	turn_rad = 0 # delta turn angle
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
			vx, vy = Mathf.AngleToVector(agent.rad)
			speed_delta = agent.speed * delta_time
			agent.x += vx * speed_delta
			agent.y += vy * speed_delta
			if wrap_bounds:
				self._check_bounds_wrap(agent)
		# bounce off each other, separate positions, reflect direction
		# for agent in self.get_agents():
		# 	# for each nearby agents
		# 	nearby = self.__agent_quadtree.query( agent, None )
		# 	# if no nearby, ignore altogether
		# 	if len(nearby) == 0:
		# 		continue
		# 	for near in nearby:
		# 		tangentVector = array(-(near.x - agent.x), near.y - agent.y)

		# 		mag = sqrt( tangentVector[0] ** 2 + tangentVector[1] ** 2 )
		# 		if mag < epsilon_v:
		# 			mag = epsilon_v
		# 		tangentVector = (tangentVector[0] / mag, tangentVector[1] / mag)

		# 		c2_d_x, c2_d_y = Mathf.AngleToVector(near.rad)
		# 		c1_d_x, c1_d_y = Mathf.AngleToVector(agent.rad)

		# 		c2_v_x = c2_d_x * near.speed
		# 		c2_v_y = c2_d_y * near.speed

		# 		c1_v_x = c1_d_x * near.speed
		# 		c1_v_y = c1_d_y * near.speed

		# 		relativeVelocity = array( c2_v_x-c1_v_x, c2_v_y-c1_v_y )
		# 		length = relativeVelocity.dot(tangentVector)
		# 		velocityComponentOnTangent = tangentVector * length
		# 		velocityComponentPerpendicularToTangent = relativeVelocity - velocityComponentOnTangent

		# 		c1_v_x -= velocityComponentPerpendicularToTangent[0]
		# 		c2_v_x -= velocityComponentPerpendicularToTangent[0]

		# 		c1_v_y -= velocityComponentPerpendicularToTangent[1]
		# 		c2_v_y -= velocityComponentPerpendicularToTangent[1]

		# 		circle1.Velocity.X -= velocityComponentPerpendicularToTangent.X
		# 		circle1.Velocity.Y -= velocityComponentPerpendicularToTangent.Y
		# 		circle2.Velocity.X += velocityComponentPerpendicularToTangent.X
		# 		circle2.Velocity.Y += velocityComponentPerpendicularToTangent.Y

	def __construct_quad_trees(self) -> None:
		bounds = Rectangle(0, 0, self.__simulation_bounds[0], self.__simulation_bounds[1])

		self.__objects_quadtree = QuadTree.QuadTree(boundary=bounds)
		self.__objects_quadtree.insert_array(self.__objects)

		self.__agent_quadtree = QuadTree.QuadTree(boundary=bounds)
		self.__agent_quadtree.insert_array(self.__agents)

	def __init__(self, simulation_bounds=(1280, 720)):
		self.__simulation_bounds = ( int(simulation_bounds[0]), int(simulation_bounds[1]) )
		self.__construct_quad_trees()
