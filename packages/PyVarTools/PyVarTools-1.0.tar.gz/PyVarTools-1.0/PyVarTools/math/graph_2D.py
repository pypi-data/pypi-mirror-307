import numpy
from typing import Any, Literal
#
#
#
#
class GraphPoint:
	def __init__(self, x: int | float, y: int | float):
		self.x = x
		self.y = y
	#
	#
	#
	#
	def __str__(self):
		x_string = ("%.4f" % self.x) if type(self.x) == float else str(self.x)
		y_string = ("%.4f" % self.y) if type(self.y) == float else str(self.y)

		return f"({x_string}, {y_string})"
	#
	#
	#
	#
	def __repr__(self):
		return str(self)
#
#
#
#
def calculate_angle_degree(start_point: GraphPoint, end_point: GraphPoint):
	if start_point.y == end_point.y:
		return 0.0
	else:
		tanh = (end_point.y - start_point.y) / (end_point.x - start_point.x)
		return numpy.degrees(numpy.arctan(tanh))
#
#
#
#
class GraphSection:
	def __init__(self, points: list[GraphPoint], angle_sensitivity: float = 0.0):
		if angle_sensitivity < 0.0:
			raise ValueError("angle_sensitivity must be >= 0.0")
		#
		#
		#
		#
		self.points = points
		self.angle_sensitivity = angle_sensitivity
		self.min = min(points, key=lambda point: point.y)
		self.max = max(points, key=lambda point: point.y)
		self.average = numpy.mean([point.y for point in self.points]).item()
	#
	#
	#
	#
	def __str__(self):
		min_string = ("%.4f" % self.min) if type(self.min) == float else str(self.min)
		max_string = ("%.4f" % self.max) if type(self.max) == float else str(self.max)
		average_string = ("%.4f" % self.average) if type(self.average) == float else str(self.average)

		return f"{self.points} (num_points: {len(self.points)}, min: {min_string}, max: {max_string}, average: {average_string}, direction: {self.get_direction()})"
	#
	#
	#
	#
	def __repr__(self):
		return str(self)
	#
	#
	#
	#
	def calculate_average(self):
		self.average = numpy.mean([point.y for point in self.points]).item()
	#
	#
	#
	#
	def add(self, point: GraphPoint):
		self.points.append(point)

		if point.y < self.min.y:
			self.min = point

		if point.y > self.max.y:
			self.max = point

		self.calculate_average()
	#
	#
	#
	#
	def get_angle_degree(self):
		if len(self.points) >= 2:
			return calculate_angle_degree(self.points[0], self.points[-1])
		else:
			return None
	#
	#
	#
	#
	def get_direction(self):
		if len(self.points) >= 2:
			angle = calculate_angle_degree(self.points[0], self.points[-1])

			if angle > self.angle_sensitivity:
				return "increasing"
			elif angle < -self.angle_sensitivity:
				return "decreasing"
			else:
				return "straight"
		else:
			return None
	#
	#
	#
	#
	def get_graph_points_after_max(self):
		return self.points[self.points.index(self.max):]
	#
	#
	#
	#
	def get_graph_points_after_min(self):
		return self.points[self.points.index(self.min):]
	#
	#
	#
	#
	def remove_point_after_max(self):
		self.points = self.points[:self.points.index(self.max) + 1]
		self.calculate_average()
	#
	#
	#
	#
	def remove_point_after_min(self):
		self.points = self.points[:self.points.index(self.min) + 1]
		self.calculate_average()
#
#
#
#
class ThresholdSensitivity:
	def __init__(
			self,
			threshold_sensitivity: float = 0.0,
			type_: Literal["absolute", "relative"] = "absolute"
	):
		if type_ not in ["absolute", "relative"]:
			raise ValueError("type_ must be \"absolute\" or \"relative\"")
		#
		#
		#
		#
		self.threshold_sensitivity = threshold_sensitivity
		self.type_ = type_
	#
	#
	#
	#
	def get_decrease_sensitive_point(self, point: GraphPoint | int | float):
		decrease_sensitive_point = point.y if isinstance(point, GraphPoint) else point

		if self.type_ == "absolute":
			return decrease_sensitive_point - self.threshold_sensitivity

		if self.type_ == "relative":
			return decrease_sensitive_point * (1 - self.threshold_sensitivity)
	#
	#
	#
	#
	def get_increase_sensitive_point(self, point: GraphPoint | int | float):
		increase_sensitive_point = point.y if isinstance(point, GraphPoint) else point

		if self.type_ == "absolute":
			return increase_sensitive_point + self.threshold_sensitivity

		if self.type_ == "relative":
			return increase_sensitive_point * (1 + self.threshold_sensitivity)
#
#
#
#
class Graph:
	def __init__(self, points: list[GraphPoint] = None):
		if points is not None:
			self.points = points
			self.min = min(points, key=lambda point: point.y)
			self.max = max(points, key=lambda point: point.y)
			self.average = numpy.mean([point.y for point in self.points]).item()
		else:
			self.points = []
			self.min = None
			self.max = None
			self.average = None
	#
	#
	#
	#
	def __str__(self):
		min_string = ("%.4f" % self.min) if type(self.min) == float else str(self.min)
		max_string = ("%.4f" % self.max) if type(self.max) == float else str(self.max)
		average_string = ("%.4f" % self.average) if type(self.average) == float else str(self.average)

		return f"(num_points: {len(self.points)}, min: {min_string}, max: {max_string}, average: {average_string})"
	#
	#
	#
	#
	def __repr__(self):
		return str(self)
	#
	#
	#
	#
	def calculate_average(self):
		self.average = numpy.mean([point.y for point in self.points]).item()
	#
	#
	#
	#
	def add(self, point: GraphPoint):
		self.points.append(point)

		if self.min is None or point.y < self.min.y:
			self.min = point

		if self.max is None or point.y > self.max.y:
			self.max = point

		self.calculate_average()
	#
	#
	#
	#
	def get_sections(
			self,
			threshold_sensitivity: ThresholdSensitivity = ThresholdSensitivity(),
			angle_sensitivity: float = 0.0,
			counter: Any = None
	):
		graph_section = None

		for i in range(len(self.points)):
			if graph_section is None:
				graph_section = GraphSection([self.points[i]], angle_sensitivity)
			else:
				direction = graph_section.get_direction()

				if direction is None:
					graph_section.add(self.points[i])
				elif direction == "increasing":
					if self.points[i].y > threshold_sensitivity.get_decrease_sensitive_point(graph_section.max):
						graph_section.add(self.points[i])
					else:
						start_of_new_section = graph_section.get_graph_points_after_max()
						graph_section.remove_point_after_max()

						yield graph_section

						graph_section = GraphSection(start_of_new_section + [self.points[i]], angle_sensitivity)
				elif direction == "decreasing":
					if self.points[i].y < threshold_sensitivity.get_increase_sensitive_point(graph_section.min):
						graph_section.add(self.points[i])
					else:
						start_of_new_section = graph_section.get_graph_points_after_min()
						graph_section.remove_point_after_min()

						yield graph_section

						graph_section = GraphSection(start_of_new_section + [self.points[i]], angle_sensitivity)
				elif direction == "straight":
					if self.points[i].y < threshold_sensitivity.get_increase_sensitive_point(graph_section.average) or self.points[i].y > threshold_sensitivity.get_decrease_sensitive_point(graph_section.average):
						graph_section.add(self.points[i])
					else:
						yield graph_section
						graph_section = GraphSection([self.points[i]], angle_sensitivity)

			if counter is not None:
				counter.step()

		yield graph_section
