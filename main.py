#!/usr/bin/env python3
    
import logging
import os
import sys

from mastodon_client import MastodonClient
from picture import Picture
from random_picture import WikimediaCommonsRandomPictureGenerator as PictureGenerator
from short_url import YourlsUrlShortener

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


    def random_picture(self):
        self.logger.info("Fetching random picture...")
        pic = self.picture_generator.random_picture()
        self.logger.info("Random picture: %s" % pic)
        return pic

    
    def shorten(self, url):
        shorturl = self.shortener.shorten(url)
        self.logger.info('Shortened full url "%s" to short url "%s"' % (url, shorturl))
        return shorturl


    def toot(self, picture):
        self.logger.info("Tooting the picture...")
        toot = self.mastodon.toot(picture)
        self.logger.info("Tooted: %s'" % toot)


    def fetch_and_post(self):
        pic = self.random_picture()
        pic.download(pic.filename)

        if pic.link:
            pic.link = self.shorten(pic.link)
        return self.mastodon.toot(pic)


if __name__ == '__main__':
    bot = RandomPictureBot()
    bot.fetch_and_post()
