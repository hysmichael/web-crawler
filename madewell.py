####
## MADEWELL NEW ARRIVALS CRAWLER
####


from bs4 import BeautifulSoup
import httplib, urllib2, re
from cookielib import CookieJar
import json
import time, datetime

import requests, logging


cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

def initialize_url(url):
    page = opener.open(url)
    return BeautifulSoup(page.read())

## subdue openssl InsecurePlatformWarning warning
logging.captureWarnings(True)

print 'Start Crawling MadeWell New Arrivals'
list_page = 0
listpage = initialize_url('https://www.madewell.com/newarrivals.jsp?iNextCategory=-1')

count = 0
data = []

def issue_detail_request(item_id, referer_url, color_name=None):
    cookies = {
        'gtm_abtest': '2',
        'invited_visitor_223626': '1',
        '__sonar': '7688060882950719717',
        'BVBRANDID': '5dfcbc18-4741-4ee4-8210-0281fe2ed13a',
        '_ga': 'GA1.2.1899172858.1434067435',
        '__olapicU': '1434068713560',
        'madewell_srccode': 'PMG|G|Madewell-US-Core-B-Desktop-Exact|madewell',
        's_ev14': '%%5B%%5B%%27PMG%%257CG%%257CMadewell-US-Core-B-Desktop-Exact%%257Cmadewell%%27%%2C%%271434073446137%%27%%5D%%5D',
        'madewell_country': 'US',
        'JSESSIONID': 'wLQYVQLGy6LGdgKMMwnlvfWpQ10J01sB8fjX7z88ZVw0TQpLJnfY!-1267291119',
        'bmSessionId': 'Uf0I3g4OjoPj_d4i_dwa_AU36kDxb_/hWe_iazsfni3_29lw',
        'jcrew_wc': 'yes',
        '__utmt_UA-38295707-3': '1',
        'BTT_Collect': 'off',
        'spotifyBanner': '3',
        'productnum': '24',
        'AKSB': 's=1434486978413&r=https%%3A//www.madewell.com/newarrivals.jsp%%3FiNextCategory%%3D-1',
        '__utma': '50118458.1899172858.1434067435.1434412966.1434486854.5',
        '__utmb': '50118458.5.10.1434486854',
        '__utmc': '50118458',
        '__utmz': '50118458.1434073445.2.2.utmcsr=PMG|G|Madewell-US-Core-B-Desktop-Exact|madewell|utmgclid=CjwKEAjw4-SrBRDP483GvreDr2ASJAD5sCIuigUQviq6NvGOmHLZ8mRLPwrGOpO6OZccoi2TeVUddBoCUbfw_wcB|utmgclsrc=aw.ds|utmccn=PMG|G|Madewell-US-Core-B-Desktop-Exact|madewell|utmcmd=PMG|G|Madewell-US-Core-B-Desktop-Exact|madewell|utmctr=(not%%20provided)',
        'BTT_X0siD': '4344868554186311391',
        'bn_u': '6925705951759003429',
        'bn_cd': 'd%%26g%%26s',
        'wishlistToutShown': 'true',
        'wishlistTout': '3',
        'mt.v': '2.364213365.1434067433380',
        'BVBRANDSID': '967ae66a-1baf-4d1c-98a7-bf5b8e8e8c23',
        'firstPageLoad': 'false',
        'bmBrowserSalt': 'p6OU04xjyCTUUKY80QngNgwrVS8jIGzQ',
        's_cc': 'true',
        's_fid': '1435CA0F89C32D96-167E1C9D790B5743',
        'gpv_p41': 'PDP%%20-%%20Silk%%20Dreamdrift%%20Overlay%%20Dress%%20in%%20Palm%%20Tree%%20%%28%s%%29' % item_id,
        'SC_LINKS': '%%5B%%5BB%%5D%%5D',
        's_sq': '%%5B%%5BB%%5D%%5D',
        's_vi': '[CS]v1|2ABD10F5050114EE-40001608C0050071[CE]',
    }

    headers = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,ja;q=0.2',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2427.7 Safari/537.36',
        'Accept': '*/*',
        'Referer': referer_url,
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
    }

    url = 'https://www.madewell.com/browse2/ajax/product_details_ajax.jsp?sRequestedURL=https%%3A%%2F%%2Fwww.madewell.com%%2Fnewarrivals%%2Fcurrentfavorites%%2FPRDOVR~%s%%2F%s.jsp&isFiftyOneContext=false&isProdSellable=true&bRestrictedProduct=false&isIgnoreOutOfStock=true&prodCode=%s&color_name=%s&nav_type=PRMNAV&imgPersonalShopperWedding=&imgPersonalShopperMen=&imgSkuCode=&imgPersonalShopperKids=&imgPersonalShopperWomen=&addToBagLabel=add+to+bag&updateBagLabel=update+bag&outOfStockLabel=Out+Of+Stock&isPriceBook=false&index=0&isSaleItem=false&isSearchItem=false&variationParams=&isFromSale=false&_=1434486996498' % (item_id, item_id, item_id, color_name)

    r = requests.get(url, headers=headers, cookies=cookies)
    return r.text


