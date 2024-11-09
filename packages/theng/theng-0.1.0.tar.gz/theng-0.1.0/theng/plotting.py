"""Module to provide a number of pre-formatted plotting functions for use in Thunderhead Results"""

from enum import Enum
from typing import Iterable, List, Tuple, Union
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objects import Figure

class PlotType(Enum):
    """Defines the valid types of plot file types"""
    HTML = 0
    PNG = 1
    JPG = 2
    JPEG = 3
    
def save_plot(fig: Figure, filename: str, plot_type: PlotType) -> None:
    """Saves the given figure as the provided PlotType and loads that file in to Thunderhead Results
    
    Args:
        fig (Figure): The Plotly Figure to save
        filename (str): The filename to save the Figure as
        type (FileType): The FileType to save the figure as
    """
    if plot_type == PlotType.HTML:
        path: str = filename + ".html"
        fig.write_html(path, include_mathjax='cdn')
        return_html_plot(fig.layout.title.text, path)
        
    elif plot_type == PlotType.PNG:
        path: str = filename + ".png"
        fig.write_image(path)
        return_image_plot(fig.layout.title.text, path)
        
    elif plot_type == PlotType.JPG:
        path: str = filename + ".jpg"
        fig.write_image(path)
        return_image_plot(fig.layout.title.text, path)
        
    elif plot_type == PlotType.JPEG:
        path: str = filename + ".jpeg"
        fig.write_image(path)
        return_image_plot(fig.layout.title.text, path)

def return_html_plot(name: str, filename: str) -> None:
    """Return an HTML plot object to Thunderhead Results for loading in the UI

    Args:
        name (str): The name of the plot to return and display
        filename (str): The path to the saved plot file
    """
    print(f'PLOTTITLE: {name}')
    print(f'HTMLPLOT: {filename}')
        
def return_image_plot(name: str, filename: str) -> None:
    """Return an image plot object to Thunderhead Results for loading in the UI

    Args:
        name (str): The name of the plot to return and display
        filename (str): The path to the saved plot file
    """
    print(f'PLOTTITLE: {name}')
    print(f'IMGPLOT: {filename}')

def line_plot(x_data: Union[List, Tuple[List]],
              y_data: Union[List, Tuple[List]], 
              x_title: str = None, 
              y_title: str = None, 
              plot_title: str = None, 
              width: int = 800, 
              height: int = 600, 
              legend_names: List[str] = None) -> Figure:
    """Utility plotting function for making line plots

    Args:
        x_data (Union[List, Tuple[List]]): 
            The data to plot on the X axis. Must be the same length and type as y_data.
            
            If a List, only one series will be plotted in the figure.
            If a tuple of lists, one series will be plotted for each pair of x_data and y_data.
        y_data (Union[List, Tuple[List]]): 
            The data to plot on the Y axis. Must be the same length and type as x_data.
            
            If a List, only one series will be plotted in the figure.
            If a tuple of lists, one series will be plotted for each pair of x_data and y_data.
        x_title (str, optional): Sets the X axis title. Defaults to None.
        y_title (str, optional): Sets the y axis title. Defaults to None.
        plot_title (str, optional): Sets the plot title. Defaults to None.
        width (int, optional): The width of the figure. Defaults to 800.
        height (int, optional): The height of the figure. Defaults to 600.
        legend_names (List[str], optional): Optional list of names to use when plotting multiple series of data. Defaults to a generator of "Series xxx" format.

    Raises:
        TypeError: If x_data and y_data are different types, not of type Tuple or List, or if they are a Tuple, but any of the elements in the tuple are not lists.
            Also raised if the legend_names List contains a Non-string.
        ValueError: If x_data, y_data, or legend_names (optional) are different lengths. 

    Returns:
        Figure: The final constructed figure
    """
    if type(x_data) != type(y_data):
        raise TypeError("X Data and Y Data are of incompatible type signatures for plotting.")
    elif type(x_data) not in (tuple, list):
        raise TypeError(f"Data provided is not an acceptable type. Expected Tuple or List, but got \"{type(x_data)}\"")
    elif len(x_data) != len(y_data):
        raise ValueError("X Data and Y Data are of different lengths.")
    
    if legend_names != None:
        if len(legend_names) != len(x_data):
            raise ValueError("Legend name generator does not supply a sufficient number of names")
    
    #Plot a single series of data
    if type(x_data) == list:
        data = {
            "x": x_data,
            "y": y_data
        }
        x_title = "X Data" if x_title == None else x_title
        y_title = "Y Data" if y_title == None else y_title
        plot_title = "Line Plot" if plot_title == None else plot_title
        
        fig: Figure = px.line(data, x="x", y="y")
        
    #Plot multiple series of data on the same figure
    elif type(x_data) == tuple:
        fig: Figure = Figure()
        if legend_names == None: 
            legend_names = [f'Series {i}' for i in range(0, len(x_data))]
        
        if legend_names != None:
            for x, y, name in zip(x_data, y_data, legend_names):
                if type(x) != list:
                    raise TypeError(f"Member of X Data tuple is not a valid type. Expected List, got \"{type(x)}\"")
                elif type(y) != list:
                    raise TypeError(f"Member of Y Data tuple is not a valid type. Expected List, got \"{type(y)}\"")
                elif type(name) != str:
                    raise TypeError(f"Name provided by legend_name is not a string: \"{name}\"")
                
                fig.add_trace(go.Scatter(
                    x=x,
                    y=y,
                    mode='lines',
                    name=name,
                    showlegend=True
                ))
    
    #Make it pretty by default
    fig.update_layout(
        title_text=plot_title,
        title_x=0.5,
        font_family="Courier New",
        font_color="#222222",
        paper_bgcolor="#cccccc",
        width=width,
        height=height,
        showlegend=True
    )
    fig.update_xaxes(title=x_title)
    fig.update_yaxes(title=y_title)
    return fig