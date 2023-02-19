#!/usr/bin/env python3

import logging
import random
import re
import tempfile
import pywikibot

from picture import Picture

class RandomPictureGenerator:
    def random_picture(self):
        pass


class WikimediaCommonsRandomPictureGenerator(RandomPictureGenerator):
    
    TITLE_EXCLUSIONS = ('File:', '.tif', '.TIF', '.jpg', '.JPG', '.jpeg', '.JPEG')
    DATE_YEAR_MONTH_PATTERN = re.compile('(19[0-3][0-9])-([01]?[0-9])')
    DATE_DAY_MONTH_YEAR_PATTERN = re.compile('([0-3]?[0-9])\.([01]?[0-9])\.(19[0-3][0-9])')
    DATE_YEAR_MONTH_DAY_PATTERN = re.compile('(19[0-9][0-9])-([01][0-9])-([0-3][0-9])')
    MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
    
    def __init__(self):
        self.logger = logging.getLogger('wm.WikimediaCommonsRandomPictureGenerator')
        site = pywikibot.Site('commons') # Wikimedia Commons
        self.top_category = pywikibot.Category(site, 'Walter Mittelholzer')
        

    def random_filepage_or_category(self, category):
        elements = list(category.members(recurse=0, member_type=['subcat', 'file']))
        if not elements:
            return None

        return elements[random.randrange(len(elements))]


    def random_filepage(self, category):
        # return a random member from the category
        element = self.random_filepage_or_category(category)

        if self.is_category(element):
            self.logger.info('Entering category "%s"', element.title().replace('Category:', ''))
            return self.random_filepage(element)
        elif self.is_filepage(element):
            return element
        else:
            raise Exception('Unknown element: ' + element)


    def is_category(self, obj):
        return isinstance(obj, pywikibot.Category)
        #return obj.is_categorypage()


    def is_filepage(self, obj):
        return isinstance(obj, pywikibot.FilePage)
        #return obj.is_filepage()


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
        title = self.extract_title(metadata, filepage)
        place = metadata['depicted place'] if 'depicted place' in metadata else None
        date = self.extract_date(metadata)

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


    def extract_title(self, metadata, filepage):
        title  = metadata['title'] if 'title' in metadata else filepage.title()
        self.logger.debug('Title before cleaning: %s', title)

        if title:
            if '}}' in title:
                title = title.split('}}')[0]

            if 'LBS' in title:
                title = title.split('LBS')[0]

            for exclusion in self.TITLE_EXCLUSIONS:
                title = title.replace(exclusion, '')

            title = title.strip()

        return title


    def extract_date(self, metadata):
        date  = metadata['date'] if 'date' in metadata else None
        self.logger.info('Date: %s', date)
        if date:
            if 'Taken on' in date:
                self.logger.debug("date taken on: %s" % date)
                date = date.split('|')[1]
            elif 'date|between' in date: # {{other date|between|1930|1931}}
                start, end = date.replace('{{','').replace('}}','').split('|')[2:4]
                if start != end:
                    date = "%s - %s" % (start, end)
                else:
                    date = start
            elif 'date|ca|' in date: # {{other date|ca|1934-2}}
                date = date.split('date|ca|')[1].replace('}}', '')
            elif 'date|~|' in date: # {{other date|~|1935}}
                date = date.split('date|~|')[1].replace('}}', '')

            date = self.extract_year_month(date)

        self.logger.info('Clean date: %s', date)
        return date


    def extract_year_month(self, date):
        # Extract month if format is "YYYY-MM" or "YYYY-M"
        try:
            
            if match := self.DATE_YEAR_MONTH_PATTERN.fullmatch(date): # 1925-02 or 1925-2
                year = match.group(1)
                month_number = int(match.group(2))
                month = self.MONTHS[month_number - 1]
                return '%s %s' % (month, year)
            elif match := self.DATE_DAY_MONTH_YEAR_PATTERN.fullmatch(date): # 1.3.1920 (incl. 0 before day and/or month)
                return self.as_human_date(match.group(1), match.group(2), match.group(3))
            elif match := self.DATE_YEAR_MONTH_DAY_PATTERN.fullmatch(date): # 1925-12-31
                return self.as_human_date(match.group(3), match.group(2), match.group(1))
            else:
                return date
        except Exception as e:
            self.logger.error('Error while processing date "%s"', date, exc_info=e)
            return date


    def as_human_date(self, day, month, year):
        return '%d %s %s' % (int(day), self.MONTHS[int(month) - 1], year) 


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
    print(gen.extract_year_month('1923-12-31'))
