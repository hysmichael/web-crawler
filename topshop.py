####
## TOPSHOP NEW ARRIVALS CRAWLER
####


from bs4 import BeautifulSoup
import httplib, urllib2, re
from cookielib import CookieJar
import json
import time, datetime

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

def initialize_url(url):
    page = opener.open(url)
    return BeautifulSoup(page.read())

def crawl_all_images(front_url):
    base_url = 'http://media.topshop.com/wcsstore/TopShopUS/images/catalog/'

    image_id = re.match(r'http://mediaus.topshop.com/wcsstore/TopShopUS/images/catalog/(\w+)_thumb\.jpg', front_url).group(1)
    image_count = 1
    images = ['%s%s_large.jpg' % (base_url, image_id), ]
    while True:
        path = '/wcsstore/TopShopUS/images/catalog/%s_%d_large.jpg' % (image_id, image_count + 1)
        conn = httplib.HTTPConnection('mediaus.topshop.com')
        conn.request('HEAD', path)
        response = conn.getresponse()
        conn.close()
        if response.status != 200:
            break
        image_count += 1
        images.append('%s%s_%d_large.jpg' % (base_url, image_id, image_count))

    return images

print 'Start Crawling TopShop New Arrivals'
list_page = 0
listpage = initialize_url('http://us.topshop.com/en/tsus/category/new-in-this-week-2169940/')

count = 0
data = []

def process_item(item, item_no):
    item_dict = {}
    for entry in item.select('li'):
        entry_class = entry.get('class')
        if entry_class:
            class_name = entry_class[0]
            if class_name== 'product_image':
                item_dict['url'] = entry.a['href']
                item_dict['images'] = crawl_all_images(entry.a.img['src'])
            elif class_name== 'product_description':
                item_dict['name'] = entry.a['title']
                if item_dict['name'].startswith('**'):
                    item_dict['name'] = item_dict['name'][2:]
            elif class_name == 'product_price':
                item_dict['price'] = entry.string[1:] 

    detail_page = initialize_url(item_dict['url'])
    # skip bundle items
    if detail_page.find('div', class_='bundle_description'):
        return
    
    item_dict['description'] = detail_page.find('div', class_='product_description').get_text(strip=True)
    item_dict['style_id'] = detail_page.find('li', class_='product_code').span.string

    item_dict['sizes'] = []
    sizes = detail_page.find('select', id='product_size_full')
    if sizes:
        for size_op in sizes.select('option'):
            if size_op.get('value') and size_op.get('title') == 'In stock':
                item_dict['sizes'].append(size_op['value'])

    data.append(item_dict)
    print ' + %s (%d)' % (item_dict['name'], item_no)

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M')

while True:
    list_page += 1
    print '   ---> Page: %d <---   ' % list_page

    for item in listpage.select('.product'):
        count += 1
        process_item(item, count)
    
    with open('topshop_%s.json' % st, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    nextpage_tag = listpage.find('li', attrs={'class': 'show_next'})
    if nextpage_tag:
        nextpage_url = nextpage_tag.a['href']
        listpage = initialize_url(nextpage_url)
    else:
        break

print 'All Done.'
