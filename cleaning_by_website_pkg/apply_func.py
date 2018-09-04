import re


def prc_mapping(inputstr, mappingdict):
    cleanstr = re.sub(' +', ' ', inputstr.lower().strip())
    retvalue = -1
    for key, value in mappingdict.items():
        try:
            if len(re.findall(key, cleanstr)) > 0:
                if value is not None:
                    if value == 'nan':
                        retvalue = None
                        break
                    else:
                        retvalue = value
                        break
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


def general_mapping(inputstr, mappingdict):
    cleanstr = re.sub(' +', ' ', inputstr.strip())
    for key, value in mappingdict.items():
        if len(re.findall(key, cleanstr)) > 0:
            if value is not None:
                if value == 'EMPTY':
                    return None
                return value
            return re.findall(key, cleanstr)[0].strip()
    return 'Miss: '+inputstr

def apply_general_mapping(strlst, mappingdict):
    return [general_mapping(str(x), mappingdict) for x in strlst]


