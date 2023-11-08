from pathlib import Path
import uuid
import re
class extDownloader:
	"""
	extDownloader description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def DownloadAndUse(self, downloadId:str ):
		baseName 	= Path( iop.Store.Data.op("downloads")[ downloadId, "Filename"].val )
		url 		= iop.Store.Data.op("downloads")[ downloadId, "Downloadlink"].val
		releaseId 	= iop.Store.Data.op("downloads")[ downloadId, "releaseId"].val
		releaseVersion = iop.Store.Data.op("releases")[ releaseId, "Version"].val

		owner 	= iop.Store.Data.op("releases")[ releaseId, "Owner"].val
		repo 	= iop.Store.Data.op("releases")[ releaseId, "Repo"].val

		filename = baseName

		if filename.suffix == ".tox":
			filename = Path( f"{releaseVersion}_{baseName}" )
			downloadPath = Path( app.userPaletteFolder,"GitHub", owner, repo )
			meta = {"callback" : self.placeTox }

		elif filename.suffix in [".py", ".pyi"]:
			filename = Path( baseName )
			downloadPath = Path( "typings" )
			meta = {"callback" : self.placeTyping }
		else:
			return ui.messageBox("Invalid Filetype", 
						f"The GitHub browser currently does not support files with the type {filename.suffix}")

		self.ownerComp.op("fileDownloader").QueryDownload(
			url,
			downloadPath,
			filename = filename,
			meta = meta
		)
		return
	def placeTyping(self, download:"Download"):
		builtinsFile = Path("typings", "__builtins__.pyi")
		builtinsFile.touch(exist_ok=True)

		currentBuiltinsText = builtinsFile.read_text()
		if re.search(f"import * from {download.filepath.stem}", currentBuiltinsText): return
		with builtinsFile.open("t+a") as builtinsFileHandler:
			builtinsFileHandler.write(f"\nfrom {download.filepath.stem} import *")
		return
	
	def placeTox(self, download:"Download"):
		#op('/ui/dialogs/palette/palette/local/macros/refreshFolder').run()
		loaded_tox = self.ownerComp.op('quitePlace').copy( op('quitePlace/template'), name=str(uuid.uuid4()))
		loaded_tox.par.Filepath = download.filepath 
		ui.panes.current.placeOPs( [ loaded_tox ] )
		return