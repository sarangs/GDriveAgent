'''
Created on 22-Mar-2020

@author: sarangsawant
'''
import os
import unittest

from sarang.GDriveDownloader import _main

class Test(unittest.TestCase):

    
    def test_download_single_file(self):
        
        self.files = ['UCLA PGPX - Program Calender.pdf']
        downloaded_files = _main(self.files)
        self.assertListEqual(self.files, downloaded_files,"files and downloaded files are not same")
        
    def test_download_file_multiple_occurences(self):
        self.files = ['Data Base Performance Tuning']
        downloaded_files = _main(self.files)
        self.assertListEqual(self.files, downloaded_files,"files and downloaded files are not same")
    
    def test_download_big_files(self):
        self.files = ['Cybershot.zip']
        downloaded_files = _main(self.files)
        self.assertListEqual(self.files, downloaded_files,"files and downloaded files are not same")
    
    
    def test_donwload_zero_size_files(self):
        self.files = ['t']
        downloaded_files = _main(self.files)
        self.assertListEqual(self.files, downloaded_files,"files and downloaded files are not same")
    
    
    def test_non_existing_files(self):
        self.files = ['temp']
        downloaded_files = _main(self.files)
        assert not downloaded_files
        self.assertNotEqual(self.files, downloaded_files,"Lists not equal")
    
    
    def test_files_with_non_word_char(self):
        self.files = ['vaishali(2)(2)(2)(1)(1)(2)(1)(1)(1)']
        downloaded_files = _main(self.files)
        self.assertListEqual(self.files, downloaded_files,"Lists not equal")
     
    
    def test_folder_with_one_M_files(self):
        self.files = []
        raise NotImplementedError()
    
    def test_download_of_1M_files(self):
        self.files = []
        raise NotImplementedError()
    
    
    def tearDown(self):
        for p in self.files:
            if os.path.exists(p):
                os.unlink(p, dir_fd=None)
        self.files = None
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_']
    unittest.main()