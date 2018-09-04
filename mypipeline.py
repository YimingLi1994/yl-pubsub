import datetime as dt
import time
import pytz
from google.cloud import bigquery
from timeit import default_timer as timer
import L2_Picking
import L3_Cleaning
import bigquery_uploader
import time
import google
import json

def mypipeline(MessageQueue, L1queue, L2queue_SUCC, L2queue_FAIL, L3queue):
    while True:
        L1 = MessageQueue.get()
        L1queue.put(L1)
        # todaydate = (dt.datetime.now(pytz.timezone('America/Chicago'))).replace(tzinfo=None).strftime('%Y%m%d')
        # bigquery_uploader.stream_data(bigquery_client, 'yl_crawler', 'recv_raw_{}'.format(todaydate), L1)
        try:
            L1_SUCC = L1 if L1['STATUS'] == 'SUCCESS' else None
            L2_SUCC = None
            L1_FAIL = L1 if L1['STATUS'] != 'SUCCESS' else None
            L2_FAIL = None
            if L1_SUCC is not None:
                L2_SUCC = L2_Picking.cleaning(L1_SUCC)
                if type(L2_SUCC) == dict:
                    L2queue_SUCC.put(L2_SUCC)
                elif type(L2_SUCC) == list:
                    for each_L2_SUCC in L2_SUCC:
                        L2queue_SUCC.put(each_L2_SUCC)
                # bigquery_uploader.stream_data(bigquery_client, 'yl_crawler', 'succ_crawl_{}'.format(todaydate), L2_SUCC)
            elif L1_FAIL is not None:
                L2_FAIL = L2_Picking.errcleaning(L1_SUCC)
                L2queue_FAIL.put(L2_FAIL)
                # bigquery_uploader.stream_data(bigquery_client, 'yl_crawler', 'err_crawl_{}'.format(todaydate), L2_FAIL)

            if L2_SUCC is not None:
                if type(L2_SUCC) == dict:
                    if L3_Cleaning.L3_filter(L2_SUCC) is True:
                        L3 = L3_Cleaning.L3_Cleaning(L2_SUCC)
                        L3queue.put(L3)
                    # bigquery_uploader.stream_data(bigquery_client, 'yl_crawler', 'all_comp_all_{}'.format(todaydate), L3)
                elif type(L2_SUCC) == list:
                    for each_L2_SUCC in L2_SUCC:
                        if L3_Cleaning.L3_filter(each_L2_SUCC) is True:
                            L3 = L3_Cleaning.L3_Cleaning(each_L2_SUCC)
                            L3queue.put(L3)
        except TypeError as e:
            print(e)



def L1_uploader(L1queue):
    schemalst=[('WEBSITE','STRING'), ('URL','STRING'), ('PID','STRING'), ('SKU','STRING'),
               ('TAG','STRING'), ('STATUS','STRING'), ('PAYLOAD','STRING'), ('LAST_CRAWL','STRING')]
    bigquery_client = bigquery.Client('yl3573-214601')

    uploderlst = []
    starttime = timer()
    while True:
        todaydate = (dt.datetime.now(pytz.timezone('America/Chicago'))).replace(tzinfo=None).strftime('%Y%m%d')
        eachitem = L1queue.get()
        uploderlst.append(eachitem)
        endtime = timer()
        timepass = endtime - starttime
        if (len(uploderlst) > 100 or timepass > 1) and len(uploderlst) > 1:
            try:
                # print('upload...{}'.format(len(uploderlst)))
                bigquery_uploader.stream_data(bigquery_client, 'yl_crawler', 'recv_raw_{}'.format(todaydate), uploderlst, schemalst=schemalst)
                starttime = timer()
                uploderlst = []
            except google.api_core.exceptions.NotFound as e:
                print(e)



def L2queue_SUCC(L2queue_SUCC):
    schemalst = [('WEBSITE', 'STRING'), ('PID', 'STRING'),('product_title', 'STRING'),('shipping', 'STRING'),
                 ('model', 'STRING'),('SKU', 'STRING'),('UPC', 'STRING'),('price', 'STRING'),('price_type', 'STRING'),
                 ('style', 'STRING'),('style2', 'STRING'),('availability', 'STRING'),('brand', 'STRING'),('rating', 'STRING'),
                 ('reviews', 'STRING'),('channel', 'STRING'),('meta', 'STRING'),('page_path', 'STRING'),('LAST_CRAWL', 'STRING'),('tag', 'STRING'),
                 ]
    bigquery_client = bigquery.Client('yl3573-214601')

    uploderlst = []
    starttime = timer()
    while True:
        todaydate = (dt.datetime.now(pytz.timezone('America/Chicago'))).replace(tzinfo=None).strftime('%Y%m%d')
        eachitem = L2queue_SUCC.get()
        uploderlst.append(eachitem)
        endtime = timer()
        timepass = endtime - starttime
        if (len(uploderlst) > 100 or timepass > 1) and len(uploderlst) > 1:
            try:
                # print('upload...{}'.format(len(uploderlst)))
                bigquery_uploader.stream_data(bigquery_client, 'yl_crawler', 'succ_crawl_{}'.format(todaydate), uploderlst, schemalst)
                starttime = timer()
                uploderlst = []
            except google.api_core.exceptions.NotFound as e:
                print(e)



def L2queue_FAIL(L2queue_FAIL):
    schemalst = [('WEBSITE', 'STRING'), ('PID', 'STRING'), ('URL', 'STRING'), ('STATUS', 'STRING'),
                 ('LAST_CRAWL', 'STRING'), ('tag', 'STRING'),
                 ]
    bigquery_client = bigquery.Client('yl3573-214601')

    uploderlst = []
    starttime = timer()
    while True:
        todaydate = (dt.datetime.now(pytz.timezone('America/Chicago'))).replace(tzinfo=None).strftime('%Y%m%d')
        eachitem = L2queue_FAIL.get()
        uploderlst.append(eachitem)
        endtime = timer()
        timepass = endtime - starttime
        if (len(uploderlst) > 100 or timepass > 1) and len(uploderlst) > 1:
            try:
                # print('upload...{}'.format(len(uploderlst)))
                bigquery_uploader.stream_data(bigquery_client, 'yl_crawler', 'err_crawl_{}'.format(todaydate), uploderlst, schemalst)
                starttime = timer()
                uploderlst = []
            except google.api_core.exceptions.NotFound as e:
                print(e)



def L3queue(L3queue):
    schemalst = [('WEBSITE', 'STRING'), ('PID', 'STRING'), ('shipping', 'STRING'), ('brand', 'STRING'),
                 ('model', 'STRING'), ('UPC', 'STRING'),('price', 'FLOAT'), ('price_type', 'STRING'),
                 ('availability', 'STRING'), ('channel', 'STRING'),('LAST_CRAWL', 'STRING'),
                 ]
    bigquery_client = bigquery.Client('yl3573-214601')
    uploderlst = []
    starttime = timer()
    while True:
        todaydate = (dt.datetime.now(pytz.timezone('America/Chicago'))).replace(tzinfo=None).strftime('%Y%m%d')
        eachitem = L3queue.get()
        uploderlst.append(eachitem)
        endtime = timer()
        timepass = endtime - starttime
        if (len(uploderlst) > 100 or timepass > 1) and len(uploderlst)>1:
            try:
                # print('upload...{}'.format(len(uploderlst)))
                bigquery_uploader.stream_data(bigquery_client, 'yl_crawler', 'all_comp_all_{}'.format(todaydate), uploderlst, schemalst)
                starttime = timer()
                uploderlst = []
            except google.api_core.exceptions.NotFound as e:
                print(e)



