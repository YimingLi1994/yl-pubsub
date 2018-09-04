import collections
from .apply_func import apply_prc_mapping, apply_general_mapping, apply_general_mapping_lower

def main(inputdict):
    returndict = {}

    avb_mapping_dict = collections.OrderedDict()
    avb_mapping_dict['^none$'] = 'EMPTY'
    avb_mapping_dict['^not available$'] = 'Out_Of_Stock'
    avb_mapping_dict['out of stock$'] = 'Out_Of_Stock'
    avb_mapping_dict['not available$'] = 'Out_Of_Stock'
    avb_mapping_dict['unavailable$'] = 'Out_Of_Stock'
    avb_mapping_dict['no longer available$'] = 'Out_Of_Stock'
    avb_mapping_dict['^preorder'] = 'PREORDER'
    avb_mapping_dict['^in stock'] = 'In_Stock'
    avb_mapping_dict['^get it tomorrow$'] = 'In_Stock'
    avb_mapping_dict['^get it free in'] = 'In_Stock'
    avb_mapping_dict['^get it by'] = 'In_Stock'
    avb_mapping_dict['^get it from'] = 'In_Stock'

    prc_mapping_dict = collections.OrderedDict()
    prc_mapping_dict['^none$'] = 'nan'
    prc_mapping_dict['-'] = 'nan'
    prc_mapping_dict['^\$([\d.,]+)$'] = None
    prc_mapping_dict['^see store for price$'] = -10
    prc_mapping_dict['^see low price in cart$'] = -100


    model_mapping_dict=collections.OrderedDict()
    model_mapping_dict['^None$'] = 'EMPTY'

    upc_mapping_dict = collections.OrderedDict()
    upc_mapping_dict['^none$'] = 'EMPTY'
    upc_mapping_dict['^UPC: *(\d+)$'] = None

    price_type_mapping_dict = collections.OrderedDict()
    price_type_mapping_dict['^none$'] = 'EMPTY'
    price_type_mapping_dict['^sale'] = 'SALE'
    price_type_mapping_dict['^clearance$'] = 'CLEARANCE'

    returndict['availability'] = apply_general_mapping_lower([inputdict['availability']], avb_mapping_dict)[0]
    returndict['price'] = apply_prc_mapping([inputdict['price']], prc_mapping_dict)[0]
    returndict['model'] = apply_general_mapping([inputdict['model']],model_mapping_dict)[0]
    returndict['UPC'] = apply_general_mapping([inputdict['UPC']], upc_mapping_dict)[0]
    returndict['price_type'] = apply_general_mapping_lower([inputdict['price_type']], price_type_mapping_dict)[0]
    return returndict

if __name__ == '__main__':
    main()
