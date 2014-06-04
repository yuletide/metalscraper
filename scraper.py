import scraperwiki
import json
import requests
import re
import lxml.html
from time import sleep
from random import random
from datetime import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6'}

genres = ('heavy', 'black', 'death', 'doom', 'thrash', 'speed', 'folk', 'power', 'prog', 'electronic', 'gothic', 'orchestral', 'avantgarde')

genre_root = 'http://www.metal-archives.com/browse/ajax-genre/g/'

GENRE_CACHE_DAYS = 60

def scrape_genre(genre):
    suffix = genre + '/json/?sEcho=1&iDisplayStart=0'
    r = requests.get(genre_root + suffix, headers=headers)
    page = json.loads(r.text)
    count = page['iTotalRecords']

    pages = count / 500
    if not count % 500: pages -= 1
    if not check_cache(genre, 0):
        print "not cached, processing json"
        process_json(page, genre)
        cache_page(genre, 0) 
    for i in range(1,pages):
        if not check_cache(genre, i): 
            if scrape_genre_page(genre, i):
                cache_page(genre, i)
            else:
                print 'something prevented caching'
        else:
            print 'already scraped! ' + genre + str(i)
    #scrape_genre_page(genre, pages-1)
    #scrape_genre_page(genre, pages) # just in case
    scrape_genre_page(genre, pages+1) # never cache the last page

def scrape_genre_page(genre, page):
    print "scraping genre page ", genre, page
    suffix = genre + '/json/?sEcho=1&iDisplayStart=' + str(500 * page)
    #print suffix
    r = requests.get(genre_root + suffix, headers=headers)
    if r.text: 
        json_obj = json.loads(r.text)
        process_json(json_obj, genre)
        return True
    else:
        print "no request body! ", str(r)
        return False

def process_json(page, genre):
    for item in page['aaData']:
        link=re.sub('<a href=\'(.*)\'>(.*)</a>', '\\1|\\2', item[0]).split('|')
        id = link[0].split('/')[5]
        band = {}
        band['name'] = link[1]
        band['link'] = link[0]
        band['country'] = item[1]
        band['genre'] = item[2]
        band['id'] = id
        band['category'] = genre
        #print bands[str(id)]
        scraperwiki.sqlite.save(unique_keys=['id'], data=band)

def cache_page(genre, page):
    print "caching ", genre+" "+str(page)
    scraperwiki.sqlite.save_var(genre+str(page), datetime.now().strftime("%c"))

def check_cache(genre, page):
    val = scraperwiki.sqlite.get_var(genre+str(page))
    print "checking cache " + str(val)
    if val == None or val == 1:
        return False
    else:
        try:
            d = datetime.strptime(val, "%c")
            return (datetime.now() - d).days < GENRE_CACHE_DAYS
        except:
            print "error parsing date"
            return False

def scrape_bands(limit=''):
    if limit: limit = " LIMIT " + str(limit)
#    bands = scraperwiki.sqlite.select("* FROM data where scraped IS NULL OR scraped == '0'" + limit)
    bands = scraperwiki.sqlite.select("* FROM data where id==5678")
    print bands
    for band in bands:
        scrape_band(band)
        sleep(random())

def get_scraped_bands(limit=''):
    if limit: limit = " LIMIT " + str(limit)
    return scraperwiki.sqlite.select("* FROM data where scraped IS NOT NULL and scraped <> '0' ORDER BY scraped DESC" + limit)

def get_failed_bands(limit=''):
    if limit: limit = " LIMIT " + str(limit)
    return scraperwiki.sqlite.select("* FROM data where scraped == '-1'")

def scrape_band(band):
    print 'scraping band '+ band['name']
    if band['link']:
        r = requests.get(band['link'])
        if r.status_code == 200 and r.text:
            root = lxml.html.fromstring(r.text)
            keys = map(lambda x: x.text_content()[:-1], root.cssselect('dt'))
            vals = map(lambda x: x.text_content(), root.cssselect('dd'))
            print vals
            for i,key in enumerate(keys):
                if key == 'Location':
                    band['location'] = vals[i]
                    band['location_utf'] = vals[i].encode('ISO-8859-1').decode('utf-8')
                elif key == 'Status':
                    band['status'] = vals[i]
                elif key == 'Year of creation':
                    band['year'] = vals[i]
                elif key == 'Lyrical themes':
                    band['themes'] = vals[i]
                elif key == 'Current label':
                    band['current_label'] = vals[i]
            save_band(band)
            return True
    save_band_failed(band)
    return False
    
def save_band(band):
    print 'scrape successful ' + band['id']
    band['scraped'] = datetime.now()
    scraperwiki.sqlite.save(unique_keys=['id'], data=band)

def save_band_failed(band):
    print 'scrape failed '+band['id']
    band['scraped'] = '-1'
    scraperwiki.sqlite.save(unique_keys=['id'], data=band)

def clear_band_cache(bands):
    for band in bands:
        band['scraped'] = None
        scraperwiki.sqlite.save(unique_keys=['id'], data=band)

def get_band_by_id(id):
    records = scraperwiki.sqlite.select("* from data WHERE id="+str(id))
    if len(records): return records[0]

#to test encoding
#scrape_band(get_band_by_id(5678))

''' band ajax points 
root: http://www.metal-archives.com/band/view/id/3540277491
$('dt') for headers
$('dd') for values

members: $('div#band_tab_members_current')
discography: http://www.metal-archives.com/band/discography/id/3540277491/tab/all
recommendations: http://www.metal-archives.com/band/ajax-recommendations/id/3540277491
links: http://www.metal-archives.com/link/ajax-list/type/band/id/3540277491

'''
'''
scrape_bands(500)
sleep(500)
scrape_bands(500)


print "failed bands: "
print get_failed_bands()
print "scraped bands: "
print get_scraped_bands()
#clear_band_cache(get_failed_bands())

for genre in genres:
    scrape_genre(genre)
'''
scrape_genre('black')



