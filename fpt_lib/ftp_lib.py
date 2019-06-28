import sys
from ftplib import FTP
from ftplib import all_errors
import logging


class MyFTP:
    def __init__(self, ftp_host):
        logging.basicConfig(level=logging.INFO)
        self.ftp = FTP(ftp_host)

    def connect(self, user_name, password):
        try:
            resp = self.ftp.login(user=user_name, passwd=password)
            logging.info(resp)
            return "230" in resp
        except all_errors as e:
            logging.error(e)
            sys.exit(1)

    def check_files_count_in_current_directory(self):
        files = []
        self.ftp.retrlines("LIST", files.append)
        return len(files)

    def is_file_in_current_directory(self, filename):
        directory = []
        self.ftp.retrlines("LIST", directory.append)
        for file in directory:
            if filename in file:
                return True
        return False

    def upload_file(self, filename):
        with open(filename, "rb") as f:
            try:
                resp = self.ftp.storbinary("".join(["STOR ", filename]), f)
                logging.info(resp)
                return "226" in resp
            except all_errors as e:
                logging.error(e)
                return False

    def download_file(self, filename, download_filename):
        with open(download_filename, 'wb') as f:
            try:
                resp = self.ftp.retrbinary("".join(["RETR ", filename]), f.write)
                logging.info(resp)
                return "226" in resp
            except all_errors as e:
                logging.error(e)
                return False

    def close(self):
        self.ftp.close()
