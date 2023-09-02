'''Info Header Start
Name : olibRemote
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.28040
Info Header End'''
import requests
class olibRemote:
	"""
	olibRemote description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.log = self.ownerComp.op("logger").Log

	def checkResponse(self, response:requests.Request ):
		if not response.ok: 
			self.log("Could not resolve reques to OLIB.", response.url , response.status_code, response.reason)
			raise Exception( "Error Response. Check Logs!")
		responseData = response.json()
		if not responseData:
			self.log("Olib returned empty response!", response.url, responseData )
			raise Exception( "Empty Response. Check Logs!")
		return responseData

	def findLatestVersion(self, slug):
		request_string = f"{self.ownerComp.par.Oliburl.eval()}/api/versions?component.slug={slug}&_limit=1&_sort=created_at:desc"
		response = requests.get( request_string )
		return self.checkResponse(response)

	def findFixedVersion(self, slug, version, build):
		request_string = f"{self.ownerComp.par.Oliburl.eval()}/api/versions?component.slug={slug}&_limit=1&_sort=created_at:desc&main_version={version}&build={build}"
		response = requests.get( request_string )
		return self.checkResponse( response )
	
	def findFixedVersion(self, slug, version):
		request_string = f"{self.ownerComp.par.Oliburl.eval()}/api/versions?component.slug={slug}&_limit=1&_sort=created_at:desc&main_version={version}"
		response = requests.get( request_string )
		return self.checkResponse( response )

	def ExternalData(self):
		slug = self.ownerComp.par.Olibslug.eval().lower()
		mode = self.ownerComp.par.Versionmode.eval()
	
		if mode == "Latest" : result = self.findLatestVersion(slug)
		elif mode =="Fixed" : result = self.findFixedVersion( 	slug, 
																self.ownerComp.par.Version.eval(),
																self.ownerComp.par.Build.eval() )
			
		elif mode =="Stable" : result = self.findFixedVersion( 	slug, 
																self.ownerComp.par.Version.eval() )

		downloadpath 	= f"{self.ownerComp.par.Oliburl.eval()}/api/versions/{result[0]['id']}/download"

		return downloadpath