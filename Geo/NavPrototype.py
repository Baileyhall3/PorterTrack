import folium
from folium import plugins
import geopandas as gpd
import geoplot

import ipywidgets
import os
import json

import IPython
from IPython import display
import datetime

data = gpd.read_file('GeoResources/EAU.geojson')

print(type(data))

UMMlocation = (54.973523, -1.625129)
map_UMM = folium.Map(location = UMMlocation, width = "75%", zoom_start = 17)

select_widget = ipywidgets.Select(
    options=['Option A', 'Option B'],
    value='Option A',
    #description='Select',
    disabled=False)

def selectOption(opt):
    if opt == 'Option A':
        print('A')
    if opt == 'Option B':
        print('B')

ipywidgets.interact(selectOption, opt=select_widget)


class navigator:
    def __init__(self):
        self.geoResources = {}
        self.hospital_location = (54.973523, -1.625129)
        self.position = 'w'
        self.destination = 'EAU'

        for root, dirs, files in os.walk('portertrack/Geo/GeoResources'):
            for file in files:
                self.geoResources[file.split('.')[0]] = root + '/' + file

    def changeDestination(self, newDestination):
        self.destination = newDestination
        self.redrawMap()

    def drawBuilding(self, hospitalMap):
        locationOutline = self.geoResources[self.destination]
        folium.GeoJson(locationOutline, name="geojson").add_to(hospitalMap)

    def redrawMap(self):
        hospitalMap = folium.Map(location=self.hospital_location, width = "75%", zoom_start=17)
        self.drawBuilding(hospitalMap)
        #display(hospitalMap)

    #myNavigator = navigator()

    def displayWay(self, whereTo):
        self.changeDestination(whereTo)
        #self.changeDestination(whereTo)

    selectLocation_widget = ipywidgets.Select(
        options=[
            'CAS',
            'CT',
            'EAU',
            'ECG',
            'Kitchen',
            'MXR',
            'Pathology',
            'TC',
            'Theatres',
            'Ultrasound',
            'Ward1',
            'Ward2',
            'Ward3',
            'Ward4'
        ],
        value='EAU',
        description='Target',
        disabled=False
    )

    def selectLocation(self, way):
        if way == 'CAS':
            self.displayWay('CAS')
        if way == 'CT':
            self.displayWay('CT')
        if way == 'EAU':
            self.displayWay('EAU')
        if way == 'ECG':
            self.displayWay('ECG')
        if way == 'Kitchen':
            self.displayWay('Kitchen')
        if way == 'MXR':
            self.displayWay('MXR')
        if way == 'Pathology':
            self.displayWay('Pathology')
        if way == 'TC':
            self.displayWay('TC')
        if way == 'Theatres':
            self.displayWay('Theatres')
        if way == 'Ultrasound':
            self.displayWay('Ultrasound')
        if way == 'Ward1':
            self.displayWay('Ward1')
        if way == 'Ward2':
            self.displayWay('Ward2')
        if way == 'Ward3':
            self.displayWay('Ward3')
        if way == 'Ward4':
            self.displayWay('Ward4')

    #ipywidgets.interact(selectLocation(way=selectLocation_widget))
    #ipywidgets.interact(selectLocation(), )
