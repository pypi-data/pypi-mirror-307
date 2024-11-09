
import pandas as pd
from pdutils.utilities.check_input import check_input

def parse_range(ls_range, range_name=None, counter=0, allow_nan=False):
    '''
    Method specifically created to parse range in check_range().

    Parameters
    ----------
    ls_range        : list
        The input range.
    range_name      : str (default=None)
        The user-designated name for the given range.
    counter         : int (default=0)
        Integer flag used to indicate the occurrence of an exception.
    allow_nan       : boolean (default=False)
        Whether to allow np.nan as a limit in the given range.

    Returns
    -------
    ls_range        : list, representing the parsed range.
    '''

    check_input(ls_range, inp_elem_type=(float, int, pd.Timestamp, str) )
    if range_name:
        assert isinstance(range_name, str),'A string type is required for list name.'
    else:
        range_name = 'range'

    assert len(ls_range) == 2,f"The {range_name} must comprise a valid [min, max] pair."

    if allow_nan is False:
        assert str(ls_range[0])!='nan' and str(ls_range[1])!='nan','This range object prohibits the use of np.nan or other missing value variants.'

    if type(ls_range[0]) in [str]:
        try:
            print(f"*** Warning! Found string type in {range_name}. Attempting to convert to numeric...")
            if int(ls_range[0]) and int(ls_range[1]):
                ls_range = [int(ls_range[0]), int(ls_range[1]) ]
                print('*** Done!')
        except Exception:
            counter += 1

        if counter >= 1:
            print('*** Numeric conversion failed.')
            print("*** Attempting to convert the range elements to datetime...")
            ls_range[0] = pd.to_datetime(ls_range[0])
            ls_range[1] = pd.to_datetime(ls_range[1])

    if type(ls_range[0]) in [int, float, pd.Timestamp]:
        if allow_nan is False:
            assert ls_range[0]<ls_range[1],"The min of range must be less than the max of range."
        else:
            if str(ls_range[0])!='nan' and str(ls_range[1])!='nan':
                assert ls_range[0]<=ls_range[1],"The min of range must be less than or equal to the max of range."

    print(f'{range_name:<12}: [{ls_range[0]}, {ls_range[1]}]' )

    return ls_range