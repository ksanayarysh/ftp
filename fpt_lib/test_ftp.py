import configparser
import os
import unittest

from fpt_lib.ftp_lib import MyFTP

config = configparser.ConfigParser()
config.read('ftp_creds.ini')
ftp_secret = config.get('vm', 'secret')
ftp_user = config.get('vm', 'user')
ftp_host = config.get('vm', 'host')

upload_filename = "Chajka.txt"
download_filename = "".join([upload_filename, "-new", ".txt"])


class TestFTP(unittest.TestCase):
    def setUp(self):
        self.my_ftp = MyFTP(ftp_host)

    def tearDown(self):
        self.my_ftp.close()

    def test_upload_file(self):
        """
        check that where is no such file
        then upload it
        then check that it has appeared
        """
        if self.my_ftp.connect(user_name=ftp_user, password=ftp_secret):
            self.assertFalse(self.my_ftp.is_file_in_current_directory(filename=upload_filename))
            if self.my_ftp.upload_file(filename=upload_filename):
                self.assertTrue(self.my_ftp.is_file_in_current_directory(filename=upload_filename))

    def test_download_file(self):
        """
        check that we have no file
        download it from ftp (if there is no file there than upload it first)
        check that file has appeared
        """
        if self.my_ftp.connect(user_name=ftp_user, password=ftp_secret):
            if not self.my_ftp.is_file_in_current_directory(filename=upload_filename):
                self.my_ftp.upload_file(filename=upload_filename)
            self.assertFalse(os.path.exists(download_filename))
            if self.my_ftp.download_file(filename=upload_filename, download_filename=download_filename):
                self.assertTrue(os.path.exists(download_filename))
