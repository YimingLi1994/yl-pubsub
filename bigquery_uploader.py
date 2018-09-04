from google.cloud import bigquery

def table_exists(tblname, bigquery_client, ds_ref):
    if tblname in [x.table_id for x in bigquery_client.list_dataset_tables(ds_ref)]:
        return True
    else:
        return False


def stream_data(bigquery_client, dataset_id, table_id, rows, schemalst:list):
    # bigquery_client = bigquery.Client('yl3573-214601')
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    # Get the table from the API so that the schema is available.
    try:
        table = bigquery_client.get_table(table_ref)
    except:
        tableschema=()
        for eachpair in schemalst:
            tableschema+=(bigquery.SchemaField(eachpair[0], eachpair[1]),)
        tablet = bigquery.Table(table_ref, schema=tableschema)
        try:
            table = bigquery_client.create_table(tablet)
        except:
            table = bigquery_client.get_table(table_ref)
    errors = bigquery_client.create_rows(table, rows, )
    if not errors:
        print('Loaded {} row(s) into {}:{}'.format(len(rows), dataset_id, table_id))
    else:
        print('Errors:')


