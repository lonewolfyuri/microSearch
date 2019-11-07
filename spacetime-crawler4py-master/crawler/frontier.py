import os
import shelve

from threading import Thread, RLock
from queue import Queue, Empty

from utils import get_logger, get_urlhash, normalize
from scraper import is_valid

class Frontier(object):
    def __init__(self, config, restart):
        self.logger = get_logger("FRONTIER")
        self.config = config
        self.to_be_downloaded = list()
        if restart:
            if os.path.exists(self.config.save_file):
                os.remove(self.config.save_file)
            if os.path.exists(self.config.save_file + ".dir"):
                os.remove(self.config.save_file + ".dir")
            if os.path.exists(self.config.save_file + ".bak"):
                os.remove(self.config.save_file + ".bak")
            if os.path.exists(self.config.save_file + ".db"):
                os.remove(self.config.save_file + ".db")
            if os.path.exists(self.config.save_file + ".bat"):
                os.remove(self.config.save_file + ".bat")
        self.save = shelve.open(self.config.save_file)
        if restart:
            self.logger.info("re-starting from seed.")
            for url in self.config.seed_urls:
                self.add_url(url)
        else:
            self.logger.info("loading frontier from shelved file if exists")
            # Set the frontier state with contents of save file.
            self._parse_save_file()
            if not self.save:
                self.logger.info("Shelve file was empty or non existing, loading seed urls")
                for url in self.config.seed_urls:
                    self.add_url(url)

    def _parse_save_file(self):
        ''' This function can be overridden for alternate saving techniques. '''
        total_count = len(self.save)
        tbd_count = 0
        for url, completed in self.save.values():
            if not completed and is_valid(url):
                self.to_be_downloaded.append(url)
                tbd_count += 1
        self.logger.info(
            f"Found {tbd_count} urls to be downloaded from {total_count} "
            f"total urls discovered.")

    def get_tbd_url(self):
        try:
            return self.to_be_downloaded.pop()
        except IndexError:
            return None

    def add_url(self, url):
        url = normalize(url)
        urlhash = get_urlhash(url)
        if urlhash not in self.save:
            self.save[urlhash] = (url, False)
            self.save.sync()
            self.to_be_downloaded.append(url)
    
    def mark_url_complete(self, url):
        urlhash = get_urlhash(url)
        if urlhash not in self.save:
            # This should not happen.
            self.logger.error(
                f"Completed url {url}, but have not seen it before.")

        self.save[urlhash] = (url, True)
        self.save.sync()
