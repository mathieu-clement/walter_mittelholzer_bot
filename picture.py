#!/usr/bin/env python3

import pathlib
from wand.image import Image # requires also imagemagick to be installed (native package)
from wand.api import library
from ctypes import c_void_p, c_size_t

# Tell Python's wand library about the MagickWand Compression Quality (not Image's Compression Quality)
library.MagickSetCompressionQuality.argtypes = [c_void_p, c_size_t]

class Picture:
    license = None
    url = None
    filename = None # path on file system if downloaded
    author = 'Walter Mittelholzer'
    date = None # typically a year, but could be more precise
    title = None
    place = None # e.g. Aarberg, or "Westalpen; Provence-Alpes-Côte d'Azur"
    link = None # typically DOI.org link

    def download(self, filename):
        """Downloads picture to filename and returns path"""
        raise Exception('Not implemented')


    def convert_to_jpeg(self):
        if self.filename.lower().endswith('.jpg') or self.filename.lower().endswith('.jpeg'):
            new_filename = self.filename
        else:
            new_filename = self.change_extension(self.filename, 'jpg')

        src = Image(filename=self.filename)
        convert = src.convert('jpg')
        if src.width * src.height > 1600000:
            if src.width > src.height:
                new_width = min(src.width, 1200)
                new_height = new_width / (src.width / src.height)
            else:
                new_height = min(src.height, 1200)
                new_width = new_height / (src.height / src.width)
            src.resize(int(new_width), int(new_height))
        
        library.MagickSetCompressionQuality(src.wand, 85)
        convert.save(filename=new_filename)
        self.filename = new_filename


    def change_extension(self, filename, new_extension):
        return str(pathlib.Path(filename).with_suffix('.' + new_extension))

    
    def __repr__(self):
        return 'Picture(license=%s, url=%s, filename=%s, author=%s, date=%s, title=%s, place=%s, link=%s' % (
                self.license, self.url, self.filename, self.author, self.date, self.title, self.place, self.link)



