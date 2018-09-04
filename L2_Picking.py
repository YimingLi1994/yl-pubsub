import json


def general_cleaning(WEBSITE, PID, LAST_CRAWL, TAG, payload, schemalst):
    retdict={}
    for eachcol in schemalst:
        if eachcol in payload:
            retdict[eachcol] = str(payload[eachcol]) if payload[eachcol] is not None else None
        else:
            retdict[eachcol] = None
    retdict['WEBSITE']=WEBSITE
    retdict['PID']=PID
    retdict['LAST_CRAWL']=LAST_CRAWL
    retdict['tag'] =TAG
    return retdict


def cleaning(row):
    final_table_schema = [
        'WEBSITE', 'PID',
        'product_title', 'shipping', 'model', 'SKU', 'UPC', 'price', 'price_type', 'style', 'style2',
        'availability', 'brand', 'rating', 'reviews', 'channel', 'meta', 'page_path',
        'LAST_CRAWL', 'tag', ]
    payload_temp = json.loads(row['PAYLOAD'])
    if type(payload_temp) == dict:
        payload_dict = payload_temp
        retdict = general_cleaning(row['WEBSITE'], row['PID'], row['LAST_CRAWL'], row['TAG'],
                                   payload_dict, final_table_schema)
    elif type(payload_temp) == list:
        retdict = []
        for each_payload in payload_temp:
            retdict.append(general_cleaning(row['WEBSITE'], row['PID'], row['LAST_CRAWL'], row['TAG'],
                                each_payload, final_table_schema))
    return retdict


def errcleaning(row):
    FAIL_table_schema = ['WEBSITE', 'PID', 'URL', 'STATUS', 'LAST_CRAWL', 'tag']
    retdict={}
    retdict['WEBSITE'] = row['WEBSITE']
    retdict['PID'] = row['PID']
    retdict['URL'] = None
    retdict['STATUS'] = row['STATUS']
    retdict['LAST_CRAWL'] = row['LAST_CRAWL']
    retdict['tag'] = row['TAG']
    return retdict
