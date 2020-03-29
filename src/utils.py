
def dict2list(d):
    ''' Converts a dictionary to a sorted list
    '''
    ret = []
    for c in d.keys():
        if d[c]:
            ret.append(c)
    return sorted(ret)


def get_timestamp():
    ''' yyyymmdd
    '''
    from datetime import datetime
    now = datetime.now()
    timestamp =  int( datetime.timestamp(now) ) 
    timestamp = str( datetime.fromtimestamp(timestamp)) .replace(":", "").replace("-", "").replace(" ", "_") 
    return timestamp


def default_encoding_for_json(obj):
    import numpy as np
    if type(obj).__module__ == np.__name__:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj.item()
    raise TypeError('Unknown type:', type(obj))