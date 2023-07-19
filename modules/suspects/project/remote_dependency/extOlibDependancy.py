'''Info Header Start
Name : extOlibDependancy
Author : Wieland
Version : 0
Build : 3
Savetimestamp : 1674234668
Saveorigin : Project.toe
Saveversion : 2022.28040
Info Header End'''
from importlib.resources import path
import requests
from functools import lru_cache
import os
class extOlibDependancy:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp


	def Get_Component(self):
		op_shortcut = self.ownerComp.par.Targetopshortcut.eval()
		return getattr( op, op_shortcut, None ) or self.download_and_place()

	def download_and_place(self):
		targetmode = self.ownerComp.par.Target.eval()
		if targetmode == "Olib"		: remote = self.ownerComp.op("olib_remote")
		if targetmode == "Github"	: remote = self.ownerComp.op("github_remote")
		if targetmode == "Url"		: remote = self.ownerComp.op("url_remote")
		filename, downloadpath = remote.ExternalData()

		target_tox = self.download_file( filename,
										 downloadpath,
										 f"TDImportCache/external/{targetmode}")
		if not target_tox: return None

		new_comp = self.get_target_place().loadTox( target_tox )
		new_comp.par.opshortcut = self.ownerComp.par.Targetopshortcut.eval()
		return new_comp

	def get_target_place(self):
		operator = root
		for path_element in self.ownerComp.par.Targetplace.val.split("/"):
			if not path_element: continue
			operator = operator.op(path_element) or operator.create(baseCOMP, tdu.legalName(path_element))
		return operator

	def download_file(self, filename, url, target_dir):
		filepath = os.path.join( target_dir, filename)
		if os.path.isfile(filepath): return filepath

		response = requests.get(url)

		if not response.ok: return ''

		os.makedirs(target_dir, exist_ok = True)
		
		with open(filepath, "wb") as target_file: 
			target_file.write( response.content )
		
		return filepath

	