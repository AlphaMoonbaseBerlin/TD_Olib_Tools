'''Info Header Start
Name : githubRemote
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.28040
Info Header End'''

import re, requests
class githubRemote:
	"""
	githubRemote description
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

	def getRepoData(self):
		return [ str(value) for value in re.search(r"github\.com\/([\w,-]+)\/([\w,-]+).*", self.ownerComp.par.Repository.eval()).groups() ]
	
	def searchFile(self, releaseDict:dict):
		for assetEement in releaseDict["assets"]:
			if re.match( self.ownerComp.par.Fileregex.eval(), assetEement["name"]): 
				return assetEement.get("browser_download_url", "" )

	def fetchLatest(self):
		owner, repoName = self.getRepoData()[0:2]
		apiEndpoint = f" https://api.github.com/repos/{owner}/{repoName}/releases/latest"
		response = requests.get( apiEndpoint )
		return self.searchFile( self.checkResponse( response ) )

	def fetchByTag(self):
		owner, repoName = self.getRepoData()[0:2]
		apiEndpoint = f" https://api.github.com/repos/{owner}/{repoName}/releases?per_page={self.ownerComp.par.Searchdepth.eval()}"
		response = requests.get( apiEndpoint )
		for releaseDict in self.checkResponse( response ):
			if re.match( self.ownerComp.par.Tagregex.eval(), releaseDict["name"]): 
				return self.searchFile( releaseDict )
		

	def ExternalData(self):
		if self.ownerComp.par.Mode.eval() == "Latest": return self.fetchLatest()
		if self.ownerComp.par.Mode.eval() == "Search Tag": return self.fetchByTag()