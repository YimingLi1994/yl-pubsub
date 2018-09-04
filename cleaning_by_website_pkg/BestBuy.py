import collections
import sys

from .apply_func import apply_prc_mapping, apply_general_mapping, apply_general_mapping_lower


def main(inputdict):
    returndict = {}

    avb_mapping_dict = collections.OrderedDict()
    avb_mapping_dict['''^none$'''] = 'EMPTY'
    avb_mapping_dict['''no longer available\.$'''] = 'Out_Of_Stock'
    avb_mapping_dict['''^loading$'''] = 'loading'
    avb_mapping_dict['''^sold out$'''] = 'Out_Of_Stock'
    avb_mapping_dict['''^add to cart$'''] = 'In_Stock'
    avb_mapping_dict['''^in-store purchase only'''] = 'Store_Only'
    avb_mapping_dict['''^in store only'''] = 'Store_Only'
    avb_mapping_dict['''^store pickup only'''] = 'Store_Only'
    avb_mapping_dict['''exclusively available at'''] = 'Store_Only'
    avb_mapping_dict['''check stores'''] = 'Store_Only'
    avb_mapping_dict['''^free shipping by'''] = 'In_Stock'
    avb_mapping_dict['''shipping: get it by'''] = 'In_Stock'
    avb_mapping_dict['''^free delivery'''] = 'In_Stock'
    avb_mapping_dict['''^\$\d+.\d+ shipping by'''] = 'In_Stock'
    avb_mapping_dict['''^\$\d+.\d+ delivery as soon as'''] = 'In_Stock'
    avb_mapping_dict['''^coming soon'''] = 'Out_Of_Stock'
    avb_mapping_dict['''^getting more soon'''] = 'Out_Of_Stock'
    avb_mapping_dict['''^delivery: unavailable for \d+'''] = 'Out_Of_Stock'
    avb_mapping_dict['''^shipping: unavailable for \d+'''] = 'Out_Of_Stock'
    avb_mapping_dict['''pickup on release day'''] = 'Out_Of_Stock'
    avb_mapping_dict['''pre-order now'''] = 'Out_Of_Stock'

    prc_mapping_dict = collections.OrderedDict()
    prc_mapping_dict['^none$'] = 'nan'
    prc_mapping_dict['^\d+.\d+$'] = None
    prc_mapping_dict['^\d+$'] = None

    model_mapping_dict = collections.OrderedDict()
    model_mapping_dict['^None$'] = 'EMPTY'
    model_mapping_dict['^Model ?[:|#] ?(.*)$'] = None

    upc_mapping_dict = collections.OrderedDict()
    upc_mapping_dict['^none$'] = 'EMPTY'
    upc_mapping_dict['^\d+$'] = None

    returndict['WEBSITE'] = 'BestBuy'
    returndict['availability'] = apply_general_mapping_lower([inputdict['availability']], avb_mapping_dict)[0]
    returndict['price'] = apply_prc_mapping([inputdict['price']], prc_mapping_dict)[0]
    returndict['model'] = apply_general_mapping([inputdict['model']], model_mapping_dict)[0]
    returndict['UPC'] = apply_general_mapping([inputdict['UPC']], upc_mapping_dict)[0]
    return returndict

if __name__ == '__main__':
    tagname = sys.argv[1]
    main(tagname)
