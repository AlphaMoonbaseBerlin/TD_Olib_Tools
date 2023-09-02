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
	
	@property
	def fileRegex(self):
		return self.ownerComp.par.Fileregex.eval()
	
	def searchFile(self, releaseDict:dict):
		for assetElement in releaseDict["assets"]:
			if re.match( self.fileRegex, assetElement["name"]): 
				return assetElement["browser_download_url"]
		raise Exception(f"Could not find file with regex {self.fileRegex}")

	def getAndRaise(self, url):
		response = requests.get( url )
		response.raise_for_status()
		return response
	
	def fetchLatest(self):
		owner, repoName = self.getRepoData()[0:2]
		apiEndpoint = f" https://api.github.com/repos/{owner}/{repoName}/releases/latest"
		response = self.getAndRaise( apiEndpoint )
		return self.searchFile( self.checkResponse( response ) )
	
	@property
	def tagRegex(self):
		return self.ownerComp.par.Tagregex.eval()
	
	def fetchByTag(self):
		owner, repoName = self.getRepoData()[0:2]
		apiEndpoint = f" https://api.github.com/repos/{owner}/{repoName}/releases?per_page={self.ownerComp.par.Searchdepth.eval()}"
		response = self.getAndRaise( apiEndpoint )
		for releaseDict in self.checkResponse( response ):
			if re.match( self.tagRegex , releaseDict["name"]): 
				return self.searchFile( releaseDict )
		raise Exception(f"Could not find tag with regex {self.tagRegex}")

	def ExternalData(self):
		if self.ownerComp.par.Mode.eval() == "Latest": return self.fetchLatest()
		if self.ownerComp.par.Mode.eval() == "Search Tag": return self.fetchByTag()
		raise Exception( "Invalid Mode selected", self.ownerComp.par.Mode.eval() )