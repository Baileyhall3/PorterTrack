import folium
from folium import plugins
import geopandas as gpd

import ipywidgets
import os
import json

import IPython
from IPython.display import display
import datetime

data = gpd.read_file('GeoResources/EAU.geojson')

print(type(data))

UMMlocation = (54.973523, -1.625129)
map_UMM = folium.Map(location = UMMlocation, width = "75%", zoom_start = 17)
hauseOutline = 'GeoResources/EAU.geojson'
folium.GeoJson(hauseOutline, name="EAU").add_to(map_UMM)
display(map_UMM)

