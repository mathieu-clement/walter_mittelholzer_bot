#!/usr/bin/env python3

import os.path

class PublishedImagesDatabase:
    def add(self, picture):
        pass

    def is_published(self, picture):
        pass


class FileBasedPublishedImagesDatabase(PublishedImagesDatabase):
    def __init__(self, filename='published_images.txt'):
        self.filename = filename
        self.image_urls = []

        # Read file
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                for url in f:
                    self.image_urls.append(url.replace('\n',''))


    def add(self, picture):
        self.write_line(picture.url)
        self.image_urls.append(picture.url)


    def write_line(self, line):
        with open(self.filename, 'a') as f:
            f.write("%s\n" % line)


    def is_published(self, picture):
        return picture.url in self.image_urls

