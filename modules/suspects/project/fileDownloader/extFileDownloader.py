
'''Info Header Start
Name : extFileDownloader
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.28040
Info Header End'''
import os
import downloader_utils

TDF = op.TDModules.mod.TDFunctions

class extFileDownloader:
	"""
	extFileDownloader description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
	
		self.Progress = self.ownerComp.op('info')['out1']
		self.Downloading = tdu.Dependency( False )

		self.info_table = self.ownerComp.op("info_table")
		#self.info_table.clear( keepFirstRow = True, keepFirstCol = True)
		self.info_table.copy( self.ownerComp.op("startup_table") )
	

		self.download_query 	= []
		self.current_download 	= None
		self.info 				= self.ownerComp.op("info")

		self.log = self.ownerComp.op("log")
		self.log.clear()

		self.client 		= self.ownerComp.op("downloader")
		self.client.par.stop.pulse()

		self.timeout_timer 	= self.ownerComp.op('timeout_timer')
		self.timeout_timer.par.initialize.pulse()
		self.callbacks 		= self.ownerComp.op('callbackManager')
	
	def write_log(self, *args):
		self.log.appendRow( args )

	def Query_Download(self, source_url, target_dir, filename = False, meta = None):
		
		self.write_log("Querying Download", filename)

		filename = filename if filename else source_url.split('/')[-1]
		download_element = { 	"source_url"	:	source_url,
								"filename"		:	filename,
								"target_dir"	:	target_dir,
								"file_object"	:	None,
								"meta"			:	meta,
							}
							
		
		
		self.download_query.append( download_element )
		self.check_query()
		
	def check_query(self):
		self.Downloading.val = False
		self.write_log("Checking Query")

		if self.current_download is not None: 
			return
		self.stop_timer()
		if self.current_download is None and not len( self.download_query ) :

			if not len( self.download_query ): self.callbacks.Execute("OnQueryFinish")()
			return
		
		self.current_download = self.download_query.pop(0)
		self.write_log("New Download", self.current_download)
	
		self.Downloading.val = True
		os.makedirs( self.current_download["target_dir"], exist_ok = True )
		self.current_download["target_filepath"] 	= self.get_filepath( self.current_download["target_dir"], self.current_download["filename"] )
		self.current_download["download_filepath"] 	= self.current_download["target_filepath"] + ".download"
		

		self.remove_file(self.current_download["download_filepath"])

		self.callbacks.Do_Callback("OnDownloadStart", self.current_download['source_url'], self.current_download["target_filepath"], self.current_download['meta'] )

		if os.path.isfile( self.current_download["target_filepath"] ): 
			self.write_log("File already exists. Continuing", self.current_download["target_filepath"] )
			self.finish_download()
			return

		self.current_download["file_object"] = open( self.current_download["download_filepath"], "wb" )
		self.client.par.stop.pulse()
		self.client.request( self.current_download["source_url"], "GET" )
		self.start_timer()

		
	
			
	def start_timer(self):
		
		self.timeout_timer.par.start.pulse()
		
	def stop_timer(self):
		
		self.timeout_timer.par.initialize.pulse()
		
	def write_line(self, data):
		self.start_timer()
		self.current_download["file_object"].write( data )
		self.write_log("Writing Line")
		self.update_info_table()
		if self.download_done(): self.finish_download()
	
	def close_current_file(self):
		file = self.current_download.get("file_object", None)
		if file: file.close()

	def remove_file(self, filepath):
		try:
			os.remove( filepath )
		except FileNotFoundError:
			pass

	def timeout(self):
		self.client.par.stop.pulse()
		if not self.current_download: return
		self.close_current_file()
		self.remove_file( self.current_download.get("download_filepath", "" ) )

		self.callbacks.Do_Callback("OnFail", self.current_download['source_url'], self.current_download['meta'] )

		self.current_download = None
		self.check_query()
	
	def download_done(self):
		return self.ownerComp.op("info")["downloaded_size"].eval() >= self.ownerComp.op("info")["total_size"].eval()

	def finish_download(self):
		self.info_table["state", "value"] = "done"
		self.info_table["queue", "value"]			= len( self.download_query )
		
		self.close_current_file()
		self.write_log("Finishing Download")
		try:
			os.rename(self.current_download["download_filepath"], self.current_download["target_filepath"])
		except FileNotFoundError:
			pass
		except Exception as e:
			debug(e)
		self.callbacks.Do_Callback("OnDownloadFinish", self.current_download["target_filepath"], self.current_download['meta'] )
		
		self.current_download = None
		self.stop_timer()
		run( "args[0]()", lambda: self.check_query(), delayFrames = 1, fromOP = self.ownerComp)
		#self.check_query()
		
		
	def get_filepath(self, dir, name):
		filepath =  dir + "/" + name
		return filepath
		
	def update_info_table(self):
		self.info_table["state", "value"]			= "downloading"
		self.info_table["source", "value"]			= self.current_download["source_url"]
		self.info_table["target", "value"] 			= self.current_download["target_filepath"]
		self.info_table["target_size", "value"] 	= downloader_utils.convert_size( self.ownerComp.op("info")["total_size"].eval() )
		self.info_table["downloaded_size", "value"] = downloader_utils.convert_size( self.ownerComp.op("info")["downloaded_size"].eval() )
		self.info_table["speed", "value"] 			= downloader_utils.convert_size( self.ownerComp.op("speed")["speed"].eval() ) + "/s"
		current_speed = self.ownerComp.op("speed")["speed"].eval()
		if current_speed:
			self.info_table["estimated_time", "value"]  = downloader_utils.convert_time( (self.ownerComp.op("info")["total_size"].eval() - self.ownerComp.op("info")["downloaded_size"].eval())/self.ownerComp.op("speed")["speed"].eval()  )
		else:
			self.info_table["estimated_time", "value"]  = downloader_utils.convert_time( 0 )
		self.info_table["queue", "value"]			= len( self.download_query )