#!/usr/bin/env python3

import logging
import random
import tempfile
import pywikibot

from picture import Picture

class RandomPictureGenerator:
    def random_picture(self):
        pass


class WikimediaCommonsRandomPictureGenerator(RandomPictureGenerator):
    
    def __init__(self):
        self.logger = logging.getLogger('wm.WikimediaCommonsRandomPictureGenerator')
        site = pywikibot.Site('commons') # Wikimedia Commons
        self.top_category = pywikibot.Category(site, 'Walter Mittelholzer')
        

    def random_filepage_or_category(self, category):
        elements = list(category.members(recurse=0, member_type=['subcat', 'file']))
        if not elements:
            return None

        return elements[random.randrange(len(elements) - 1)]


    def random_filepage(self, category):
        # return a random member from the category
        element = self.random_filepage_or_category(category)

        if self.is_category(element):
            return self.random_filepage(category)
        elif self.is_filepage(element):
            return element
        else:
            raise Exception('Unknown element: ' + element)


    def is_category(self, obj):
        #return isinstance(obj, pywikibot.Category)
        return obj.is_categorypage()


    def is_filepage(self, obj):
        #return isinstance(obj, pywikibot.FilePage)
        return obj.is_filepage()


    def random_picture(self):
        # Starts from top category
        # then chooses a file at random
        element = self.random_filepage(self.top_category)

        # convert to Picture object
        return self.get_picture(element)


    def get_picture(self, filepage):
        license = 'Public domain'
        url = filepage.get_file_url()
        file = tempfile.NamedTemporaryFile()
        filename = file.name
        download = filepage.download

        metadata = self.extra_metadata(filepage.get())
        self.logger.debug(filepage.get())
        place = metadata['depicted place'] if 'depicted place' in metadata else None
        date  = metadata['date'] if 'date' in metadata else None
        if date is not None and 'Taken on' in date:
            self.logger.debug("date taken on: %s" % date)
            date = date.split('|')[1]
        if date is not None and 'date|between' in date:
            start, end = date.replace('{{','').replace('}}','').split('|')[2:4]
            date = "%s - %s" % (start, end)
        title  = metadata['title'] if 'title' in metadata else None
        if title is not None and '}}' in title:
            title = title.split('}}')[0]
        if title is not None and 'LBS' in title:
            title = title.split('LBS')[0]

        if title is None:
            title = filepage.title().replace('File:', '').replace('.tif', '').replace('.TIF', '').replace('.jpg','').replace('.JPG', '').replace('.jpeg','').replace('.JPEG', '')

        picture = Picture()
        picture.url = url
        picture.filename = filename
        picture.download = download
        picture.date = date
        picture.title = title
        picture.place = place
        picture.link = filepage.full_url()
        #picture.link = self.extract_doi_link(filepage.get())

        return picture


    def extract_doi_link(self, text):
        raw = [w for w in text.split(' ') if 'doi.org' in w and 'Template' in w]
        if not raw:
            return None
        return raw[0].split('{{')[0]


    def extra_metadata(self, raw):
        cleaned_fields = [p.replace('\n', '').strip() 
                          for p in raw.split(' | ') 
                          if p[0] >= 'a' 
                          and p[0] <= 'z' 
                          and not p.startswith('gwtoolset')]
        metadata = dict()
        for field in cleaned_fields:
            spl = field.split(' = ')
            if len(spl) == 2:
                name, value = field.split(' = ')
                metadata[spl[0]] = spl[1]

        return metadata



if __name__ == '__main__':

    gen = WikimediaCommonsRandomPictureGenerator()
    print(gen.random_picture())
