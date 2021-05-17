import numpy


class Crosquare:

	# returns line {y, b}
	@staticmethod
	def _line_from_section(section):
		k = (section[1]['y'] - section[0]['y']) / (section[1]['x'] - section[0]['x'])
		return {'k': k, 'b': section[0]['y'] - k * section[0]['x']}

	# returns f(x)
	@staticmethod
	def _line_function(line, x):
		return line['k'] * x + line['b']

	# returnes x(f)
	@staticmethod
	def _line_function_reverse(line, y):
		return (y - line['b']) / line['k']

	# returns polygon area
	@staticmethod
	def _zone(polygon):
		sum = 0
		for i in range(len(polygon) - 1):
			sum += (polygon[i]['x'] + polygon[i + 1]['x']) * (polygon[i]['y'] - polygon[i + 1]['y'])
		return sum / 2

	# returns True if points are equals, else False
	@staticmethod
	def _equal_point(point_A, point_B):
		if point_A['x'] == point_B['x'] and point_A['y'] == point_B['y']:
			return True
		else:
			return False

	# returns two sections cross point
	@staticmethod
	def _cross(section_a, section_b):
		return {
			'x': ((section_a[0]['x'] * section_a[1]['y'] - section_a[0]['y'] * section_a[1]['x']) * (section_b[0]['x'] - section_b[1]['x']) - (section_a[0]['x'] - section_a[1]['x']) * (section_b[0]['x'] * section_b[1]['y'] - section_b[0]['y'] * section_b[1]['x'])) /
			((section_a[0]['x'] - section_a[1]['x']) * (section_b[0]['y'] - section_b[1]['y']) - (section_a[0]['y'] - section_a[1]['y']) * (section_b[0]['x'] - section_b[1]['x'])),
			'y': ((section_a[0]['x'] * section_a[1]['y'] - section_a[0]['y'] * section_a[1]['x']) * (section_b[0]['y'] - section_b[1]['y']) - (section_a[0]['y'] - section_a[1]['y']) * (section_b[0]['x'] * section_b[1]['y'] - section_b[0]['y'] * section_b[1]['x'])) /
			((section_a[0]['x'] - section_a[1]['x']) * (section_b[0]['y'] - section_b[1]['y']) - (section_a[0]['y'] - section_a[1]['y']) * (section_b[0]['x'] - section_b[1]['x']))
	}

	# returns True if sections are crossing
	@staticmethod
	def _is_cross(section_a, section_b):
		line_b = Crosquare._line_from_section(section_b)
		if section_a[0]['y'] == section_a[1]['y']:
			if ((section_b[0]['y'] >= section_a[0]['y'] >= section_b[1]['y']) or (section_b[0]['y'] <= section_a[0]['y'] and section_b[1]['y'] >= section_a[0]['y'])) and 0 <= Crosquare._line_function_reverse(line_b, section_a[0]['y']) <= 1:
				return True
			else:
				return False
		elif section_a[0]['x'] == section_a[1]['x']:
			if ((section_b[0]['x'] >= section_a[0]['x'] >= section_b[1]['x']) or (section_b[0]['x'] <= section_a[0]['x'] and section_b[1]['x'] >= section_a[0]['x'])) and 0 <= Crosquare._line_function(line_b, section_a[0]['x']) <= 1:
				return True
			else:
				return False
		else:
			return False

	# returns True if point in a rectangle
	@staticmethod
	def _is_in(rectangle, point):
		if rectangle[0]['x'] == 0 and rectangle[0]['y'] == 0 and rectangle[2]['x'] == 1 and rectangle[2]['y'] == 1:
			if point['x'] > 0 and point['x'] < 1 and point['y'] > 0 and point['y'] < 1:
				return True
		elif ((point['y'] < Crosquare._line_function(Crosquare._line_from_section(( rectangle[0], rectangle[1] )), point['x']))
			and (point['y'] > Crosquare._line_function(Crosquare._line_from_section(( rectangle[3], rectangle[4] )), point['x']))
			and (point['y'] < Crosquare._line_function(Crosquare._line_from_section(( rectangle[1], rectangle[2] )), point['x']))
			and (point['y'] > Crosquare._line_function(Crosquare._line_from_section(( rectangle[2], rectangle[3] )), point['x']))):
			return True
		return False

	# return polygon vertexes count, getted from two rectangles cross
	@staticmethod
	def _quantity_of_tops(rectangle_A, rectangle_B):
		quant = 0
		for i in range(4):
			if Crosquare._is_in(rectangle_B, rectangle_A[i]):
				quant += 1
			if Crosquare._is_in(rectangle_A, rectangle_B[i]):
				quant += 1
		for i in range(4):
			for j in range(4):
				if Crosquare._is_cross(( rectangle_A[j], rectangle_A[j + 1] ), ( rectangle_B[i], rectangle_B[i + 1] )):
					quant += 1
		return quant

	def _dot_in_arr(arr, point):
		if point in arr:
			return True
		return False

	# returns angle of two sections
	@staticmethod
	def _angle_of_sections(section_a, section_b):
		dot_a = {'x': section_a.B['x'] - section_a.A['x'], 'y': section_a.B['y'] - section_a.A['y']}
		dot_b = {'x': section_b.B['x'] - section_b.A['x'], 'y': section_b.B['y'] - section_b.A['y']}
		return 180 / numpy.pi * numpy.arccos((dot_a['x'] * dot_b['x'] + dot_a['y'] * dot_b['y']) / (pow(pow(dot_a['x'], 2) + pow(dot_a['y'], 2), 0.5) * pow(pow(dot_b['x'], 2) + pow(dot_b['y'], 2), 0.5)))

	# returns angle of two points
	@staticmethod
	def _angle_dots(point_A, point_B):
		t = numpy.arctan2(point_A['y'] - point_B['y'], point_A['x'] - point_B['x']) * 180 / numpy.pi
		if t > 0:
			return 270 - t
		else:
			if t <= -90:
				return -t - 90
			else:
				return -t + 270
		return None

	# sort polygon vertexes
	@staticmethod
	def _last_convexer(polygon):
		polygon_len = len(polygon)
		point_t = []
		point_t.append(polygon[0])
		for i in range(1, polygon_len):
			point_t.append({ 'x': 10, 'y': 10 })
		for i in range(1, polygon_len):
			if polygon[i]['x'] < point_t[0]['x']:
				point_t[0] = polygon[i]
		for i in range(1, polygon_len):
			for j in range(polygon_len):
				if not Crosquare._dot_in_arr(point_t, polygon[j]):
					a = polygon[j]
					point_t[i] = a
			for j in range(polygon_len):
				if Crosquare._angle_dots(point_t[i - 1], polygon[j]) < Crosquare._angle_dots(point_t[i - 1], point_t[i]) and not Crosquare._dot_in_arr(point_t, polygon[j]):
					point_t[i] = polygon[j]
		for i in range(polygon_len):
			polygon[i] = point_t[i]
		polygon.append(point_t[0])
		return None

	# rotate point avoid mainPoint
	@staticmethod
	def _rotate_dot(main_point, point, angle):
		point_t = { 'x': point['x'] - main_point['x'], 'y': point['y'] - main_point['y'] }
		angle_t = numpy.pi / 180 * angle
		return {'x': point_t['x'] * numpy.cos(angle_t) + point_t['y'] * numpy.sin(angle_t) + main_point['x'],'y': -point_t['x'] * numpy.sin(angle_t) + point_t['y'] * numpy.cos(angle_t) + main_point['y'] }

	# creates rectangle with main_point, angle and model_length
	@staticmethod
	def _set_sqr(main_point, angle, model_length):
		rec = []
		rec.append({'x': main_point['x'] - 0.5, 'y': main_point['y'] - 0.5})
		rec[0] = Crosquare._rotate_dot(main_point, rec[0], angle)
		rec.append({'x': main_point['x'] - 0.5, 'y': main_point['y'] + 0.5})
		rec[1] = Crosquare._rotate_dot(main_point, rec[1], angle)
		rec.append({'x': main_point['x'] + 0.5 + model_length, 'y': main_point['y'] + 0.5})
		rec[2] = Crosquare._rotate_dot(main_point, rec[2], angle)
		rec.append({'x': main_point['x'] + 0.5 + model_length, 'y': main_point['y'] - 0.5})
		rec[3] = Crosquare._rotate_dot(main_point, rec[3], angle)
		rec.append(rec[0])
		return rec

	# returns polygon from rectangles crosses
	@staticmethod
	def _fill_polygon(rectangle_0, rectangle_1):
		polygon = []
		for i in range(4):
			if Crosquare._is_in(rectangle_1, rectangle_0[i]):
				polygon.append(rectangle_0[i])
			if Crosquare._is_in(rectangle_0, rectangle_1[i]):
				polygon.append(rectangle_1[i])
		for i in range(4):
			for j in range(4):
				if Crosquare._is_cross(( rectangle_0[j], rectangle_0[j + 1] ), ( rectangle_1[i], rectangle_1[i + 1] )):
					polygon.append(Crosquare._cross(( rectangle_0[j], rectangle_0[j + 1] ), ( rectangle_1[i], rectangle_1[i + 1] )))
		return polygon

	# returns rectangles cross area
	@staticmethod
	def _zone_zero_angle(main_point, length):
		if main_point['y'] >= 1.5 or main_point['y'] <= -0.5 or main_point['x'] >= 1.5 or main_point['x'] + length <= -0.5:
			return 0
		else:
			S = 1
			S *= (1 - abs(main_point['y'] - 0.5))
			if main_point['x'] > 0.5:
				S *= (1.5 - main_point['x'])
			if main_point['x'] + length < 0.5:
				S *= 0.5 + main_point['x'] + length
		return S

	@staticmethod
	def calc(main_point, angle, model_length):
		rectangle_0 = ( {'x': 0,'y': 0}, {'x': 0,'y': 1}, {'x': 1,'y': 1}, {'x': 1,'y': 0}, {'x': 0,'y': 0} )

		if (angle == 0):
			return Crosquare._zone_zero_angle(main_point, model_length)
		else:
			rectangle_1 = Crosquare._set_sqr(main_point, angle, model_length)
			tops = Crosquare._quantity_of_tops(rectangle_0, rectangle_1)
			if (tops == 0):
				return 0
			else:
				polygon = Crosquare._fill_polygon(rectangle_0, rectangle_1)
				Crosquare._last_convexer(polygon)
				result = Crosquare._zone(polygon)
				return result
		return 0

