import PySimpleGUI as sg  
import json
import geocoder
import sys
import webbrowser
from time import sleep
from urllib.request import urlopen



def open_appointments(cities=None):
    locations = json.loads(urlopen('https://heb-ecom-covid-vaccine.hebdigital-prd.com/vaccine_locations.json').read())['locations']
    success = False
    for location in locations:
        if cities is not None and location['city'].lower() not in cities:
            continue
        if location['openTimeslots'] > 0:
            contents = urlopen(location['url']).read().decode('utf-8')
            if 'Appointments are no longer available for this location' not in contents:
                webbrowser.open(location['url'])
                print('\n'.join(f'{k}={v}' for k, v in location.items() if k not in ['url', 'slotDetails'] and v is not None))
                success = True
    return success



if __name__ == '__main__':
    sg.theme('DarkGrey10')
    layout = [[sg.Text('Please Enter City Name to find open vaccination appointments.')],      
                    [sg.InputText()],      
                    [sg.Submit(), sg.Cancel()]
                    ]     

    window = sg.Window('HEB Vaccine Finder', layout)    

    event, values = window.read() 

    cities = values[0]
    window.close()
    while not open_appointments(cities):
        layout = [[sg.Text('Searching for Vaccine Appointments in '+cities)]]
        window = sg.Window('HEB Vaccine Finder', layout)
        event, values = window.read()
        sleep(1)
        

   