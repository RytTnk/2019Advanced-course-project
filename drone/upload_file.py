#! /usr/bin/env python
# -*- coding: utf-8 -*-

#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Include library -----
import os
import pprint

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
#_____________________________________________________________________


#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Utility of google drive library -----
######################################################################
## @version    0.1.0
## @author     K.Ishimori
## @date       2019/12/19 Newly created.                  [K.Ishimori]
## @brief      Utility of google drive library
######################################################################
class google_drive_utility:
    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Initialized utility class -----
    ######################################################################
    ## @brief      Initialized utility class
    ######################################################################
    def __init__(self):
        ## Create google drive api object
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        self.gdrive_api = GoogleDrive(gauth)

        ## Create file object for google drive api
        self.gdrive_file = self.gdrive_api.CreateFile()

        ## Create file list object
        self.files = []
        self.files_idx = 0
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Set google drive file processing -----
    ######################################################################
    ## @brief      Set google drive file processing
    ######################################################################
    def set_gd_file_proc(self, gd_file):
        self.gdrive_file.SetContentFile(gd_file)
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Upload google drive file processing -----
    ######################################################################
    ## @brief      Upload google drive file processing
    ######################################################################
    def upload_gd_file_proc(self):
        self.gdrive_file.Upload()
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Get google drive file url processing -----
    ######################################################################
    ## @brief      Get google drive file url processing
    ######################################################################
    def get_gd_file_url_proc(self):
        url = 'https://drive.google.com/uc?id=' + str( self.gdrive_file['id'] )
        return url
    #____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Get file list processing -----
    ######################################################################
    ## @brief      Get file list processing
    ######################################################################
    def get_file_list_proc(self, path):
        for filename in os.listdir(path):
            if os.path.isfile(os.path.join(path, filename)):
                self.files.append(filename)
                self.files_idx = self.files_idx + 1
    #____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Get last file processing -----
    ######################################################################
    ## @brief      Get last file processing
    ######################################################################
    def get_last_file_proc(self):
        last_file = self.files[self.files_idx - 1]
        print(last_file)
        return last_file
    #____________________________________________________________________

#_____________________________________________________________________


#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Main processing -----
######################################################################
## @brief      Main processing
## @callgraph
## @callergraph
######################################################################
def main_proc():

    gd_utility = google_drive_utility()

    path = './20191214175813'
    gd_utility.get_file_list_proc(path)

    exit()

    # Set google drive file processing
    gd_utility.set_gd_file_proc('haarcascade_smile.xml')
    # Upload google drive file processing
    gd_utility.upload_gd_file_proc()
    # Get google drive file url processing
    print(gd_utility.get_gd_file_url_proc())

if __name__ == '__main__':
    main_proc()
