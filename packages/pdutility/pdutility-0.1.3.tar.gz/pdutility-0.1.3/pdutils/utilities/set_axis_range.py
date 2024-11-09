
import numpy as np
import pandas as pd
from datetime import datetime
from pdutils.utilities.parse_range import parse_range

def set_axis_range(plot, data, axis='x', ax_range=None, **kwargs):
    '''
    Method to:
    > set limits to values along the x and the y axes 
    > format tick labels along the axes

    Important considerations:
    - This method should be performed on complete input data.
    - Expand datetime data type and data format in a future update. 
    
    Parameters
    ----------
    plot            : matplotlib.axes._subplots.AxesSubplot
        Matplotlib graph that represents the original plot.
    data            : list, np.ndarray, or pd.core.series.Series
        Axis data to apply limits to and format.
    axis            : string (default='x')
        Graph axis that is the target of this method.
    ax_range        : tuple (default=None)
        Min and max limits that will form the range for the axis.
    kwargs          : custom keyword arguments.
        data_type   : string (default=None), input data type.
        data_format : string (default=None), input data format.

    Returns
    -------
    plot            : matplotlib.axes._subplots.AxesSubplot, with axes  
                      ticks representing designated ranges and formats.
    '''
    
    data_type   = kwargs.get('data_type', None)
    data_format = kwargs.get('data_format', None)

    assert type(data) in [list, np.ndarray, pd.core.series.Series], 'The required data type  must be a list, numpy array, or pandas series.'
    assert axis in ['x', 'y'],"The axis arg must be either 'x' or 'y'."

    data = list(data)
    if isinstance(data[0], datetime) or isinstance(data[0], pd.Timestamp):
        print('*** First item in the input data has type datetime. Make sure that the rest of the input data is of the same type.')
        data = [pd.to_datetime(n) for n in data]

    if data_type is not None:
        assert data_type in ['int', 'float', 'datetime'],'Specify a valid data type.'

    if ax_range is not None:
        ax_range = parse_range(list(ax_range), range_name=f'{axis}-axis range')
        if isinstance(ax_range[0], pd.Timestamp) and isinstance(data[0], str):
            ax_range = [datetime.strftime(x, format=data_format) for x in ax_range] 
        print(f'*** Note that the terminal value in the given range {ax_range} for the {axis}-axis will be included in the plot.')
        plot.set(xlim=ax_range) if axis=='x' else plot.set(ylim=ax_range)
    else:
        if data_type == 'datetime' and isinstance(data[0], str):
            assert data_format is not None,"If data_type='datetime', it must be accompanied by the corresponding formar in 'data_format'."
            dticks = [pd.to_datetime(n, format='%Y-%m-%d') for n in sorted(data)]
        else:
            dticks = [n for n in sorted(data)]

        ticks = list(np.unique(dticks))
        step  = ticks[1]-ticks[0]
        ticks.append(ticks[-1]+step)

        if data_type == 'datetime' and isinstance(data[0], str):
            ticks = [datetime.strftime(x, format=data_format) for x in ticks]
  
        plot.set(xlim=[ticks[0], ticks[-1]]) if axis=='x' else \
            plot.set(ylim=[ticks[0], ticks[-1]] )

        if data_type != 'datetime':
            if data_format:
                ticklabels = [data_format.format(x) for x in ticks]
                plot.set_xticklabels(ticklabels) if axis=='x' else \
                    plot.set_yticklabels(ticklabels)
                
    return plot