def process_item(item, item_no):
    item_dict = {}

    item_dict['url'] = item.div.a['href']
    
    product_id = item['data-prodcode']
    color_name = None
    color_matchObj = re.search(r'color_name=([a-zA-Z-]+)', item_dict['url'])
    if color_matchObj:
        color_name = color_matchObj.group(1)
    if color_name == None:
        item_dict['style_id'] = product_id
    else:
        item_dict['style_id'] = '%s-%s' % (product_id, color_name)

    inner_span = item.span.span.div.div.a
    item_dict['name'] = inner_span.find('span', class_='desc_line1').string

    price_string = inner_span.find('span', class_='desc_line2').get_text(strip=True)
    if price_string[0] == '$':
        item_dict['price'] = price_string[1:]
    else:    
        ## for sale price
        item_dict['price'] = inner_span.find('span', class_='desc_line3').get_text(strip=True)[4:]
    
    
    detail_page = initialize_url(item_dict['url'])
    description_node = detail_page.find('div', class_='product_desc')
    description_list = description_node.ul.extract()
    item_dict['description'] = description_node.get_text(strip=True) + '\n' + ' '.join([li.string for li in description_list.select('li')])

    images = []
    item_dict['images'] = []
    main_image = detail_page.find('img', class_='prod-main-image')
    if main_image:
        images.append(main_image['src'])
    detail_images = detail_page.find_all('img', class_='product-detail-images')
    for img in detail_images:
        images.append(img['src'])

    for img in images:
        img = re.sub(r'\$[\w_]+\$', '$pdp_enlarge$', img)
        item_dict['images'].append(img)

    ## remove possible duplicates
    if len(item_dict['images']) >= 2 and item_dict['images'][0] == item_dict['images'][1]:
        del item_dict['images'][0]

    ## request ajax and get item size chart
    item_dict['sizes'] = []
    detail_ajax = BeautifulSoup(issue_detail_request(product_id, item_dict['url'], color_name))
    sizes = detail_ajax.select('.size-box')
    for size_div in sizes:
        if 'unavailable' not in size_div['class']:
            item_dict['sizes'].append(size_div['data-size'])

    data.append(item_dict)
    print ' + %s (%d)' % (item_dict['name'], item_no)

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M')

for item in listpage.select('.plus_product'):
    if item.get('data-prodcode'):
        count += 1
        process_item(item, count)

    if count % 20 == 0:
        with open('madewell_%s.json' % st, 'w') as outfile:
            json.dump(data, outfile, indent=4)

print 'All Done.'

with open('madewell_%s.json' % st, 'w') as outfile:
    json.dump(data, outfile, indent=4)

