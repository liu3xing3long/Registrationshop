"""
AppResources

:Authors:
	Berend Klein Haneveld
"""

import os
from AppVars import AppVars

class AppResources(object):
	"""
	AppResources is a static class that can be used to find common resources
	easily. Just provide a name to the 
	"""
	
	@staticmethod
	def imageNamed(imageName):
		"""
		Returns the full path to the given imageName. 

		Note:
		Future versions might be more intelligent and can handle searching 
		through the resource folder. For now it just combines the AppVars 
		imagePath with the imageName.

		:type imageName: basestring
		:rtype: basestring
		"""
		return os.path.join(AppVars.imagePath(), imageName)

