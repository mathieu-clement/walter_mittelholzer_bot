#!/usr/bin/env python3


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
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
            return

    
    def __repr__(self):
        return 'Picture(license=%s, url=%s, filename=%s, author=%s, date=%s, title=%s, place=%s, link=%s' % (
                self.license, self.url, self.filename, self.author, self.date, self.title, self.place, self.link)



