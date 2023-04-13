
from simulation.Simulation import Simulation, Agent, LineSegment

from random import randint
from math import pi

from PIL import Image, ImageDraw, ImageColor

SIMULATION_SIZE = (1280, 720)
TOTAL_AGENTS = 100
SPAWN_PADDING = 50

agentz = []

for _ in range(TOTAL_AGENTS):
	rX = randint(SPAWN_PADDING, SIMULATION_SIZE[0] - SPAWN_PADDING)
	rY = randint(SPAWN_PADDING, SIMULATION_SIZE[1] - SPAWN_PADDING)
	rRadius = int( randint(50, 100)/10 )
	
	agent = Agent( rX, rY, rRadius )
	agent.vx = randint(-100, 100) / 100
	agent.vy = randint(-100, 100) / 100
	agent.rad = (randint( 1, 360 ) / 360) * pi

	agentz.append(agent)

# append a ton of agents
sim = Simulation(simulation_bounds=SIMULATION_SIZE)
sim.bulk_append_agents(agentz)

# raycast into the agents
ray_segment = LineSegment(0, 0, SIMULATION_SIZE[0], SIMULATION_SIZE[1])
result = sim.raycast_agents( ray_segment )
print(result)

# generate a visualization of it
from simulation.Visual import VisualMethods

preview_image = Image.new("RGB", SIMULATION_SIZE, (0,0,0))
VisualMethods.DrawOnImage( preview_image, agentz )
VisualMethods.DrawOnImage( preview_image, [ray_segment] )

preview_image.show("PREVIEW")
