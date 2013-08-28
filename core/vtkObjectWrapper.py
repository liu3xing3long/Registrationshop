"""
vtkObjectWrapper

:Authors:
	Berend Klein Haneveld
"""

from core.decorators import overrides
from vtk import vtkColorTransferFunction
from vtk import vtkPiecewiseFunction
from vtk import vtkVolumeProperty


class vtkObjectWrapper(object):
	"""
	vtkObjectWrapper is an interface class for
	wrapping vtkObjects. The subclass must implement the
	two methods to set and retrieve the original vtk
	object.
	"""

	def __init__(self, vtkObject=None):
		"""
		Provide a vtk object so that it will automatically
		get wrapped.
		:type vtkObject: vtkObject
		"""
		super(vtkObjectWrapper, self).__init__()

		if vtkObject is not None:
			self.setOriginalObject(vtkObject)

	def setOriginalObject(self, vtkObject):
		"""
		Provide a vtk object so that it gets wrapped.
		Subclasses should implement this method for specific
		vtkObject types.
		:type vtkObject: vtkObject
		"""
		raise NotImplementedError()

	def originalObject(self):
		"""
		Returns a vtk object that was wrapped.
		Subclasses should implement this method for specific
		vtkObject types.
		:rtype: vtkObject
		"""
		raise NotImplementedError()

	def applyToObject(self, vtkObject):
		"""
		Instead of returning a new object, sometimes only properties
		of vtkObjects are stored and should be applied to already
		existing vtkObjects.
		"""
		raise NotImplementedError()


class vtkColorTransferFunctionWrapper(vtkObjectWrapper):
	"""
	vtkColorTransferFunctionWrapper is a wrapper around
	vtkColorTransferFunction object. It stores the nodes
	from the transfer function.
	On retrieval it will create a new vtkColorTransferFunction
	and put the original values back.
	"""
	def __init__(self, colorFunction=None):
		super(vtkColorTransferFunctionWrapper, self).__init__(colorFunction)

	@overrides(vtkObjectWrapper)
	def setOriginalObject(self, colorFunction):
		self.nodes = []

		for index in range(colorFunction.GetSize()):
			value = [0 for x in range(6)]
			colorFunction.GetNodeValue(index, value)
			self.nodes.append(value)

	@overrides(vtkObjectWrapper)
	def originalObject(self):
		colorTransferFunction = vtkColorTransferFunction()
		for index in range(len(self.nodes)):
			value = self.nodes[index]
			colorTransferFunction.AddRGBPoint(value[0], value[1], value[2], value[3], value[4], value[5])

		return colorTransferFunction


class vtkPiecewiseFunctionWrapper(vtkObjectWrapper):
	"""
	vtkPiecewiseFunctionWrapper is a wrapper around
	vtkPiecewiseFunction object. It stores the nodes
	from the transfer function.
	On retrieval it will create a new vtkPiecewiseFunction
	and put the original values back.
	"""
	def __init__(self, piecewiseFunction=None):
		super(vtkPiecewiseFunctionWrapper, self).__init__(piecewiseFunction)

	@overrides(vtkObjectWrapper)
	def setOriginalObject(self, piecewiseFunction):
		self.nodes = []
		for index in range(piecewiseFunction.GetSize()):
			value = [0 for x in range(4)]
			piecewiseFunction.GetNodeValue(index, value)
			self.nodes.append(value)

	@overrides(vtkObjectWrapper)
	def originalObject(self):
		pieceWiseFunction = vtkPiecewiseFunction()
		for index in range(len(self.nodes)):
			value = self.nodes[index]
			pieceWiseFunction.AddPoint(value[0], value[1], value[2], value[3])

		return pieceWiseFunction


class vtkVolumePropertyWrapper(vtkObjectWrapper):
	"""
	vtkVolumePropertyWrapper is a wrapper around
	vtkVolumeProperty object. It stores the properties
	of a vtkVolume as attributes.
	"""
	def __init__(self, VolumeVisualization=None):
		super(vtkVolumePropertyWrapper, self).__init__(VolumeVisualization)

	@overrides(vtkObjectWrapper)
	def setOriginalObject(self, VolumeVisualization):
		self.independentComponents = VolumeVisualization.GetIndependentComponents()
		self.interpolationType = VolumeVisualization.GetInterpolationType()
		self.shade = VolumeVisualization.GetShade()
		self.ambient = VolumeVisualization.GetAmbient()
		self.diffuse = VolumeVisualization.GetDiffuse()
		self.specular = VolumeVisualization.GetSpecular()
		self.specularPower = VolumeVisualization.GetSpecularPower()
		self.scalarOpacityUnitDistance = VolumeVisualization.GetScalarOpacityUnitDistance()

	@overrides(vtkObjectWrapper)
	def originalObject(self):
		VolumeVisualization = vtkVolumeProperty()
		VolumeVisualization.SetIndependentComponents(self.independentComponents)
		VolumeVisualization.SetInterpolationType(self.interpolationType)
		VolumeVisualization.SetShade(self.shade)
		VolumeVisualization.SetAmbient(self.ambient)
		VolumeVisualization.SetDiffuse(self.diffuse)
		VolumeVisualization.SetSpecular(self.specular)
		VolumeVisualization.SetSpecularPower(self.specularPower)
		VolumeVisualization.SetScalarOpacityUnitDistance(self.scalarOpacityUnitDistance)
		return VolumeVisualization


class vtkCameraWrapper(vtkObjectWrapper):
	"""vtkCameraWrapper is a wrapper around
	vtkCamera object. It stores the properties of a
	vtkCamera as attributes. Do not use the originalObject method
	to retrieve but rather apply the settings to an already created
	vtkCamera object."""
	def __init__(self, camera=None):
		super(vtkCameraWrapper, self).__init__(camera)

	@overrides(vtkObjectWrapper)
	def setOriginalObject(self, camera):
		self.position = camera.GetPosition()
		self.focalPoint = camera.GetFocalPoint()
		self.viewUp = camera.GetViewUp()
		self.distance = camera.GetDistance()
		self.clippingRange = camera.GetClippingRange()

	@overrides(vtkObjectWrapper)
	def applyToObject(self, camera):
		camera.SetPosition(self.position)
		camera.SetFocalPoint(self.focalPoint)
		camera.SetViewUp(self.viewUp)
		camera.SetDistance(self.distance)
		camera.SetClippingRange(self.clippingRange)
