# Scraper build
from scraper.filters import *
from scraper.objects import *
from scraper.scrap_tools import *
from scraper.printer import *

# Manage of time
from datetime import datetime, timedelta
from pytz import timezone

# Data management
import pandas as pd

def scrap_amazon_times(n_times, minutes):
    counter = 0
    for t in range(n_times):
        for min in range(minutes):
            print(min, end='')
            line_jump = 0
            for wait in range(3):
                time.sleep(15)
                print('.', end='')
                if (min > 0) and (min % 20 == 0) and (line_jump == 0):
                    line_jump = 1
                    print('\n')
        
        print(f'\nScrap No: {counter + 1}\n')
        scrap_amazon()
        counter = counter + 1

def scrap_amazon():
    MX__COL_tz = 'America/Mexico_City'
    timezone_MXCOL = timezone(MX__COL_tz) 

    Start_datetime = datetime.now(timezone_MXCOL)
    Start_datetime = Start_datetime.strftime('%Y-%m-%d %H_%M')
    centered_date = centered_string(Start_datetime)

    n_log = 0
    country_count = 0

    print(f'      Log Date    | Country |        category       | header | status | Loaded |')

    for country_name in domain_dict:
        country = domain_dict[country_name]

        if country == 'mx':
            categories_dict = mx_dict
            n_spaces = 45

        elif country == 'br':
            categories_dict = br_dict
            n_spaces = 47

        log_status = [None]*n_spaces
        log_date = [None]*n_spaces
        log_domain = [None]*n_spaces
        log_category = [None]*n_spaces
        n_header = 0

        country_count = country_count + 1

        if country_count > 1:
            print(' ---------------- | ------- | --------------------- | ------ | ------ | ------ |')


        for key in categories_dict:
            #Date-time
            log_datetime = datetime.now(timezone_MXCOL)
            log_date[n_log] = log_datetime.strftime('%Y-%m-%d %H:%M')
            print(f' {log_date[n_log]}', end=' | ')
            
            #Country where you are at
            log_domain[n_log] = country
            print(f'   {log_domain[n_log]}  ', end=' | ')

            #Category that is scraping
            category = categories_dict[key]
            log_category[n_log] = category
            centered_category = centered_string(log_category[n_log])
            print(centered_category, end=' | ')
            
            #The main scrap
            url = f'https://www.amazon.com.{country}/gp/bestsellers/{category}/ref=zg_bs_nav_0'

            
            print(f'  {n_header}   ', end=' | ')

            soup, status = extract_soup(url,n_header, preview=False)
            n_header += 1
            if n_header > 2:
                n_header = 0

            if status == 503:
                while status == 503:
                    time.sleep(1)
                    soup, status = extract_soup(url, preview=False)
                    log_status[n_log] = status
                    log_date[n_log] = datetime.now()

            if status ==200:
                log_status[n_log] = status
                print(f'  {log_status[n_log]} ', end=' | ')
                
                boxes = top_amazon_boxes(soup)
                amz_key_top_boxes, amz_rows = scrap_boxes(boxes, country, dict_to_rows=True)
                add_df = pd.DataFrame.from_dict(amz_key_top_boxes)

                #Updating Parquet files
                new_file = False
                bdb = f'{country}-{category}.parquet'
                dir_parquet_maindb = f'DB/{country}/parquet/{bdb}'
                try:
                    ''' Here it knows if it's going to create a new one from scratch
                    If this brings an error is because there's nothing, because you're a stranger
                    And I want you to create your own records ;) it's ok'''
                    main_df = pd.read_parquet(dir_parquet_maindb)
                except:
                    # Yeap, nice to meet you
                    new_file = True

                if new_file == True:
                    # Now it knows that you add all to zero, don't worry
                    main_df = add_df
                else:
                    # Yes, it's the unique difference
                    main_df = pd.concat([main_df, add_df])
                
                #case of NaN values
                main_df['Rank'] = pd.to_numeric(main_df['Rank'], downcast='float')

                parquet_file = f'{country}_{category}.parquet'
                dir_parquet_maindb = f'DB/{country}/parquet/{parquet_file}'
                #Updating  file
                main_df.to_parquet(dir_parquet_maindb)

                excel_file = f'{country}_{category}.xlsx'
                dir_excel_maindb = f'DB/{country}/excel/{excel_file}'
                #For the testing
                main_df.to_excel(dir_excel_maindb, index=False)

                print('  Yes  |')

            else:
                log_status[n_log] == status
                print(f'  {log_status[n_log]} ', end=' | ')
                
                log_date[n_log] = datetime.now()
                print(' +.No.+ |')

            n_log = n_log + 1

    log_dict = {
        'log_date' : log_date,
        'category' : log_category,
        'country' : log_domain,
        'status' : log_status
    }


    dict_rows= [
        log_date,
        log_category,
        log_domain,
        log_status]

    log_file = f'db_logs.csv'
    dir_log_testing = f'DB/logs/{log_file}'

    try:
        update_csv(dir_log_testing, log_rows, sep='|')
    except:
        log_df = pd.DataFrame.from_dict(log_dict)
        log_df.to_csv(dir_log_testing, index = False)



    log_print = """
                                ----------------------
                                |   Log file loaded   |
                                ----------------------

    """
    print(log_print)

def test_scrap_amazon(country):
    if country == 'mx':
        categories_dict = mx_dict
        n_spaces = 45

    elif country == 'br':
        categories_dict = br_dict
        n_spaces = 47

    log_status = [None]*n_spaces
    log_date = [None]*n_spaces
    log_domain = [None]*n_spaces
    log_category = [None]*n_spaces
    n_header = 0

    #Category that is scraping
    key = 'top_music'
    category = categories_dict[key]
    
    #The main scrap
    url = f'https://www.amazon.com.{country}/gp/bestsellers/{category}/ref=zg_bs_nav_0'
    soup, status = extract_soup(url,n_header, preview=False)

    if status == 503:
        while status == 503:
            time.sleep(1)
            soup, status = extract_soup(url, preview=False)
            log_status[n_log] = status
            log_date[n_log] = datetime.now()

    if status ==200:
        boxes = top_amazon_boxes(soup)
        amz_key_top_boxes, amz_rows = scrap_boxes(boxes, country, dict_to_rows=True)

        for key in amz_key_top_boxes:
            print(key, end=' | ')

        print('\n')

        for row in amz_rows:
            for idx in range(len(row)):        
                print(row[idx], end=' | ')
            print('\n')