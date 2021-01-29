headers_0 = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64;x64; rv:66.0) Gecko/20100101 Firefox/66.0",
           "Accept-Encoding":"gzip, deflate",
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "DNT":"1",
           "Connection":"close",
           "Upgrade-Insecure-Requests":"1"}

headers_1 = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15",
           "Accept-Encoding":"gzip, deflate",
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "DNT":"1",
           "Connection":"close",
           "Upgrade-Insecure-Requests":"1"}

headers_2 = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
           "Accept-Encoding":"gzip, deflate",
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "DNT":"1",
           "Connection":"close",
           "Upgrade-Insecure-Requests":"1"}

headers_tuple = (headers_1, headers_1, headers_2)

mx_dict = {
    'top_food_and_drinks':'grocery',
    'top_automotive':'automotive',
    'top_baby':'baby',
    'top_sports':'sports',
    'top_amazon_devices':'amazon-devices',
    'top_electronics':'electronics',
    'top_tools':'tools',
    'top_kitchen':'kitchen',
    'top_industrial_emp_cience':'industrial',
    'top_musical_instruments':'musical-instruments',
    'top_toys':'toys',
    'top_books':'books',
    'top_music':'music',
    'top_officeproduct':'officeproduct',
    'top_movies':'dvd',
    'top_handmade':'handmade',
    'top_pet_supplies':'pet-supplies',
    'top_fashion':'shoes',
    'top_health':'hpc',
    'top_software':'software',
    'top_kindle':'digital-text',
    'top_videogames':'videogames'
    }

br_dict = {
    'top_amazon_devices':'amazon-devices',
    'top_automotivo': 'automotive',
    'top_food_and_drinks':'grocery',
    'top_baby':'baby-products',
    'top_sports':'sports',
    'top_electronics':'electronics',
    'top_tools':'hi',
    'top_kitchen':'kitchen',
    'top_toys':'toys',
    'top_books':'books',
    'top_music':'music',
    'top_officeproduct':'office',
    'top_movies':'dvd',
    'top_pet_supplies':'pet-products',
    'top_fashion':'fashion',
    'top_health':'hpc',
    'top_software':'computers',
    'top_kindle':'digital-text',
    'top_videogames':'videogames',
    'top_apps':'mobile-apps',
    'top_beauty':'beauty',
    'top_home':'home',
    'top_home_appliances':'appliances',
    'top_pool_garden':'lawn-and-garden',
    'top_furniture':'furniture'
}

domain_dict = {'Mexico' : 'mx',
               'Brazil' : 'br'}

domain_path = '4SS/4SS_db/testing/{}'

in_box = {'tuples' : headers_tuple,
          'dictionaries' : [mx_dict, br_dict, domain_dict],
          'paths' : domain_path}

def start_log(n_spaces):
    log = {'status' : [None]*n_spaces,
       'date' : [None]*n_spaces,
       'domain' : [None]*n_spaces,
       'category' :[None]*n_spaces
       }
    
    return log
