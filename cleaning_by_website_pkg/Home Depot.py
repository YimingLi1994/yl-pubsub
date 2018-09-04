import collections
import sys

from .apply_func import apply_prc_mapping, apply_general_mapping, apply_general_mapping_lower


def main(inputdict):
    returndict = {}

    avb_mapping_dict = collections.OrderedDict()
    avb_mapping_dict['''^none$'''] = 'EMPTY'  # ('-2', 'TO_BE_CHECK')
    avb_mapping_dict['''^discontinued'''] = 'Discontinued'
    avb_mapping_dict['''^unavailable'''] = 'Out_Of_Stock'
    avb_mapping_dict['''^[a-z ]*~?out of stock online'''] = 'Out_Of_Stock'
    avb_mapping_dict['''^backordered'''] = 'Out_Of_Stock'
    avb_mapping_dict['''^out of stock'''] = 'Out_Of_Stock'
    avb_mapping_dict['''earliest delivery date: '''] = 'In_Stock'
    avb_mapping_dict['''^[a-z ]*~?free shipping'''] = 'In_Stock'
    avb_mapping_dict['''^[a-z ]*~?standard shipping'''] = 'In_Stock'
    avb_mapping_dict['''^http[s]?://schema\.org/instock'''] = 'In_Stock'
    # avb_mapping_dict['''^http[s]?://schema\.org/instock'''] = 'In_Stock'
    avb_mapping_dict['''^express delivery'''] = 'In_Stock'

    prc_mapping_dict = collections.OrderedDict()
    prc_mapping_dict['^none$'] = 'nan'
    prc_mapping_dict['^\d+.\d+$'] = None
    prc_mapping_dict['^\d+$'] = None

    model_mapping_dict = collections.OrderedDict()
    model_mapping_dict['^None'] = 'EMPTY'
    model_mapping_dict['^Model ?[:|#] ?(.*)$'] = None

    upc_mapping_dict = collections.OrderedDict()
    upc_mapping_dict['^none$'] = 'EMPTY'
    upc_mapping_dict['^\d+$'] = None

    returndict['WEBSITE'] = 'Home Depot'
    returndict['availability'] = apply_general_mapping_lower([inputdict['availability']], avb_mapping_dict)[0]
    returndict['price'] = apply_prc_mapping([inputdict['price']], prc_mapping_dict)[0]
    returndict['model'] = apply_general_mapping([inputdict['model']], model_mapping_dict)[0]
    returndict['UPC'] = apply_general_mapping([inputdict['UPC']], upc_mapping_dict)[0]
    return returndict

if __name__ == '__main__':
    tagname = sys.argv[1]
    main(tagname)
