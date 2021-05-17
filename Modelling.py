import numpy
from Crosquare import Crosquare

class Modelling:
	
	@staticmethod
	def _print_matrix(matrix):
		print(numpy.transpose(matrix))

	@staticmethod
	def _model_to_matrix(model_len, angle):
		matrix_len = int(model_len * 4 + 1) + 4
		main_point = {'x': matrix_len // 2, 'y': matrix_len // 2}
		matrix = numpy.empty([matrix_len, matrix_len])
		matrix[0:matrix_len][0:matrix_len] = 0
		for y in range(matrix_len):
			for x in range(matrix_len):
				matrix[x][y] = Crosquare.calc({'x': main_point['x'] + 0.5 - x, 'y': main_point['y'] + 0.5 - y}, angle, model_len) / (model_len + 1)
		return matrix, main_point

	@staticmethod
	def _get_crop_parameters(matrix):
		clear = False
		width = 0
		height = 0
		x_first = 0
		y_first = 0
		matrix_len = len(matrix)
		for row in range(matrix_len - 1, -1, -1):
			clear = True
			for col in range(matrix_len - 1, -1, -1):
				if matrix[col][row] > 0:
					clear = False
					y_first = row
			if not clear:
				height += 1
		for col in range(matrix_len - 1, -1, -1):
			clear = True
			for row in range(matrix_len - 1, -1, -1):
				if matrix[col][row] > 0:
					clear = False
					x_first = col
			if not clear:
				width += 1
		return {'width': width, 'height': height, 'x_first': x_first, 'y_first': y_first}

	@staticmethod
	def _crop_matrix(matrix, crop_parameters):
		cropped_matrix = numpy.empty([crop_parameters['width'], crop_parameters['height']])
		for col in range(crop_parameters['width']):
			for row in range(crop_parameters['height']):
				cropped_matrix[col][row] = matrix[col + crop_parameters['x_first']][row + crop_parameters['y_first']]
		return cropped_matrix

	@staticmethod
	def _get_low_angle_model(model_len, angle):
		matrix, main_point = Modelling._model_to_matrix(model_len, angle)
		matrix_len = len(matrix)
		crop_parameters = Modelling._get_crop_parameters(matrix)
		main_point['x'] -= crop_parameters['x_first']
		main_point['y'] -= crop_parameters['y_first']
		shift_model = {'main_point': main_point, 'matrix': None}
		shift_model['matrix'] = Modelling._crop_matrix(matrix, crop_parameters)
		return shift_model

	@staticmethod
	def _rotate_shift_model(shift_model):
		shift_model['matrix'] = numpy.rot90(shift_model['matrix'], 1)
		old_main_point_y = shift_model['main_point']['y']
		shift_model['main_point']['y'] = len(shift_model['matrix'][0])
		shift_model['main_point']['x'] = old_main_point_y
		return shift_model

	@staticmethod
	def get_model(model_len, angle):
		rotate = 0
		if (angle >= 90):
			rotate = angle // 90
			angle = angle - rotate * 90
		shift_model = Modelling._get_low_angle_model(model_len, angle)
		if rotate > 0:
			for _ in range(rotate):
				shift_model = Modelling._rotate_shift_model(shift_model)
		return shift_model