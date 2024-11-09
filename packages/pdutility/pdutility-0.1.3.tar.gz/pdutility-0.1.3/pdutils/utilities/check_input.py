import numpy as np

def check_input(inp, inp_type=list, inp_elem_type=np.ndarray):
    '''
    Method to check if user input and elements of user input conform to the
    corresponding data types.

    Important considerations:
    - This method was originally designed to focus on list types and the 
      data types within a list.

    Parameters
    ----------
    inp             : multiple
        User-defined input.
    inp_type        : multiple (default=list)
        Data type of user-defined input.
    inp_elem_type   : built-in data type (default=np.ndarray)
        Python data type that characterizes the elements of the input.

    Returns
    -------
                    : string, input validation message or assertion error.
    '''

    assert isinstance(inp, inp_type),f"Input '{inp}' must belong to {inp_type}."

    if not inp_type in [dict, float, int, str]: 
        if len(inp) > 0:
            
            types = [type(v).__name__ for v in inp]
            assert len(set(types))==1,'All input elements must belong to the same class.' 
            for e in inp:
                if isinstance(inp_elem_type, list) or isinstance(inp_elem_type, tuple):
                    err = 0
                    for i in inp_elem_type:
                        try:
                            assert isinstance(e, i),f"Input element '{e}' in '{inp}' must belong to {i}."
                        except Exception:
                            err += 1
                            if err >= len(inp_elem_type):  
                                raise AttributeError(f'Input elements must belong to one of the types in {inp_elem_type}.')
                else:
                    assert isinstance(e, inp_elem_type),f"Input element '{e}' in '{inp}' must belong to {inp_elem_type}."
                        
    if inp_type in [dict]:
        types = [type(v).__name__ for k,v in inp.items()]
        assert len(set(types))==1,'All dictionary values must belong to the same class.' 
        for k,v in inp.items():
            if isinstance(inp_elem_type, list) or isinstance(inp_elem_type, tuple):
                err = 0
                for i in inp_elem_type:
                    try:
                        assert isinstance(v, i),f"The value of '{v}' associated with '{k}' must belong to {i}."
                    except Exception:
                        err += 1
                        if err >= len(inp_elem_type):
                            raise AttributeError(f'Values must belong to one of the types in {inp_elem_type}.')
            else:
                assert isinstance(v, inp_elem_type),f"The value of '{v}' associated with '{k}' must belong to {inp_elem_type}."

    return 'Input checks out!'