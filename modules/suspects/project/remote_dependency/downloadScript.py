'''Info Header Start
Name : downloadScript
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.28040
Info Header End'''

import argparse
import requests
import pathlib

def main():
    argParser = argparse.ArgumentParser(
        prog = "Fetcher",
        description = "Fetches a component from the provided URL and filepath",
    )
    argParser.add_argument("url")
    argParser.add_argument("downloadFolder")
    argParser.add_argument("filename")

    arguments = argParser.parse_args()

    

    downloadFolder = pathlib.Path( arguments.downloadFolder )
    downloadFolder.mkdir(parents=True, exist_ok=True)
    
    filePath = pathlib.Path( downloadFolder, arguments.filename )
    print(f"Downloading {arguments.filename} to {arguments.downloadFolder} from {arguments.url}")#
    response = requests.get(arguments.url, stream=True)
    if not response.ok: 
        raise requests.ConnectionError
    
    with filePath.open( "wb" ) as targetFileHandler:
        totalLength = 0
        targetLength = response.headers["Content-Length"]
        for chunk in response.iter_content(chunk_size=64):
            targetFileHandler.write( chunk )
            totalLength += len(chunk)
            print(f"Downloaded {totalLength} of {targetLength}", end="\r")

		
if __name__ == "__main__":
    main()

