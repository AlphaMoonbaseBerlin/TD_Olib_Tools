'''Info Header Start
Name : CallbackRemote
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.28040
Info Header End'''


class CallbackRemote:
	"""
	CallbackRemote description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def ExternalData(self):

		return self.ownerComp.op("callbackManager").Do_Callback("externalData")