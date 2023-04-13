
from PIL import Image, ImageDraw, ImageColor
from os import path as os_path
from sys import path as sys_path

FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))
sys_path.append( os_path.join(FILE_DIRECTORY, "../") )

from geometry.Rectangle import Rectangle
from geometry.Point import Point
from geometry.Circle import Circle
from geometry.LineSegment import LineSegment

sys_path.pop()

class VisualMethods:

	@staticmethod
	def DrawOnImage( image : Image.Image, shapes : list ) -> None:
		draw = ImageDraw.Draw(image, "RGB")
		for shape in shapes:
			if issubclass(shape.__class__, Circle):
				draw.ellipse( (shape.x, shape.y, shape.x + shape.radius, shape.y + shape.radius), fill=(200,255,255) )
			elif issubclass(shape.__class__, Rectangle):
				draw.rectangle( (shape.x, shape.y, shape.x + shape.w, shape.y + shape.h), fill=(255,255,200) )
			elif issubclass(shape.__class__, Point):
				draw.point( (shape.x, shape.y), fill=(255,0,255) )
			elif issubclass(shape.__class__, LineSegment):
				draw.line( (shape.x0, shape.y0, shape.x1, shape.y1), fill=(255,0,0) )
		return image
