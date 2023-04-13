import math

class Vector2:
	def __init__(self, x, y):
		self.x, self.y = x, y

	def __str__(self) -> str:
		return f"{self.x}i + {self.y}j"

	def __repr__(self) -> str:
		return repr((self.x, self.y))

	def dot(self, other) -> float:
		if not isinstance(other, Vector2):
			raise TypeError('Can only take dot product of two Vector2 objects')
		return self.x * other.x + self.y * other.y
	__matmul__ = dot

	def __sub__(self, other):
		return Vector2(self.x - other.x, self.y - other.y)

	def __add__(self, other):
		return Vector2(self.x + other.x, self.y + other.y)

	def __mul__(self, scalar):
		if isinstance(scalar, int) or isinstance(scalar, float):
			return Vector2(self.x*scalar, self.y*scalar)
		raise NotImplementedError('Can only multiply Vector2 by a scalar')

	def __rmul__(self, scalar):
		return self.__mul__(scalar)

	def __neg__(self):
		return Vector2(-self.x, -self.y)

	def __truediv__(self, scalar):
		return Vector2(self.x / scalar, self.y / scalar)

	def __mod__(self, scalar):
		return Vector2(self.x % scalar, self.y % scalar)

	def magnitude(self) -> float:
		return math.sqrt(self.x**2 + self.y**2)

	def unit(self, epsilon=1e-3):
		m = self.magnitude()
		if m < epsilon:
			m = epsilon
		return Vector2(self.x / m, self.y / m) 

	def reflect(self, normal):
		return self - ( normal * ( self.dot(normal) * 2.0) )

	def __abs__(self) -> float:
		return self.magnitude()

	def distance_to(self, other) -> float:
		return abs(self - other)

	def to_polar(self) -> tuple[float, float]:
		return self.magnitude(), math.atan2(self.y, self.x)
