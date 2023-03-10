#!/usr/bin/env python3
    
import logging
import os
import sys

from db import FileBasedPublishedImagesDatabase
from mastodon_client import MastodonClient
from picture import Picture
from random_picture import WikimediaCommonsRandomPictureGenerator as PictureGenerator
from short_url import YourlsUrlShortener
from yourls.exceptions import YOURLSHTTPError

class RandomPictureBot:

    def __init__(self):
        self.logger = logging.getLogger('wm.RandomPictureBot')
        self.logger.info('Initializing...')

        self.picture_generator = PictureGenerator()

        if 'MASTODON_ACCESS_TOKEN' not in os.environ:
            raise Exception('Missing environment variable: MASTODON_ACCESS_TOKEN')
        self.mastodon = MastodonClient(os.environ.get('MASTODON_ACCESS_TOKEN'))

        if 'YOURLS_SIGNATURE' not in os.environ:
            raise Exception('Missing environment variable: YOURLS_SIGNATURE')
        self.shortener = YourlsUrlShortener(os.environ.get('YOURLS_SIGNATURE'))

        self.db = FileBasedPublishedImagesDatabase()


    def random_picture(self):
        self.logger.debug("Fetching random picture...")
        pic = self.picture_generator.random_picture()
        self.logger.debug("Random picture: %s" % pic)
        return pic

    
    def shorten(self, url):
        shorturl = self.shortener.shorten(url)
        self.logger.info('Shortened full url "%s" to short url "%s"' % (url, shorturl))
        return shorturl


    def toot(self, picture):
        self.logger.debug("Tooting the picture...")
        toot = self.mastodon.toot(picture)
        self.logger.info("Tooted: %s'" % toot)


    def fetch_and_post(self):
        picture_exists = True
        while picture_exists:
            pic = self.random_picture()
            self.logger.info('Picture: "%s"', pic.title)
            picture_exists = self.db.is_published(pic)
            if picture_exists:
                self.logger.info('Picture already published')
        pic.download(pic.filename)
        pic.convert_to_jpeg()

        try:
            if pic.link:
                pic.link = self.shorten(pic.link)
        finally:
            self.db.add(pic)

        return self.toot(pic)


if __name__ == '__main__':

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    bot = RandomPictureBot()
    max_tries = int(os.environ['WALTER_TRIES']) if 'WALTER_TRIES' in os.environ else 3
    tries = 0
    while tries < max_tries:
        tries = tries + 1
        try:
            bot.fetch_and_post()
            break
        except YOURLSHTTPError as e:
            logger.warning('Failed due to YOURLS. Trying again...', exc_info=e)
        except Exception as e:
            logger.warning('Failed due to other exception', exc_info=e)
