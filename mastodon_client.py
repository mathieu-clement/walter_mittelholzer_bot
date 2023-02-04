#!/usr/bin/env python3

import logging
from mastodon import Mastodon


class MastodonClient:
    def __init__(self, access_token):
        self.logger = logging.getLogger('wm.MastodonClient')
        self.logger.setLevel(logging.DEBUG)
        self.mastodon = Mastodon(access_token=access_token, api_base_url = 'https://mastodon.citrouille.ch')


    def toot(self, picture):
        status = 'Picture of the Day\n\n'

        if picture.title:
            status = status + 'Title: %s\n' % picture.title
        
        if picture.place:
            status = status + 'Location: %s\n' % picture.place

        if picture.date:
            status = status + 'Date: %s\n' % picture.date

        if picture.link:
            status = status + 'Source: %s\n' % picture.link

        self.logger.info("Status: %s" % status)
        
        media_dict = self.mastodon.media_post(picture.filename, mime_type='image/jpeg') 
        self.logger.info("Media Post: %s" % media_dict)

        return self.mastodon.status_post(status, media_ids=[media_dict], visibility='public', language='eng')
