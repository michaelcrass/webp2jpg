import re
import os
import datetime
import io
from datetime import date
from PIL import Image #pillow py -m pip install pillow
import pillow_avif # pip install pillow pillow-avif-plugin
import sys
import logging

class Programm:
    def __init__(self):
        # Configure logging
        self._logger = logging.getLogger(__name__)
        logging_format = "%(asctime)s - %(levelname)s - %(module)s - %(message)s"
        logging.basicConfig(filename=f"webp2jpg_{date.today()}.log", level="INFO",format=logging_format)

        # Add a console handler to show log entries as print in console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(logging_format)
        console_handler.setFormatter(console_formatter)
        logging.getLogger().addHandler(console_handler)
        
        #logging
        python_version = "{0}.{1}.{2}".format(sys.version_info.major,sys.version_info.minor,sys.version_info.micro)
        self._logger.info(f"User: {os.getenv('USERNAME')}@{os.getenv('COMPUTERNAME')}")
        self._logger.info(f"Python-Version: {python_version}")
        self._logger.info(f"Python-Script: {__file__}]")  


        #testmodus: delete all jpg-files in (sub-)folders
        self.testing = False
        if self.testing:
            self._logger.info("testing")
            self.get_webp_files()
            return

        #start
        self.start() 

    def get_webp_files(self):
        self._logger.info("get_webp_files")
        path = os.path.dirname(__file__)
        webp_files = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if self.testing:
                    if file.endswith(".jpg") or file.endswith(".jpeg"):
                        os.remove(os.path.join(root, file))
                        self._logger.info(f"Deleted: {file}")
                else:
                    if file.endswith(".webp") or file.endswith(".avif") or file.endswith(".jfif"):
                        webp_files.append(os.path.join(root, file))
        self._logger.info(f"{len(webp_files)} webp_files: {webp_files}")
        return webp_files

    def webp2jpg(self,file):
        self._logger.info(f"webp2jpg: {file}")
        im = Image.open(file).convert("RGB")
        filename, file_extension = os.path.splitext(file)
        new_file = f"{filename}_{date.today()}.jpg"
        im.save(new_file,"jpeg")
        im.close()
        return new_file

    def start(self):
        self._logger.info("start")

        if input("This pgramm converts webp/avif/jiff-files to .jpg, if they are in the same folder as the script (and subfolders). Continue? (y/n)") != "y":
            self._logger.info("Program ended by user.")
            return

        autodelete = False
        
        if input("Delete original files? (y/n)") == "y":
            autodelete = True
            self._logger.info("Delete original files.")
        else:
            self._logger.info("Keep original files.")

        for x in self.get_webp_files():
            statinfo = os.stat(x)
            self._logger.info("Found: " + x)
            self._logger.info(f"Size of the file: {statinfo.st_size} Bytes")
            
            jpgname = self.webp2jpg(x)

            if os.path.exists(jpgname):
                statinfojpg = os.stat(jpgname)
                self._logger.info("File created: " + jpgname)
                self._logger.info(f"Size of the new file: {statinfojpg.st_size} Bytes")
                if autodelete:
                    os.remove(x)
                    self._logger.info(f"Deleted: {x}")

if __name__ == '__main__':
    Programm()