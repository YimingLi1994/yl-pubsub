import collections

from .apply_func import apply_prc_mapping, apply_general_mapping, apply_general_mapping_lower


def main(inputdict):
    returndict = {}

    avb_mapping_dict = collections.OrderedDict()
    avb_mapping_dict['''^none$'''] = 'EMPTY'
    avb_mapping_dict['''^available[!]?$'''] = 'In_Stock'
    avb_mapping_dict['''^not available$'''] = 'Out_Of_Stock'
    avb_mapping_dict['''^currently unavailable$'''] = 'Out_Of_Stock'
    avb_mapping_dict['''^ready for delivery by'''] = 'In_Stock'
    avb_mapping_dict['''^delivery available as soon as'''] = 'In_Stock'
    avb_mapping_dict['''^ready for delivery on'''] = 'In_Stock'
    avb_mapping_dict['''no longer available on lowes'''] = 'Discontinued'

    prc_mapping_dict = collections.OrderedDict()
    prc_mapping_dict['^none$'] = 'nan'
    prc_mapping_dict['^\d+.\d+$'] = None
    prc_mapping_dict['^\d+$'] = None

    model_mapping_dict = collections.OrderedDict()
    model_mapping_dict['^None$'] = 'EMPTY'
    model_mapping_dict['Model ?[:|#] ?(.*)$'] = None

    upc_mapping_dict = collections.OrderedDict()
    upc_mapping_dict['^none$'] = 'EMPTY'
    upc_mapping_dict['/(\d+).jpg$'] = None

    returndict['availability'] = apply_general_mapping_lower([inputdict['availability']], avb_mapping_dict)[0]
    returndict['price'] = apply_prc_mapping([inputdict['price']], prc_mapping_dict)[0]
    returndict['model'] = apply_general_mapping([inputdict['model']], model_mapping_dict)[0]
    returndict['UPC'] = apply_general_mapping([inputdict['UPC']], upc_mapping_dict)[0]
    return returndict

if __name__ == '__main__':
    main()
