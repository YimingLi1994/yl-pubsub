import collections
from .apply_func import apply_prc_mapping, apply_general_mapping, apply_general_mapping_lower


def main(inputdict):
    returndict = {}

    staples_prc_mapping = collections.OrderedDict()
    staples_prc_mapping['''^none$'''] = 'nan'
    staples_prc_mapping['''^([\d.,]+)$'''] = None
    staples_prc_mapping['''^\$([\d.,]+)$'''] = None

    staples_avb_mapping = collections.OrderedDict()
    staples_avb_mapping['''^none$'''] = ('EMPTY')
    staples_avb_mapping['''^in_stock'''] = ('In_Stock')
    staples_avb_mapping['''^out_of_stock'''] = ('Out_Of_Stock')

    staples_prc_type_mapping = collections.OrderedDict()
    staples_prc_type_mapping['''^none$'''] = ('EMPTY')
    staples_prc_type_mapping['''^in cart'''] = ('in cart')

    staples_model_mapping = collections.OrderedDict()
    staples_model_mapping['''^None$'''] = 'EMPTY'
    staples_model_mapping['''^[\W]?(.*)$'''] = None

    staples_UPC_mapping = collections.OrderedDict()
    staples_UPC_mapping['''^none$'''] = 'EMPTY'
    staples_UPC_mapping['''^[0]+$'''] = 'EMPTY'
    staples_UPC_mapping['''^(\d+)$'''] = None

    returndict['availability'] = apply_general_mapping_lower([inputdict['availability']], staples_avb_mapping)[0]
    returndict['price'] = apply_prc_mapping([inputdict['price']], staples_prc_mapping)[0]
    returndict['price_type'] = apply_general_mapping_lower([inputdict['price_type']], staples_prc_type_mapping)[0]
    returndict['model'] = apply_general_mapping([inputdict['model']], staples_model_mapping)[0]
    returndict['UPC'] = apply_general_mapping([inputdict['UPC']], staples_UPC_mapping)[0]
    return returndict

if __name__ == '__main__':
    main()
