import collections
from .apply_func import apply_prc_mapping, apply_general_mapping, apply_general_mapping_lower

def main(inputdict):
    returndict = {}

    avb_mapping_dict = collections.OrderedDict()
    avb_mapping_dict['''^none$'''] = 'EMPTY'
    avb_mapping_dict['''^out_of_stock$'''] = 'Out_Of_Stock'
    avb_mapping_dict['''^out of stock$'''] = 'Out_Of_Stock'
    avb_mapping_dict['''^in_stock$'''] = 'In_Stock'
    avb_mapping_dict['''^retired$'''] = 'Discontinued'
    avb_mapping_dict['''^-'''] = 'RANGE_PRICE'
    avb_mapping_dict['''no longer available$'''] = 'Discontinued'

    prc_mapping_dict = collections.OrderedDict()
    prc_mapping_dict['^none$'] = 'nan'
    prc_mapping_dict['-'] = 'nan'
    prc_mapping_dict['^\d+.\d+$'] = None
    prc_mapping_dict['^\d+$'] = None


    model_mapping_dict=collections.OrderedDict()
    model_mapping_dict['^None$'] = 'EMPTY'
    model_mapping_dict['.*$'] = None

    upc_mapping_dict = collections.OrderedDict()
    upc_mapping_dict['^none$'] = 'EMPTY'
    upc_mapping_dict['^\d+$'] = None

    channel_mapping_dict = collections.OrderedDict()
    channel_mapping_dict['^none$'] = 'EMPTY'
    channel_mapping_dict['walmart.com'] = 'Walmart'
    channel_mapping_dict['.*'] = 'Market_Place'


    returndict['availability'] = apply_general_mapping_lower([inputdict['availability']], avb_mapping_dict)[0]
    returndict['price'] = apply_prc_mapping([inputdict['price']], prc_mapping_dict)[0]
    returndict['model'] = apply_general_mapping([inputdict['model']],model_mapping_dict)[0]
    returndict['UPC'] = apply_general_mapping([inputdict['UPC']], upc_mapping_dict)[0]
    returndict['channel'] = apply_general_mapping_lower([inputdict['channel']], channel_mapping_dict)[0]

    return returndict

if __name__ == '__main__':
    main()
