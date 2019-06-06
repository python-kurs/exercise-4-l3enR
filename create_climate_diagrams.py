import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from pathlib import Path

# Import both data tables into python using pandas. Set the index column to "MESS_DATUM" and parse the column values as dates. [1P]
garmisch  = pd.read_csv("./data/produkt_klima_tag_20171010_20190412_01550.txt", parse_dates = ["MESS_DATUM"],
                      index_col = "MESS_DATUM", sep = ";", na_values = "")
zugspitze = pd.read_csv("./data/produkt_klima_tag_20171010_20190412_05792.txt", parse_dates = ["MESS_DATUM"],
                      index_col = "MESS_DATUM", sep = ";", na_values = "")

# Clip the tables to the year 2018: [1P]
garmisch  = garmisch.loc["2018"]
zugspitze = zugspitze.loc["2018"]

# Resample the temperature data to monthly averages (" TMK") and the precipitation data to monthly sums (" RSK"): [1P]
garmisch_agg  = garmisch.loc[:, [" TMK", " RSK"]].resample("M").agg({" TMK": "mean", " RSK": "sum"})
zugspitze_agg = zugspitze.loc[:, [" TMK", " RSK"]].resample("M").agg({" TMK": "mean", " RSK": "sum"})

###########################################################
##1 PLOT TEMPERATURE---------------------------------------
temperatur = garmisch_agg[" TMK"]

plt.plot(temperatur, color = "r")
plt.xlabel("Time")
plt.ylabel("Temperature (°C)")

##2 PLOT PRECIPITATION-------------------------------------
#using a bar chart

position = garmisch_agg.index
niederschlag = garmisch_agg[" RSK"]

plt.bar(position, niederschlag, width = 20, color = "b") 
plt.xlabel("Time")
plt.ylabel("Precipitation (mm)")

##3 COMBINE THE PLOTS
fig = plt.figure(figsize = (8,5))

position = garmisch_agg.index

ax2 = fig.add_subplot(111)
ax1 = ax2.twinx()

ax1.plot(temperatur, color = "r")
ax2.bar(x = position, height = niederschlag, width = 25, color = "b")

##4 MONTH AS NAMES--------------------------------------
fig = plt.figure(figsize = (8,5))
position = garmisch_agg.index

ax2 = fig.add_subplot(111)
ax1 = ax2.twinx()

ax1.plot(temperatur, color = "r")
ax2.bar(x = position, height = niederschlag, width = 25, color = "b")

days = mdates.DayLocator(bymonthday = 28)
monthName = mdates.DateFormatter("%b")

#ax.xticks()
ax.xaxis.set_major_locator(days)
ax.xaxis.set_major_formatter(monthName)
##5-------------------------------------

temperatur = garmisch_agg[" TMK"]
niederschlag = garmisch_agg[" RSK"]


fig = plt.figure(figsize=(20,5))

ax2 = fig.add_subplot(111)
ax1 = ax2.twinx()

ax1.plot(temperatur, c="r", label="Temperature")
ax2.plot(niederschlag)
plt.hist(niederschlag)
#ax2.plot(tabelle_resampled.loc[:, "air_pressure"], c="b", label="Air pressure")

ax1.set_ylabel("Temperature (°C)")
ax2.set_ylabel("Precipitation (mm)")


ax1.set_xlim(("2018-01-01","2018-12-31"))

#ax1.xaxis.set_major_locator(days)
#ax1.xaxis.set_major_formatter(monthFmt)
plt.show()
###########################################################

# Define a plotting function that draws a simple climate diagram
# Add the arguments as mentioned in the docstring below [1P]
# Set the default temperature range from -15°C to 20°C and the precipitation range from 0mm to 370mm [1P]

def create_climate_diagram(df, temp_col, prec_col, title, filename, temp_min, temp_max, prec_min, prec_max):
    """
    Draw a climate diagram.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with values to plot from
    temp_col : str
        Name of temperature column
    prec_col : str
        Name of precipitation column
    title : String
        The title for the figure
    filename : String
        The name of the output figure
    temp_min : Number
        The minimum temperature value to display
    temp_max : Number
        The maximum temperature value to display
    prec_min : Number
        The minimum precipitation value to display
    prec_max : Number
        The maximum precipitation value to display

    Returns
    -------
    The figure
    
    """

    temperature = df[temp_col]
    precipitation = df[prec_col]
    position = df.index
    
    fig = plt.figure(figsize=(10,8))
    plt.rcParams["font.size"] = 16

    ax2 = fig.add_subplot(111)
    ax1 = ax2.twinx()

    # Draw temperature values as a red line and precipitation values as blue bars: [1P]
    # Hint: Check out the matplotlib documentation how to plot barcharts. Try to directly set the correct
    #       x-axis labels (month shortnames).
    ax1.plot(temperature, color = "r")
    ax2.bar(x = position, height = precipitation, width = 25, color = "b")
    # Set appropiate limits to each y-axis using the function arguments: [1P]
    ax2.set_ylim(prec_min,prec_max)
    ax1.set_ylim(temp_min,temp_max)
    
    # Set appropiate labels to each y-axis: [1P]
    ax2.set_ylabel("Precipitation in mm")
    ax1.set_ylabel("Temperature in °C")

    # Give your diagram the title from the passed arguments: [1P]
    plt.title(title)

    # Save the figure as png image in the "output" folder with the given filename. [1P]
        # create output path if it not already exists
    output_dir = Path("Output")
    if not output_dir.exists():
        output_dir.mkdir()
        
    plt.savefig(output_dir / filename)
    
    
    return fig

# Use this function to draw a climate diagram for 2018 for both stations and save the result: [1P]
create_climate_diagram(df = garmisch_agg, temp_col = " TMK", prec_col = " RSK",
                       title = "Climate Diagram\nGarmisch-Partenkirchen",
                       filename = "Garmisch-Partenkirchen_climateDiagram.png", temp_min = -15., temp_max = 20., prec_min = 0., prec_max = 370.)
create_climate_diagram(df = zugspitze_agg, temp_col = " TMK", prec_col = " RSK",
                       title = "Climate Diagram\nZugspitze",
                       filename = "Zugspitze_climateDiagram.png", temp_min = -15., temp_max = 20., prec_min = 0., prec_max = 370.)