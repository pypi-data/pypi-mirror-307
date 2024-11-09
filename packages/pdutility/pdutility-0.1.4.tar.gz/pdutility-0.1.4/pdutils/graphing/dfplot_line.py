import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import warnings
warnings.simplefilter("ignore")
from pdutils.utilities.check_input import check_input
from pdutils.utilities.set_axis_range import set_axis_range

def dfplot_line(x_data=None, y_data=None, **kwargs):
    '''
    Method to generate a line plot from the given data.

    Important considerations:
    - This method should be performed on pre-processed datasets. 
    
    Parameters
    ----------
    x_data          : list, np.ndarray, or pd.core.series.Series (default=None)
        X-axis data.
    y_data          : list, np.ndarray, or pd.core.series.Series (default=None)
        Y-axis data.
    kwargs          : custom keyword arguments.
        df          : pandas.core.frame.DataFrame (default=None), input data.
        x_col_name  : string (default=None), df column mapped to the x-axis.
        y_col_name  : string (default=None), df column mapped to the y-axis.
        class_data  : string, list, np.ndarray, or pd.Series (default=None), 
                      df column comprising a class (categorical) variable.
        x_axis_name : string (default=''), label assigned to the x-axis.
        y_axis_name : string (default=''), label assigned to the y-axis.
        x_rotation  : int (default=None), degree value to rotate xtick labels.
        y_rotation  : int (default=None), degree value to rotate ytick labels.
        tick_marks  : boolean (default=False), whether to show major divisions.
        ranges      : boolean (default=True), whether to allow this method to 
                      accept user-defined or auto-generated x and y limits.
        x_range     : tuple (default=None), min and max limits that will form 
                      the range of values for the x-axis.
        y_range     : tuple (default=None), min and max limits that will form 
                      the range of values for the y-axis.
        x_dtype     : string (default=None), x data type.
        y_dtype     : string (default=None), y data type.
                      (supported data types: 'int', 'float', and 'datetime')
        x_format    : string (default=None), format used to represent x data.
        y_format    : string (default=None), format used to represent y data.
        fig_style   : string (default='white'), graph background style. 
        fig_title   : string (default=''), graph title shown top-center.
        fig_size    : tuple (default=(8,6)), plot size in (w,h) format.
        legend_title: string (default=''), title shown inside the legend box.
        marker      : string (default='o'), symbol to represent a data point. 
        marker_size : int (default=35), value [10,200] to set marker size.
        font_size   : float (default=1.), value to set font scale for labels.
        line_alpha  : float (default=0.7), line opaqueness (lower is more transparent).
        line_style  : string (default='solid'), line type.
                      (supported line types: 'dashdot', 'dashed', 'dotted', 'solid') 
        line_width  : float (default=1.), line thickness.
        rug_plot    : boolean (default=False), whether to include the rug plot.

    Returns
    -------
    plot            : matplotlib.axes._subplots.AxesSubplot, showing a scatter
                      plot of x and y data.
    '''

    df           = kwargs.get('df', None) 
    x_col_name   = kwargs.get('x_col_name', None)
    y_col_name   = kwargs.get('y_col_name', None)
    class_data   = kwargs.get('class_data', None) 
    x_axis_name  = kwargs.get('x_axis_name', '')
    y_axis_name  = kwargs.get('y_axis_name', '')
    x_rotation   = kwargs.get('x_rotation', None)
    y_rotation   = kwargs.get('y_rotation', None)
    tick_marks   = kwargs.get('tick_marks', False) 
    
    ranges       = kwargs.get('ranges', True)
    x_range      = kwargs.get('x_range', None)
    y_range      = kwargs.get('y_range', None)
    x_dtype      = kwargs.get('x_dtype', None)
    y_dtype      = kwargs.get('y_dtype', None)
    x_format     = kwargs.get('x_format', None)
    y_format     = kwargs.get('y_format', None)
    
    fig_style    = kwargs.get('fig_style', 'white')
    fig_title    = kwargs.get('fig_title', '')
    fig_size     = kwargs.get('fig_size', (8,6)) 
    legend_title = kwargs.get('legend_title', '')
    marker       = kwargs.get('marker', 'o') 
    marker_size  = kwargs.get('marker_size', 7) 
    font_size    = kwargs.get('font_size', 1.)
    line_alpha   = kwargs.get('line_alpha', 0.7)
    line_style   = kwargs.get('line_style', 'solid')
    line_width   = kwargs.get('line_width', 1.)
    rug_plot     = kwargs.get('rug_plot', False)
             
    if fig_size:
        check_input(fig_size, inp_type=tuple, inp_elem_type=int)

    sns.set(font_scale=font_size)
    sns.set_style(fig_style)        
    if tick_marks is True:
        plt.rcParams['xtick.bottom'] = True
        plt.rcParams['ytick.left'] = True
    else:
        plt.rcParams['xtick.bottom'] = False
        plt.rcParams['ytick.left'] = False
    
    
    fig, ax = plt.subplots(figsize=fig_size)
    assert isinstance(marker_size, int) and marker_size>=7 and marker_size<=20,'Select a valid marker size [7,20].'

    if x_data is None or y_data is None:
        assert isinstance(df, pd.core.frame.DataFrame),'The input source must be specified as a Pandas dataframe if either x or y data are missing.'
        if x_col_name is None:
            assert isinstance(x_col_name, str),'Specify the dataframe column that is to be mapped to the x-axis.'
        if y_col_name is None:
            assert isinstance(y_col_name, str),'Specify the dataframe column that is to be mapped to the y-axis.'
        x_data = df[x_col_name].values
        y_data = df[y_col_name].values
    
    if df is None:
        assert x_data is not None and y_data is not None,'Both x_data and y_data must be provided in the absence of a data source.'
        assert type(x_data) in [list, np.ndarray, pd.core.series.Series],'The specified x_data must be a list, Numpy array, or Pandas Series.'
        assert type(y_data) in [list, np.ndarray, pd.core.series.Series],'The specified y_data must be a list, Numpy array, or Pandas Series.'
               
    if df is not None:
        if isinstance(class_data, str):
            if class_data in df.columns:
                class_data = df[class_data]
        else:
            if class_data is not None:
                assert type(class_data) in [list, np.ndarray, pd.core.series.Series],'The specified class_data must be a list, Numpy array, or Pandas Series.'
                assert len(class_data)==df.shape[0],'The specified class_data and the source dataframe column must have the same length.'
    else:
        if class_data is not None:
            assert len(class_data)==len(x_data),'The specified class_data and the x_ or y_data lengths must be equal.'
            
        
    palette = sns.color_palette('bright')
    plot    = sns.lineplot(x=x_data, y=y_data, ax=ax, palette=palette,
                           marker=marker, markersize=marker_size, 
                           linestyle=line_style, linewidth=line_width,
                           style=class_data, hue=class_data, alpha=line_alpha);

    if rug_plot is True:
        sns.rugplot(x=x_data, y=y_data, hue=class_data); 

    plot.set_title(fig_title)
    plt.xlabel(x_axis_name)
    plt.ylabel(y_axis_name)   
    plt.legend(title=legend_title)

    if ranges is True:
        set_axis_range(plot, data=x_data, axis='x', ax_range=x_range, data_type=x_dtype, data_format=x_format)
        set_axis_range(plot, data=y_data, axis='y', ax_range=y_range, data_type=y_dtype, data_format=y_format)    
        
    plt.setp(plot.get_xticklabels(),rotation=x_rotation)
    plt.setp(plot.get_yticklabels(),rotation=y_rotation)
    
    return plot
