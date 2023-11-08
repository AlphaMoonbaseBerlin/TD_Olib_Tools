

class extGithubBrowserController:
	"""
	extGithubBrowserController description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
	@property
	def searchTag(self):
		return "td-olib-project"
	
	@property
	def webclient(self):
		return self.ownerComp.op("queriedWebclient")

	def ClearData(self):
		iop.Store.Data.op("releaseParser").Clear()
		iop.Store.Data.op("downloadsParser").Clear()

	def SearchRepositories(self, name="", tags = []):
		self.ClearData()
		self.webclient.Get("search/repositories",
			params = {
				"q" : f"{name} in:name topic:{' '.join([self.searchTag] + tags)}"
			},
			callback = self._parseRepositories)
		
	def _parseRepositories(self, request, response, webclient_comp):
		iop.Store.Data.op("repositoryParser").Clear()
		iop.Store.Data.op("repositoryParser").AddDicts(
			response.data["items"]
		)
		return
	
	def SearchReleases(self, repo:str, owner:str):
		request = self.webclient.Get(f"repos/{owner}/{repo}/releases", callback = self._parseReleases)
		request.meta = {
			"owner" : owner,
			"repo"  : repo
		}

	def _parseReleases(self, request, response, webclient_comp):
		self.ClearData()
		iop.Store.Data.op("releaseParser").AddDicts([{**item, **request.meta} for item in response.data])