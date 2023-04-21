import folium
from folium import plugins
import pandas as pd

import ipywidgets
import os
import json

from IPython.display import display
import IPython
#from IPython import display
import datetime

#!git clone https://github.com/Baileyhall3/PorterTrack.git

hospitalLocation = (54.973523, -1.625129)
hospitalMap = folium.Map(location = hospitalLocation, width = "75%", zoom_start = 17)

for files in os.listdir('GeoResources'):
  print(files)
  #folium.GeoJson(files).add_to(map_UMM)

CAS = 'GeoResources/CAS.geojson'
folium.GeoJson(CAS, name="CAS").add_to(hospitalMap)

MXR = 'GeoResources/MXR.geojson'
folium.GeoJson(MXR, name="MXR").add_to(hospitalMap)


hospitalMap
