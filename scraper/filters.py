import re
from datetime import datetime, timedelta
from pytz import timezone

def image_id(complete_image_link):
    regex_a = '(?<=I\/)(.*)(?=\.jpg)'
    image_link_a = re.search(regex_a, complete_image_link)

    if not image_link_a:
        image_id = complete_image_link
    else:
        image_id = image_link_a.group()
    
    return image_id

def product_id(complete_product_link):
    regex_a = '(?<=dp\/)(.+)(?=\/ref)'
    regex_b = '(?<=dp\/)(.+)(?=\?)'

    product_link_a = re.search(regex_a, complete_product_link)
    if product_link_a is None:

        product_link_b = re.search(regex_b, complete_product_link)
        if product_link_b is None:
            product_id = complete_product_link
        else:
            product_id = product_link_b.group()
    else:
        product_id = product_link_a.group()
    
    return product_id

def scrap_boxes(boxes, domain, dict_to_rows=False):
    
    ranks = [None]*50
    product_names = [None]*50
    image_urls = [None]*50
    product_links = [None]*50
    star_ratings = [None]*50
    reviews = [None]*50
    authors_companies = [None]*50
    editions_consoles = [None]*50
    min_prices = [None]*50
    max_prices = [None]*50
    time_log = [None]*50

    amz_mx_url = f'https://www.amazon.com.{domain}'
    
    n_box = 0
    for box in boxes:
        MX__COL_tz = 'America/Mexico_City'
        timezone_MXCOL = timezone(MX__COL_tz) 
        datetime_box = datetime.now(timezone_MXCOL)
        time_log[n_box] = datetime_box.strftime('%Y-%m-%d %H:%M')

        rank_box = box.find_all('span', attrs={'class':'zg-badge-text'})
        products_and_image_box = box.find_all('div', attrs={'class' : 'a-section a-spacing-small'})
        product_links_box = box.find_all('a', attrs={'class' : 'a-link-normal'})
        star_ratings_box = box.find_all('span', attrs={'class' : 'a-icon-alt'})
        reviews_box = box.find_all('a', attrs={'class' : 'a-size-small a-link-normal'})
        authors_company_box = box.find_all('span', attrs={'class' : 'a-size-small a-color-base'})
        editions_console_box = box.find_all('span', attrs={'class' : 'a-size-small a-color-secondary'})
        prices_box = box.find_all('span', attrs={'class' : "p13n-sc-price"})
        
        
        ranks[n_box] = int(rank_box[0].get_text()[1:])

        #In case the element was removed (yes, it happens)
        try:
            product_names[n_box] = products_and_image_box[0].img.get('alt')
        except: pass

        try:
            complete_product_link = product_links_box[0].get('href')
            product_links[n_box] = product_id(complete_product_link)
        except: pass

        try:
            complete_image_id = products_and_image_box[0].img.get('src')
            image_urls[n_box] = image_id(complete_image_id)
        except: pass

        try:
            if domain == 'mx':
                star_ratings[n_box] = float(star_ratings_box[0].get_text()[:3])
                reviews[n_box] = int(reviews_box[0].get_text().replace(',',''))

            elif domain == 'br':
                star_ratings[n_box] = float(star_ratings_box[0].get_text()[:3].replace(',','.'))
                reviews[n_box] = int(reviews_box[0].get_text().replace('.',''))
        except: pass
        #Individual cases
        try:
            authors_companies[n_box] = authors_company_box[0].get_text()
        except:pass
        
        try:
            editions_consoles[n_box] = editions_console_box[0].get_text()
        except:pass

        #Courrencies
        if domain == 'mx':
            coin_symbol = 1
        elif domain == 'br':
            coin_symbol = 2

        try:
            if domain == 'mx':
                min_prices[n_box] = float(prices_box[0].get_text()[coin_symbol:].replace(',',''))
            elif domain == 'br':
                min_prices[n_box] = float(prices_box[0].get_text()[coin_symbol:].replace('.','').replace(',','.'))
        except: pass

        try:    
            if domain == 'mx':
                max_prices[n_box] = float(prices_box[1].get_text()[coin_symbol:].replace(',',''))
            elif domain == 'br':
                max_prices[n_box] = float(prices_box[1].get_text()[coin_symbol:].replace('.','').replace(',','.'))
        except: pass

        n_box = n_box + 1 

    # Dictionary
    boxes_dict = {
    'time' : time_log,
    "Rank" : ranks,
    "Product Names": product_names,
    "Product ID": product_links,
    "Image ID": image_urls,
    "Stars": star_ratings,
    "Reviews": reviews,
    "Authors/Company": authors_companies,
    "Edition/Console": editions_consoles,
    "Price_std_or_min" : min_prices,
    "Max_prices" : max_prices
    }

    if dict_to_rows == True:
        dict_rows = [None]*50
        for n in range(len(dict_rows)):
            dict_rows[n] = [
                boxes_dict["time"][n],
                boxes_dict["Rank"][n],
                boxes_dict["Product Names"][n],
                boxes_dict["Product ID"][n],
                boxes_dict["Image ID"][n],
                boxes_dict["Stars"][n],
                boxes_dict["Reviews"][n],
                boxes_dict["Authors/Company"][n],
                boxes_dict["Edition/Console"][n],
                boxes_dict["Price_std_or_min"][n],
                boxes_dict["Max_prices"][n]]

        return boxes_dict, dict_rows
    else:
        return boxes_dict