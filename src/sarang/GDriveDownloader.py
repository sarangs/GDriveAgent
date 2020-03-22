#!/usr/bin/env python
# encoding: utf-8
'''
sarang.GDriveAgent 

1) Downloads your files from Google Drive OR Google contacts to the local disk 
2) The program should be triggered using a command line
3) Write extensive tests to test your code; preferably break your code
4) The scenarios that could not be automated, document them

It defines functions download_files_folders 

@author:     sarang

@copyright:  

@license:    license

@contact:    sawant.sarang@gmail.com
'''
import sys
import os
import os.path
import pickle
import requests
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from optparse import OptionParser
from apiclient import errors
from apiclient import http
from sarang import logger
from sarang.Exceptions import *
        
APP_GOOGLE_DRIVE = 'gdrive'

__all__ = []
__version__ = 0.1
__date__ = '2020-03-21'
__updated__ = '2020-03-21'

DEBUG = 1
TESTRUN = 0
PROFILE = 0


DOWNLOAD_SIZE = 4*1024*1024     # Download size 4MB

SCOPES = ['https://www.googleapis.com/auth/drive.file', 
          'https://www.googleapis.com/auth/drive.readonly', 
          'https://www.googleapis.com/auth/drive']


class GDriveDownloader():
    '''
        Methods exposed to Download GDrive files and folder with revision. 
    '''
    user_exist_req = 'https://www.googleapis.com/admin/directory/v1/users/{emailid}?customer=my_customer'
    
            
    def __init__(self):
        self.agent = None
        self.service = None
        self.credentials_cache = dict()
        
        
    def build_service(self):
        creds = None
        print(os.getcwd())
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
            
            self.credentials_cache.update(dict(token=creds.token,
                                               refresh_token=creds.refresh_token,
                                               token_uri=creds.token_uri,
                                               client_id=creds.client_id,
                                               client_secret=creds.client_secret,
                                               scopes=creds.scopes))
        
        self.service = build('drive', 'v3', credentials=creds)
        
    
    def download_files(self, names=None):
        #scans the complete folder
         
        if not isinstance(names, list):
            raise Exception('Needs list of file names')
        assert names
        pageToken = None 
        done = False
        pg_sz = 50
        downloaded = list()
        while not done:
            response = self.service.files().list(pageSize=pg_sz, pageToken=pageToken, 
                                                 fields="nextPageToken, files(id, name)").execute()
            items = response.get('files', list())
        
            if not items:
                logger.info('No files found in list')
                done = True
                continue
            
            for item in items:
                logger.info(u'{0} ({1})'.format(item['name'], item['id']))
                if item['name'] in names and self.download_file(item['id'], item['name']):
                    downloaded.append(item['name'])
            
            pageToken = response.get('nextPageToken', None)
            if pageToken is None:
                done = True
                continue
        return downloaded
            
        
    
    def download_file(self, file_id, name, export=None):
        fname = '%s.%s'% (os.path.splitext(name)[0], os.path.splitext(name)[1])
        fh = open(fname, 'wb')
        request = self.service.files().get_media(fileId=file_id)
        media_request = http.MediaIoBaseDownload(fh, request)
        done = False
        try:
            while True:
                try:
                    _progress, done = media_request.next_chunk()
                except errors.HttpError as error:
                    logger.error('An error occurred: %s' % error)
                    return False
                if _progress:
                    logger.info('Download Progress: %d%%' % int(_progress.progress() * 100))
                if done:
                    logger.info('Download Complete for file {0}'.format(name))
                    return done
        finally:
            fh.close()
    

def _main(files):
    
    downloader = GDriveDownloader()
    downloader.build_service()
    downloaded = downloader.download_files(names=files)
    logger.info('Following files {0} were downloaded from Gdrive'.format(downloaded))
    return downloaded

def main(argv=None):
    '''Command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_version = "v0.1"
    program_build_date = "%s" % __updated__

    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)
    program_longdesc = '''Script to download Gdrive files. When run first time it will generate auth tokens and pickle it''' 
    program_license = "Copyright 2020"

    if argv is None:
        argv = sys.argv[1:]
    try:
        # setup option parser
        parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license)
        parser.add_option("-i", "--in", dest="infile", help="set input path [default: %default]", metavar="FILE")
        
        # set defaults
        parser.set_defaults(outfile=sys.stdout, infile="downloading.txt")
        
        # process options
        (opts, args) = parser.parse_args(argv)
        
        files = list()
        with open(opts.infile) as fd:
            files.extend(fd.readlines())
        
        assert files
        
        _main(files)

    except Exception as e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2


if __name__ == "__main__":
    main()
