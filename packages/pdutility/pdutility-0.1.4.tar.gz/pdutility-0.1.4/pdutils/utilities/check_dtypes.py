import numpy as np

def check_dtypes(inp, dtype_ls, join='or'):
    '''
    Method to check if user input comprising one or more values conforms to  
    one or more data types.

    Parameters
    ----------
    inp             : multiple
        User-defined input.
    type_ls         : list 
        Data type(s) of user-defined input.
    join            : string (default='or')
        String (options: 'or', '|', 'and', '&') to characterize how the given 
        data types are concatenated.

    Returns
    -------
                    : boolean, input data type validation or invalidation.
    '''
    
    assert join in ['or', '|', 'and', '&'],"Argument paased to the 'join' parameter must be one of the four options: 'or', '|', 'and', '&'."
    inp = inp if isinstance(inp, list) else [inp]
    
    if len(inp) != len(dtype_ls):
        inp = inp*len(dtype_ls)
    res = list(map(isinstance, inp, dtype_ls ) )

    if join in ['or', '|']:
        if True in res:
            return True
        else:
            return False
    else:
        res = list(np.unique(res))
        if len(res) == 1 and res == True:
            return True
        else:
            return False