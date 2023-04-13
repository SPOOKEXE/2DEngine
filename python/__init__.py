
from simulation.Simulation import Simulation, Agent

from geometry.Rectangle import Rectangle
from geometry.Point import Point
from geometry.Circle import Circle
from geometry.LineSegment import LineSegment

from random import randint
from math import pi
from PIL import Image, ImageDraw

SIMULATION_SIZE = (1280, 720)
TOTAL_AGENTS = 100
SPAWN_PADDING = 10

# generate a bunch of agents
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

# generate a visualization of the simulation
def DrawOnImage( image : Image.Image, shapes : list ) -> None:
	draw = ImageDraw.Draw(image, "RGB")
	for shape in shapes:
		if issubclass(shape.__class__, Circle):
			hr = int(shape.radius / 2)
			draw.ellipse( (shape.x - hr, shape.y - hr, shape.x + hr, shape.y + hr), fill=(200,255,255) )
		elif issubclass(shape.__class__, Rectangle):
			draw.rectangle( (shape.x, shape.y, shape.x + shape.w, shape.y + shape.h), fill=(255,255,200) )
		elif issubclass(shape.__class__, Point):
			draw.point( (shape.x, shape.y), fill=(255,0,255) )
		elif issubclass(shape.__class__, LineSegment):
			draw.line( (shape.x0, shape.y0, shape.x1, shape.y1), fill=(255,0,0) )
	return image

def GeneratePreview():
	preview_image = Image.new("RGB", SIMULATION_SIZE, (0,0,0))
	DrawOnImage( preview_image, agentz )

	# raycast into the agents
	ray_segment = LineSegment(0, 0, SIMULATION_SIZE[0], SIMULATION_SIZE[1])
	hit, dist, point = sim.raycast_agents( ray_segment )

	# generate a visualization of the raycast
	DrawOnImage( preview_image, [ray_segment] )

	# visualize the raycast result
	print(hit)
	if hit != None:
		print(hit.x, hit.y, point[0], point[1], hit)
		notif = Circle(point[0] - 3, point[1] - 3, 6)
		draw = ImageDraw.Draw(preview_image, "RGB")
		draw.ellipse( (point[0], point[1], point[0] + 5, point[1] + 5), fill=(0,255,0) )

	preview_image.show("PREVIEW")
	preview_image.close()

if __name__ == '__main__':

	import pygame

	BLACK_COLOR_CONST = pygame.colordict.THECOLORS['black']
	WHITE_COLOR_CONST = pygame.colordict.THECOLORS['white']

	pygame.init()
	screen = pygame.display.set_mode( SIMULATION_SIZE )
	clock = pygame.time.Clock()

	time_scale = 0.1
	delta_actual = 0
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		screen.fill(BLACK_COLOR_CONST)

		# UPDATE ENTITIES IN THE GAME
		sim.step_physics(delta_actual)

		# RENDER YOUR GAME HERE
		def render_objects(array_of_objects, color=WHITE_COLOR_CONST):
			for obj in array_of_objects:
				if issubclass( obj.__class__, Rectangle ):
					pygame.draw.rect(screen, color, pygame.Rect( obj.x, obj.y, obj.w, obj.h ))
				elif issubclass( obj.__class__, Circle ):
					pygame.draw.circle( screen, color, (obj.x, obj.y), obj.radius )

		render_objects(sim.get_agents(), color=pygame.colordict.THECOLORS['aqua'])

		pygame.display.flip()
		delta_actual = clock.tick(165) * time_scale

	pygame.quit()

