
'''Info Header Start
Name : extOlibDependancy
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.28040
Info Header End'''

from os import path
import pathlib
import subprocess
import functools


class extOlibDependancy:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def ClearCache(self):
		debug( "CÃ¶ear Cache")
		self.GetGlobalComponent.cache_clear()
		self.GetRemoteFilepath.cache_clear()
		self.ownerComp.cook( force = True )

	@functools.lru_cache(maxsize=1)
	def GetGlobalComponent(self):
		globalOPShortcut = self.ownerComp.par.Targetopshortcut.eval()
		return getattr( op, globalOPShortcut, None ) or self.downloadAndPlace()

	@functools.lru_cache(maxsize=1)
	def GetRemoteFilepath(self):
		filename, downloadpath = self.fetchRemoteData()
		return self.downloadFile( 	filename,
									downloadpath,
									self.ownerComp.par.Downloaddirectory.eval() )

	def fetchRemoteData(self):
		targetmode = self.ownerComp.par.Target.eval()
		if targetmode == "Olib"		: remote = self.ownerComp.op("olib_remote")
		if targetmode == "Github"	: remote = self.ownerComp.op("github_remote")
		if targetmode == "Url"		: remote = self.ownerComp.op("url_remote")
		return remote.ExternalData()

	def downloadAndPlace(self):
		target_tox = self.GetRemoteFilepath()
		if not target_tox: return None

		new_comp = self.getTargetAndPlace().loadTox( target_tox )
		new_comp.par.opshortcut = self.ownerComp.par.Targetopshortcut.eval()
		return new_comp

	def getTargetAndPlace(self):
		operator = root
		for path_element in self.ownerComp.par.Targetplace.val.split("/"):
			if not path_element: continue
			operator = operator.op(path_element) or operator.create(baseCOMP, tdu.legalName(path_element))
		return operator

	def downloadFile(self, filename, url, target_dir):
		downloadScriptDAT = self.ownerComp.op("downloadScript")
		downloadScript = pathlib.Path( f"TDImportCache/Scripts/{downloadScriptDAT.id}" )
		downloadScript.is_file() or downloadScriptDAT.save(downloadScript, createFolders = True)
		executable = pathlib.Path( app.binFolder, "python.exe" )
		subprocess.call( 
			[ executable, downloadScript, url, target_dir, filename]
			) 
		return pathlib.Path( target_dir, filename)
	