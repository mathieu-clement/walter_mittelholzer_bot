#!/usr/bin/env python3

from yourls import YOURLSClient


class UrlShortener:
    def shorten(self, url):
        """Shortens URL using shortener service and returns shortened URL."""
        pass


class YourlsUrlShortener(UrlShortener):
    def __init__(self, signature):
        self.client = YOURLSClient('https://s.citrouille.ch/yourls-api.php', signature=signature)

    def shorten(self, url):
        shortened = self.client.shorten(url)
        return shortened.shorturl


if __name__ == '__main__':
    import os
    import random
    import sys

    if 'YOURLS_SIGNATURE' not in os.environ:
        print('Missing environment variable: YOURLS_SIGNATURE')
        sys.exit(1)

    shortener = YourlsUrlShortener(os.environ.get('YOURLS_SIGNATURE'))
    print(shortener.shorten('https://xkcd.com/' + str(random.randrange(1,2500)) + '/'))
