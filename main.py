from scrapers.pastebin import PastebinCrawler
from dal import PasteDB, DBOrchestrator
import argparse
import logging
import logging.handlers
import time


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-db", help="Local database path", default="db.json")
    parser.add_argument("-t", "--time", help="Scrapping interval in seconds", default=120)
    args = parser.parse_args()
    return args


def get_logger():
    logger = logging.getLogger("pastebin_crawler")
    logger.setLevel(logging.DEBUG)
    h = logging.handlers.RotatingFileHandler('pastebin.log', 'a', 1024 * 5, 10)
    f = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    h.setFormatter(f)
    logger.addHandler(h)
    return logger


def main():
    args = get_arguments()
    logger = get_logger()
    pb_crawler = PastebinCrawler()
    logger.info("Pastebin Crawler Started")
    db = PasteDB(args.db)
    logger.info("Loaded db {}".format(args.db))
    db_orch = DBOrchestrator(db)
    keep_looping = True
    while keep_looping:
        logger.debug("Fetching recent pastes")
        recent_pastes = pb_crawler.get_recent_pastes_ids()
        for paste_id in recent_pastes:
            if not db_orch.does_exist(paste_id):
                try:
                    logger.debug("Fetching paste id: {}".format(paste_id))
                    crawled_paste = pb_crawler.get_paste(paste_id)
                    db_orch.add_paste(crawled_paste)
                except AttributeError:
                    logger.error("AttributeError fetching {} will try again.".format(paste_id))
                    break
                except:
                    logger.fatal("Unknown Error fetching {} shuting down.".format(paste_id))
                    keep_looping = False
                    return
            else:
                logger.debug("Already fetched {}".format(paste_id))
        logger.debug("Sleeping for {} seconds.".format(args.time))
        time.sleep(args.time)
    logger.debug("Shutting down")


if __name__ == '__main__':
    main()
