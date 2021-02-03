from os import listdir

def tokensList():
    path = 'static/a/tokens'
    data = []
    for f in listdir(path):
        data.append(
            path + '/'  + f
        )

    return {
        'succs': True,
        'data': data
        
    }

def mapsList():
    path = 'static/a/maps'
    data = []
    for f in listdir(path):
        data.append(
            path + '/'  + f
        )

    return {
        'succs': True,
        'data': data
    }
