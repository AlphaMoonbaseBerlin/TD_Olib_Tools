'''Info Header Start
Name : extOlibDependancy
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.28040
Info Header End'''

from os import path
import pathlib
import subprocess
import td


class extOlibDependancy:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def filepath(self)-> pathlib.Path:
		return pathlib.Path( 
			self.ownerComp.par.Downloaddirectory.eval(),
			self.ownerComp.par.Filename.eval() 
		)

	def fetchRemoteData(self):
		targetmode = self.ownerComp.par.Target.eval()
		if targetmode == "Olib"		: remote = self.ownerComp.op("olib_remote")
		if targetmode == "Github"	: remote = self.ownerComp.op("github_remote")
		if targetmode == "Url"		: remote = self.ownerComp.op("url_remote")
		if targetmode == "Callback" : remote = self.ownerComp.op("callback_remote")
		return remote.ExternalData()

	def GetRemoteFilepath(self):
		filepath = self.filepath()
		if filepath.is_file(): return filepath
		downloadURL = self.fetchRemoteData()
		return self.downloadFile( 	filepath,
									downloadURL )
	
	def GetGlobalComponent(self):
		globalOPShortcut = self.ownerComp.par.Targetopshortcut.eval()
		return getattr( op, globalOPShortcut, None ) or self.downloadAndPlace()

	def downloadAndPlace(self):
		targetTox = self.GetRemoteFilepath()
		if not targetTox: return None

		newComp 					= self.getTargetAndPlace().loadTox( targetTox )
		newComp.par.opshortcut.val = self.ownerComp.par.Targetopshortcut.eval()
		return newComp

	def getTargetAndPlace(self):
		operator = td.root
		for path_element in self.ownerComp.par.Targetplace.val.split("/"):
			if not path_element: continue
			operator = operator.op(path_element) or operator.create(baseCOMP, tdu.legalName(path_element))
		return operator

	def downloadFile(self, filepath:pathlib.Path, url:str):
		downloadScriptDAT 	= self.ownerComp.op("downloadScript")
		downloadScript 		= pathlib.Path( f"TDImportCache/Scripts/{downloadScriptDAT.id}" )
		downloadScript.is_file() or downloadScriptDAT.save(downloadScript, createFolders = True)
		executable = pathlib.Path( app.binFolder, "python.exe" )
		if subprocess.call( 
			[ executable, downloadScript, url, filepath]
			) :
			raise Exception( "Error on Download! Try again. Enable TOUCH_TEXT_CONSOLE to read info of subprocess.")
		return filepath
	
