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

	def find_latest_version(self, slug):
		request_string = f"{self.ownerComp.par.Oliburl.eval()}/api/versions?component.slug={slug}&_limit=1&_sort=created_at:desc"
		response = requests.get( request_string )
		if not response.ok: return []		
		return response.json()

	def find_fixed_version(self, slug, version, build):
		request_string = f"{self.ownerComp.par.Oliburl.eval()}/api/versions?component.slug={slug}&_limit=1&_sort=created_at:desc&main_version={version}&build={build}"
		response = requests.get( request_string )
		if not response.ok: return []		
		return response.json()
		return

	def ExternalData(self):
		slug = self.ownerComp.par.Olibslug.eval().lower()
		mode = self.ownerComp.par.Versionmode.eval()
		result = None
		if mode == "Latest" : result = self.find_latest_version(slug)
		elif mode =="Fixed" : result = self.find_fixed_version( 	slug, 
																self.ownerComp.par.Version1.eval(),
																self.ownerComp.par.Version2.eval() )

		if result is None: raise Exception( "Invalid parameters, Could not find tox in Olib.")
		filename 		= result[0]["file"]["hash"] + result[0]["file"]["ext"]
		downloadpath 	= f"{self.ownerComp.par.Oliburl.eval()}/api/versions/{result[0]['id']}/download"
		return filename, downloadpath