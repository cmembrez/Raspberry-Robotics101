class TinyYOLOV3Params:
	def __init__(self, param, side):
		self.num = 3 if 'num' not in param else len(
			param['mask'].split(',')) if 'mask' in param else \
			int(param['num'])
		self.coords = 4 if 'coords' not in param else int(
			param['coords'])
		self.classes = 80 if 'classes' not in param else int(
			param['classes'])
		self.anchors = [float(a) for a in param['anchors'].split(',')]
		self.side = side

		if self.side == 13:
			self.anchor_offset = 2 * 3
		elif self.side == 26:
			self.anchor_offset = 2 * 0
		else:
			assert False, "Invalid output size. Only 13 and 26 " \
				"sizes are supported for output spatial dimensions"