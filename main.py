"""
run FG with --httpd=8080
https://pypi.org/project/discordsdk/
http://localhost:8080/json/

http://localhost:8080/json/position/gear-agl-m


https://wiki.flightgear.org/Aircraft_properties_reference
"""

import time, datetime
import requests
import discordsdk as dsdk

properties = {
    'altitude': 'position/gear-agl-m',
    'altitude-ft': 'position/altitude-agl-ft',
    'aircraft-desc': 'sim/description',
    'airspeed-kt': 'velocities/airspeed-kt',
    'airport': 'sim/tower/airport-id'
    }

APPLICATION_ID = 834452760530518027

app = dsdk.Discord(APPLICATION_ID, dsdk.CreateFlags.default)


def callback(result):
    if result == dsdk.Result.ok:
        pass
        #print("Successfully set the activity!")
    else:
        raise Exception(result)

def get_prop(prop):
    r = requests.get('http://127.0.0.1:8080/json/' + prop)
    return r.json()['value']


def get_all_props():
    altitude = get_prop(properties['altitude-ft'])
    altitude = int(altitude*10)/10
    if altitude < -0.1:

        altitude = 'CRASHED'
    else:
        altitude = str(altitude)
        if len(altitude) > 5:
            altitude = altitude[:-5] + ' ' + altitude[-5:]
        altitude += 'ft'
    
    acd = get_prop(properties['aircraft-desc'])
    ac_desc = ' '.join(list(acd[:16].split(' ')[:-1]))

    airport = get_prop(properties['airport'])
    return ac_desc, altitude, airport

def set_status():
    activity_manager = app.get_activity_manager()
    activity = dsdk.Activity()
    ac_desc, altitude, airport = get_all_props()
    activity.details = f'Flying near {airport} airport'
    activity.state = f"{ac_desc} {altitude}"
    activity.assets.large_image = 'logo'
    activity_manager.update_activity(activity, callback)


while True:
    set_status()
    app.run_callbacks()
    time.sleep(2)