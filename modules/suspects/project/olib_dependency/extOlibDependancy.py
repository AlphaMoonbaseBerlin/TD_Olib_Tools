'''Info Header Start
Name : extOlibDependancy
Author : Alpha Moonbase
Version : 0
Build : 5
Savetimestamp : 1669915146
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

	def validate_external(self, component):
		path = component.par.externaltox.eval()
		return bool(path) and os.path.isfile( path )

	def Get_Component(self):
		target_operator = None
		if self.ownerComp.par.Refferencemode.eval() == "Global": 
			op_shortcut = self.ownerComp.par.Targetopshortcut.eval()
			target_operator = getattr( op, op_shortcut, None )
		elif self.ownerComp.par.Refferencemode.eval() == "Path" and self.validate_external( self.ownerComp.par.Targetoperator.eval()): 
			target_operator = self.ownerComp.par.Targetoperator.eval()

		
		return  target_operator or self.download_and_place()

	def download_and_place(self):
		version_data = self.find_version()
		if not version_data: return None
		target_tox = self.download_file( version_data[0]["file"]["hash"] + version_data[0]["file"]["ext"],
										 f"{self.ownerComp.par.Oliburl.eval()}/api/versions/{version_data[0]['id']}/download",
										 self.ownerComp.par.Downloadfolder.eval() )
		if not target_tox: return None

		new_comp = self.get_target_component()
		if new_comp is None:
			raise Exception( "Could not find or create component. Makre sure the correct mode is selected.")

		if self.ownerComp.par.Refferencemode.eval() == "Global": new_comp.par.opshortcut = self.ownerComp.par.Targetopshortcut.eval()
		new_comp.par.externaltox 		= target_tox
		new_comp.par.reinitnet.pulse()
		new_comp.par.reloadcustom 		= False
		new_comp.par.reloadbuiltin 		= False
		new_comp.par.savebackup 		= False
		return new_comp


	def get_target_component(self):
		if self.ownerComp.par.Refferencemode.eval() == "Global": return self.get_global_component()
		elif self.ownerComp.par.Refferencemode.eval() == "Path": return self.get_fixed_component()
		return None

	def get_global_component(self):
		operator = root
		for path_element in self.ownerComp.par.Targetplace.val.split("/") + [self.ownerComp.par.Targetopshortcut.eval()]:
			if not path_element: continue
			operator = operator.op(path_element) or operator.create(baseCOMP, tdu.legalName(path_element))
		return operator

	def get_fixed_component(self):
		return self.ownerComp.par.Targetoperator.eval()

	def download_file(self, filename, url, target_dir):
		filepath = os.path.join( target_dir, filename)
		if os.path.isfile(filepath): return filepath

		response = requests.get(url)

		if not response.ok: return ''

		os.makedirs(target_dir, exist_ok = True)
		
		target_file = open(filepath, "wb")
		target_file.write( response.content )
		target_file.close()
		return filepath

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
		
	def find_stable_version(self, slug, version):
		request_string = f"{self.ownerComp.par.Oliburl.eval()}/api/versions?component.slug={slug}&_limit=1&_sort=created_at:desc&main_version={version}"
		response = requests.get( request_string )
		if not response.ok: return []		
		return response.json()

	def find_version(self):
		slug = self.ownerComp.par.Olibslug.eval().lower()
		mode = self.ownerComp.par.Versionmode.eval()
		if mode == "Latest" 	: return self.find_latest_version(slug)
		elif mode =="Stable" 	: return self.find_stable_version( 	slug, 
																	self.ownerComp.par.Version.eval() )
		elif mode =="Fixed" 	: return self.find_fixed_version( 	slug, 
																	self.ownerComp.par.Version.eval(),
																	self.ownerComp.par.Build.eval() )

		return []