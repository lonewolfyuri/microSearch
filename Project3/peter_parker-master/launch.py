from configparser import ConfigParser
from argparse import ArgumentParser

import crawler.file
from utils.server_registration import get_cache_server
from utils.config import Config
from crawler import Crawler
from crawler.file import urlFile, contentFile


def main(config_file, restart):
    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)
    config.cache_server = get_cache_server(config, restart)
    crawler = Crawler(config, restart)
    crawler.start()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--restart", action="store_true", default=False)
    parser.add_argument("--config_file", type=str, default="config.ini")
    args = parser.parse_args()
    # Handling keyboard interruption
    try:
        main(args.config_file, args.restart)
    except KeyboardInterrupt:
        print("Keyboard interrupted")
        print("Current largest page is ", crawler.file.maxLengthURL, "      word count : ", str(crawler.file.maxLength))
        urlFile.close()
        contentFile.close()
    # Closing all files
    print("Current largest page is ", crawler.file.maxLengthURL, "      word count : ", str(crawler.file.maxLength))
    urlFile.close()
    print("SUCCESSFULLY CLOSED urls.txt")
    contentFile.close()
    print("SUCCESSFULLY CLOSED content.txt")

