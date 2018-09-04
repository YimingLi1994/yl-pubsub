import collections

from .apply_func import apply_prc_mapping, apply_general_mapping, apply_general_mapping_lower


def main(inputdict):
    returndict = {}
    # df.groupby(['WEBSITE']).count()
    avb_mapping_dict = collections.OrderedDict()
    avb_mapping_dict['''^none$'''] = ('EMPTY')
    avb_mapping_dict['''^sorry!? we couldn\'t find that page'''] = ('expired')
    avb_mapping_dict['''^available from these sellers'''] = ('Out_Of_Stock')
    avb_mapping_dict['''^temporarily out of stock'''] = ('Out_Of_Stock')
    avb_mapping_dict['''^currently unavailable'''] = ('Out_Of_Stock')
    avb_mapping_dict['''^this item has not yet been released'''] = ('Out_Of_Stock, not release')
    avb_mapping_dict['''^this item will be release'''] = ('Out_Of_Stock, not release')
    avb_mapping_dict['''^available now'''] = ('In_Stock')
    avb_mapping_dict['''^in stock on'''] = ('In_Stock, shipping day varies')
    avb_mapping_dict['''^in stock[\.]?'''] = ('In_Stock')
    avb_mapping_dict['''^only [0-9]+ left'''] = ('In_Stock, low stock')
    avb_mapping_dict['''^usually ships within'''] = ('In_Stock, shipping day varies')
    avb_mapping_dict['''^may take an extra'''] = ('In_Stock, shipping day varies')
    avb_mapping_dict['''^want it'''] = ('In_Stock, shipping day varies')
    avb_mapping_dict['''^get it as soon as'''] = ('In_Stock, shipping day varies')
    avb_mapping_dict['''^available to buy on zappos'''] = ('In_Stock, available on Zappos')

    amazon_prc_mapping = collections.OrderedDict()
    amazon_prc_mapping['''\-'''] = -2
    amazon_prc_mapping['^none$'] = 'nan'
    amazon_prc_mapping['''^\$([\d.,]+)'''] = None

    amazon_prc_type_mapping = collections.OrderedDict()
    amazon_prc_type_mapping['''^none$'''] = ('EMPTY')
    amazon_prc_type_mapping['''^add-on item'''] = ('add on')

    amazon_model_mapping = collections.OrderedDict()
    amazon_model_mapping['''^None$'''] = 'EMPTY'
    amazon_model_mapping['''^Item model number[\W]$'''] = 'EMPTY'
    amazon_model_mapping['''^Item model number[\W]?(.*)$'''] = None
    amazon_model_mapping['''^Model\s*[\W]$'''] = 'EMPTY'
    amazon_model_mapping['''^Model\s*(.*)$'''] = None

    amazon_ch_mapping = collections.OrderedDict()
    amazon_ch_mapping['''^none$'''] = ('EMPTY')
    amazon_ch_mapping['''amazon\.com'''] = ('amazon')
    amazon_ch_mapping['''fulfilled by amazon'''] = ('fulfilled by amazon')
    amazon_ch_mapping['''sold by'''] = ('marketplace')
    amazon_ch_mapping['''^gift-wrap'''] = ('amazon')

    returndict['availability'] = apply_general_mapping_lower([inputdict['availability']], avb_mapping_dict)[0]
    returndict['price'] = apply_prc_mapping([inputdict['price']], amazon_prc_mapping)[0]
    returndict['model'] = apply_general_mapping([inputdict['model']], amazon_model_mapping)[0]
    returndict['price_type'] = apply_general_mapping_lower([inputdict['price_type']], amazon_prc_type_mapping)[0]
    returndict['channel'] = apply_general_mapping_lower([inputdict['channel']], amazon_ch_mapping)[0]

    return returndict


if __name__ == '__main__':
    test = {
        'availability': 'In Stock.',
        'price': None,
        'model': None,
        'price_type': None,
        'channel': 'Ships from and sold by Amazon.com.'
    }
    print(main(test))
