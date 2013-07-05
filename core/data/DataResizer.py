"""
DataResizer

:Authors:
	Berend Klein Haneveld
"""

from vtk import vtkImageResample
from vtk import vtkVersion

VTK_MAJOR_VERSION = vtkVersion.GetVTKMajorVersion()

class DataResizer(object):
	"""
	DataResizer is a tool that will resize a given image dataset.
	You can specify a certain magnification factor or you can use a maximum 
	number of voxels that it should contain. If the image is larger than the 
	maximum amount of voxels, it will resize the volume to just below the 
	specified maximum.
	It will never upscale a volume! So factor value that are higher than 1.0
	will not have any result.
	"""

	def __init__(self):
		super(DataResizer, self).__init__()

	def ResizeData(self, imageData, factor=1.0, maximum=0):
		self.imageResampler = vtkImageResample()
		self.imageResampler.SetInterpolationModeToLinear()
		if VTK_MAJOR_VERSION <= 5:
			self.imageResampler.SetInput(imageData)
		else:
			self.imageResampler.SetInputData(imageData)
		
		# If a maximum has been set: calculate the right factor
		if maximum > 0:
			factor = self.calculateFactor(imageData.GetDimensions(), maximum)

		# Make sure that we are never upscaling the data
		if factor > 1.0:
			factor = 1.0

		self.resampledImageData = None
		if factor != 1.0:	
			self.imageResampler.SetAxisMagnificationFactor(0, factor)
			self.imageResampler.SetAxisMagnificationFactor(1, factor)
			self.imageResampler.SetAxisMagnificationFactor(2, factor)
			self.imageResampler.Update()
			self.resampledImageData = self.imageResampler.GetOutput()
		else:
			self.resampledImageData = imageData
		
		return self.resampledImageData

	# Private methods

	def calculateFactor(self, dimensions, maximum):
		voxels = dimensions[0] * dimensions[1] * dimensions[2]
		factor = float(maximum) / float(voxels)
		return factor
