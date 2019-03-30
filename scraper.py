import scraperwiki
import json
import requests
import re
import lxml.html
from time import sleep
from time import time
from random import random
from datetime import datetime
from mapbox import Geocoder
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

headers = {'User-Agent': 'Mozilla/5.0 (Windows) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
genres = ('heavy', 'black', 'death', 'doom', 'thrash', 'speed', 'folk', 'power', 'prog', 'electronic', 'gothic', 'orchestral', 'avantgarde')

genre_root = 'https://metal-archives.com/browse/ajax-genre/g/'

GENRE_CACHE_DAYS = 0

geocoder = Geocoder(name='mapbox.places-permanent')

def scrape_genre(genre):
    suffix = genre + '/json/?sEcho=1&iDisplayStart=0'
    r = requests.get(genre_root + suffix, headers=headers)
    page = json.loads(r.text)
    count = page['iTotalRecords']
    pages = count // 500
    if not count % 500: pages -= 1

    for i in range(0, pages+1):
        if not check_cache(genre, i): 
            if scrape_genre_page(genre, i):
                cache_page(genre, i)
            else:
                print('something prevented caching')
        else:
            print('already scraped! ' + genre + str(i))
    #scrape_genre_page(genre, pages-1)
    #scrape_genre_page(genre, pages) # just in case
    #scrape_genre_page(genre, pages+1) # never cache the last page

def scrape_genre_page(genre, page):
    print ("scraping genre page ", genre, page)
    suffix = genre + '/json/?sEcho=1&iDisplayStart=' + str(500 * page)
    print (suffix)
    r = requests.get(genre_root + suffix, headers=headers)
    try: 
        json_obj = json.loads(r.text)
        process_json(json_obj, genre)
        return True
    except:
        print ("error parsing JSON or no request body! ", str(r))
        return False

def process_json(page, genre):
    for item in page['aaData']:
        link=re.sub('<a href=\'(.*)\'>(.*)</a>', '\\1|\\2', item[0]).split('|')
        # print(link)
        id = link[0].split('/')[5]
        band = get_band_by_id(id) or {}
        # print(band)
        band['name'] = link[1]
        band['link'] = link[0]
        band['country'] = item[1]
        band['genre'] = item[2]
        band['id'] = id
        band['genre_parent'] = genre # this is broken since bands can be on multiple genre pages
        band['genre_' + genre] = 1
        band['category'] = genre
        print(band)
        scraperwiki.sqlite.save(unique_keys=['id'], data=band)

def cache_page(genre, page):
    return True
    print("caching ", genre+" "+str(page))
    scraperwiki.sqlite.save_var(genre+str(page), datetime.now().strftime("%c"))
    print('wtf')

def check_cache(genre, page):
    return False
    val = scraperwiki.sqlite.get_var(genre+str(page))
    print("checking cache: " + str(val))
    if val == None or val == 1:
        return False
    else:
        try:
            d = datetime.strptime(val, "%c")
            return (datetime.now() - d).days < GENRE_CACHE_DAYS
        except:
            print ("error parsing date")
            return False

def scrape_bands(limit=''):

    if limit: limit = " LIMIT " + str(limit)
    bands = scraperwiki.sqlite.select("* FROM swdata where scraped IS NULL OR scraped == '0' OR scraped == '-1'" + limit)
    for band in bands:
        scrape_band(band)
        sleep(random()*2)

def get_scraped_bands(limit=''):
    if limit: limit = " LIMIT " + str(limit)
    return scraperwiki.sqlite.select("* FROM swdata where scraped IS NOT NULL and scraped <> '0' ORDER BY scraped DESC" + limit)

def get_failed_bands(limit=''):
    if limit: limit = " LIMIT " + str(limit)
    return scraperwiki.sqlite.select("* FROM swdata where scraped == '-1'")

def get_NA_bands():
    return scraperwiki.sqlite.select("* from swdata where location_utf = 'N/A'")

def scrape_band(band):
    print ('scraping band '+ band['id'])
    if band['link']:
        print(band['link'])
        driver.get(band['link'])
        try: 
            driver.find_element_by_class_name('band_name')
        except NoSuchElementException:
            body = driver.find_element_by_tag_name('body')
            if body.text == 'Forbidden.':
                print('Rate limited')
                sleep(60)
                return scrape_band(band)
            else: 
                print('Not a valid band page')
                save_band_failed(band)
                return False
        
        keys = list(map(lambda x: x.text[:-1], driver.find_elements_by_tag_name('dt')))
        vals = list(map(lambda x: x.text, driver.find_elements_by_tag_name('dd')))
        for i,key in enumerate(keys):
            if key == 'Location':
                band['location'] = vals[i]
                band['location_utf'] = vals[i]#.encode('ISO-8859-1').decode('utf-8')
                # print(band['location_utf'])
            elif key == 'Status':
                band['status'] = vals[i]
            elif key == 'Formed in':
                band['year'] = vals[i]
            elif key == 'Years active':
                band['years_active'] = vals[i]
            elif key == 'Lyrical themes':
                band['themes'] = vals[i]
            elif key == 'Current label':
                band['current_label'] = vals[i]
            elif key == 'Last label':
                band['current_label'] = vals[i]
        band['comment'] = driver.find_element_by_class_name('band_comment').text
        save_band(band)
        geocode_band(band)
        return True
    save_band_failed(band)
    return False
    
def save_band(band):
    print ('scrape successful ' + band['id'])
    band['scraped'] = datetime.now()
    band['scraped_timestamp'] = time()
    scraperwiki.sqlite.save(unique_keys=['id'], data=band)

def save_band_failed(band):
    print ('scrape failed '+band['id'])
    band['scraped'] = '-1'
    scraperwiki.sqlite.save(unique_keys=['id'], data=band)
    
def save_geocode(band):
    print ('geocode successful ' + band['id'])
    band['geocoded'] = datetime.now()
    scraperwiki.sqlite.save(unique_keys=['id'], data=band)

def save_geocode_failed(band):
    print('geocode failed '+str(band))
    if band['location_utf'] == 'N/A':
        band['geo_place_name'] = 0
    else:
        band['geo_place_name'] = '-1'
    band['geocoded'] = None
    scraperwiki.sqlite.save(unique_keys=['id'], data=band)

def clear_bands_by_ids(ids):
    print(ids)
    bands = list(map(lambda x: get_band_by_id(x), ids))
    print(bands)
    clear_band_cache(bands)
    
def clear_band_cache(bands):
    for band in bands:
        print('Clearing band '+band['id'])
        band['scraped'] = None
        scraperwiki.sqlite.save(unique_keys=['id'], data=band)

def get_band_by_id(id):
    records = scraperwiki.sqlite.select("* from swdata WHERE id="+str(id))
    if len(records): return records[0]

def clean_old_placenames():
    records = scraperwiki.sqlite.select("* from data WHERE location IS NOT NULL and location_utf is NULL")
    for band in records:
        band['location_utf'] = band['location'].encode('ISO-8859-1').decode('utf-8')
        scraperwiki.sqlite.save(unique_keys=['id'], data=band)

def get_ungeocoded_bands(limit=''):
    if limit: limit = " LIMIT " + str(limit)
    # return scraperwiki.sqlite.select("data.* from data INNER JOIN swdata ON data.id = swdata.id WHERE geo_center IS NULL and data.location_utf IS NOT NULL and data.location_utf <> 'N/A'")
    return scraperwiki.sqlite.select("* from swdata WHERE geo_place_name IS NULL and location_utf IS NOT NULL and location_utf <> 'N/A'")
    
def geocode_weird_names():
    for band in scraperwiki.sqlite.select("* from swdata WHERE location_utf LIKE '%;%'"):
        geocode_band(band)

def geocode_band(band):
    print("Geocoding band "+band['id'])
    types = ('place', 'locality', 'region', 'district')

    if band['location_utf'] == 'N/A':
        save_geocode_failed(band)
        return False

    if band['location_utf'] and band['country']:
        location = band['location_utf']

        print(location)
        if '(early)' in location:
            print('Complex location - early')
            location = location.split('(early)')[0] # take the original location or the later one?
            print('cleaned location '+location)    
        if ';' in location:
            print('Complex location - ;')
            location = location.split(';')[0]
            print('cleaned location '+location)    
        if '/' in location:
            print('Complex location - /')
            location = location.split('/')[0]
            print('cleaned location '+location)    

        # TODO geocode both early and later? Make this smarter
        query = location + ', ' + band['country']
        response = geocoder.forward(query, types=types)
        collection = response.json()
        # print(collection)
        # print('\n')
        # print(collection['features'])
        if len(collection['features']):
            feature = collection['features'][0]
            # print('feature\n')
            # print(feature)
            if 'id' in feature: 
                band['geo_place_id'] = feature['id']
            band['geo_place_name'] = feature['place_name']
            band['geo_place_type'] = feature['place_type'][0]
            band['geo_relevance'] = feature['relevance']
            band['geo_center'] = str(feature['center'])
            band['geo_geom'] = str(feature['geometry'])
            band['geo_properties'] = str(feature['properties'])
            if 'context' in feature:
                band['geo_context'] = str(feature['context'])
            save_geocode(band)
            return True
        else: 
            print('no geocode results')
            save_geocode_failed(band)
            return False
    else: 
        print("Band missing location field"+str(band))
        save_geocode_failed(band)
        return False

''' band ajax points 
root: http://www.metal-archives.com/band/view/id/3540277491
$('dt') for headers
$('dd') for values

members: $('div#band_tab_members_current')
discography: http://www.metal-archives.com/band/discography/id/3540277491/tab/all
recommendations: http://www.metal-archives.com/band/ajax-recommendations/id/3540277491
links: http://www.metal-archives.com/link/ajax-list/type/band/id/3540277491

'''


# geocode_band(get_band_by_id(5678))

# for band in get_NA_bands():
#     save_geocode_failed(band)

for genre in genres:
    scrape_genre(genre)


try: 
    for band in get_ungeocoded_bands():
        geocode_band(band)
    driver = webdriver.Firefox()
    scrape_bands(1000)
    sleep(50)
    scrape_bands(5000)
    sleep(500)
    scrape_bands(5000)
    sleep(500)
    scrape_bands(5000)
except KeyboardInterrupt:
    print('Scrape Aborted')
    driver.quit()

# geocode_weird_names()







