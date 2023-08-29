'''Info Header Start
Name : urlRemote
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.28040
Info Header End'''

class urlRemote:
	"""
	urlRemote description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def ExternalData(self):
		downloadpath = self.ownerComp.par.Url.eval()
		filename = self.ownerComp.par.Filename.eval() or downloadpath.split("/")[-1]
		return downloadpath
		#return filename, downloadpath