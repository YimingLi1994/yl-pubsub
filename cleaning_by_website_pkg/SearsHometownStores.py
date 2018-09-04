import collections
import re


def main(inputdict):
    returndict = {}

    avb_mapping_dict = collections.OrderedDict()
    avb_mapping_dict['''^none$'''] = 'Out_Of_Stock'
    avb_mapping_dict['''^instock$'''] = 'In_Stock'

    prc_mapping_dict = collections.OrderedDict()
    prc_mapping_dict['^none$'] = 'nan'
    prc_mapping_dict['^\d+.\d+$'] = None

    model_mapping_dict = collections.OrderedDict()
    model_mapping_dict['^none$'] = 'EMPTY'
    model_mapping_dict['^(.*)$'] = None

    returndict['availability'] = apply_general_mapping_lower([inputdict['availability']], avb_mapping_dict)[0]
    returndict['price'] = apply_prc_mapping([inputdict['price']], prc_mapping_dict)[0]
    returndict['model'] = apply_model_mapping([inputdict['model']], model_mapping_dict)[0]

    return returndict

def prc_mapping(inputstr, mappingdict):
    cleanstr = re.sub(' +', ' ', inputstr.lower().strip())
    retvalue = -1
    for key, value in mappingdict.items():
        try:
            if len(re.findall(key, cleanstr)) > 0:
                if value is not None:
                    if callable(value):
                        retvalue = value(cleanstr)
                    else:
#                         if type(value) == str:
                        if value == 'nan':
                            retvalue = None
                            break
                        else:
                            retvalue = value

                else:
                    retvalue = float(re.findall(key, cleanstr)[0].replace(',','').strip())
                    break
        except:
            pass
    return retvalue


def apply_prc_mapping(strlst, mappingdict):
    return [prc_mapping(str(x), mappingdict) for x in strlst]


def general_mapping_lower(inputstr, mappingdict):
    cleanstr = re.sub(' +', ' ', inputstr.lower().strip())
    for key, value in mappingdict.items():
        if len(re.findall(key, cleanstr)) > 0:
            if value is not None:
                if value == 'EMPTY':
                    return None
                return value
            return re.findall(key, cleanstr)[0].strip()
    return 'Miss: '+inputstr


def apply_general_mapping_lower(strlst, mappingdict):
    return [general_mapping_lower(str(x), mappingdict) for x in strlst]


def general_mapping(inputstr, mappingdict, flags=re.IGNORECASE):
    inputstr = inputstr.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    cleanstr = re.sub(' +', ' ', inputstr.strip())
    for key, value in mappingdict.items():
        if len(re.findall(key, cleanstr, flags=re.IGNORECASE)) > 0:
            if value is not None:
                if value == 'EMPTY':
                    return None
                return value
            return re.findall(key, cleanstr, flags=re.IGNORECASE)[0].strip()
    return 'Miss: '+inputstr

def apply_general_mapping(strlst, mappingdict):
    return [general_mapping(str(x), mappingdict) for x in strlst]

def model_mapping(inputstr, mappingdict, flags=re.IGNORECASE):
    #inputstr = inputstr.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    cleanstr = re.sub(' +', ' ', inputstr.strip())
    for key, value in mappingdict.items():
        if len(re.findall(key, cleanstr, flags=re.IGNORECASE)) > 0:
            if value is not None:
                if value == 'EMPTY':
                    return 'EMPTY'
                if value == "MultipleChoices":
                    return "MultipleChoices"
                return value
            return re.findall(key, cleanstr, flags=re.IGNORECASE)[0].strip()
        elif len(re.findall(key, cleanstr, flags=re.IGNORECASE)) == 0 and value == 'No_Model':
            return 'No_Model'
    return 'Miss: '+inputstr

def apply_model_mapping(strlst, mappingdict):
    return [model_mapping(str(x), mappingdict) for x in strlst]