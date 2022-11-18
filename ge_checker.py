import json
import requests
import pandas as pd
from datetime import datetime, timedelta

# constants
service_name = 'Global%20Entry'
url_all_locations = f'https://ttp.cbp.dhs.gov/schedulerapi/locations/?temporary=false&inviteOnly=false&operational=true&serviceName={service_name}'
url_avail_locations = f'https://ttp.cbp.dhs.gov/schedulerapi/slots/asLocations?minimum=1&filterTimestampBy=before&timestamp=$datebefore&serviceName={service_name}'
all_locations_file = 'locations/all_locations.pickle'

"""Retrieve the list of all Enrollment Center. save it as pickle/json file"""
def get_all_locations(use_json = False):
    global all_locations_file
    if use_json:
        try:
            all_locations_file = all_locations_file.split('.')[0] + '.json'
            with open(all_locations_file, 'r') as file:
                locations_df = pd.DataFrame.from_records(json.load(file))
        except FileNotFoundError:
            locations_json = requests.get(url_all_locations).json()
            locations_df = pd.DataFrame.from_records(locations_json)
            with open(all_locations_file, 'w') as wfile:
                json.dump(locations_json, wfile)
    else:
        try:
            with open(all_locations_file, 'rb') as file:
                locations_df = pd.read_pickle(file)
        except FileNotFoundError:
            locations_df = pd.DataFrame.from_records(requests.get(url_all_locations).json())
            with open(all_locations_file, 'wb') as wfile:
                locations_df.to_pickle(wfile)
    return locations_df

"""Retrieve Enrollment Centers that have slots before a certain date."""
def get_avail_locations(datebefore):
    return pd.DataFrame.from_records(requests.get(url_avail_locations.replace('$datebefore', datebefore)).json()).filter(["state", "city", "name", "id"]).sort_values(['state', 'city'], ascending=True).reset_index(drop=True)

"""Retrieve available slots for a single Enrollment Center as DataFrame"""
def get_slot_datetime(id):
    slots_json = requests.get(f'https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&locationId={id}&minimum=1').json()
    return pd.DataFrame.from_records(slots_json)

"""main logic to check if our interested time & places have available slots. If no slot found, gives available locations"""
def check_availability(preferences: dict):
    all_locations = get_all_locations(use_json=True)
    datetimebefore = datetime.strptime(preferences['datebefore'], '%Y-%m-%d') + timedelta(days = 1)
    # all_locations = get_all_locations()
    avail_locations = get_avail_locations(preferences['datebefore'])
    match_id = [id for id in avail_locations[avail_locations['id'].isin(preferences['locations'])]['id']]
    if (len(match_id) == 0):
        return (False, avail_locations)
    avail_time_slots = pd.concat(map(get_slot_datetime, iter(match_id)))[['locationId', 'startTimestamp']].astype({'startTimestamp':'datetime64[ns]'})
    slots_time_location = avail_time_slots[avail_time_slots['startTimestamp'] < datetimebefore].join(all_locations.set_index('id')[['state', 'city', 'name', 'address']], 'locationId').sort_values('startTimestamp')[1:]
    return (True, slots_time_location)

if __name__ == '__main__':
    # load preferences
    try:
        with open("preferences.json", 'r') as file:
            preferences = json.load(file)
    except FileNotFoundError:
        preferences = {"datebefore" : "2022-12-28", "locations" : [7740]}

    # run
    succeed, result = check_availability(preferences)
    print('Slot(s) found for the given date and location:' if succeed else 'No slot found for the given date and location. The available locations are:')
    print(result)