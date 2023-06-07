# # UK cats crossing in 2017 in Cornwall
#
# Created in cahoots with Aidan O'Donnell <ODonnellA4@cardiff.ac.uk>. 

# +
import pandas as pd
import numpy as np
# #!pip install "ydata_profiling"
from ydata_profiling import ProfileReport 

import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error

import folium

from pyproj import Geod
wgs84_geod = Geod(ellps='WGS84')

from IPython.display import display, HTML
# -

HTML(
    """<script>
code_show=true; 
function code_toggle() {
 if (code_show){
 $('div.input').hide();
 } else {
 $('div.input').show();
 }
 code_show = !code_show
} 
$( document ).ready(code_toggle);
</script>
The raw code for this IPython notebook is by default hidden for easier reading.
To toggle on/off the raw code, click <a href="javascript:code_toggle()">here</a>."""
)


# +
# Function to get distance between pairs of lat-long points in metres

def Distance(id1, id2, pairs):
    az12, az21, dist = wgs84_geod.inv(pairs[pairs.event_id == id1].location_long,
                                  pairs[pairs.event_id == id1].location_lat,
                                  pairs[pairs.event_id == id2].location_long,
                                  pairs[pairs.event_id == id2].location_lat)
    return dist[0].round()


# -

# function that takes two rows, returns a list of distance + time diffs if cats are not the same cat
def distance_time_between(row1, row2, rv_df):
    id1 = row1['animal_id'] 
    id2 = row2['animal_id']
    event_id1 = row1['event_id']
    event_id2 = row2['event_id']
        
    time_diff = row1['epoch'] - row2['epoch']
          
    # This could be the same cat at different times, ignore if so
    if id1 != id2:
        rv_df.loc[len(rv_df)] = [id1, event_id1,
                                 id2, event_id2, 
                                 Distance(event_id1, event_id2, df), 
                                 time_diff,
                                 row1['timestamp']]
    
    return rv_df


# How close are cats that have the same timestamps?
def find_rendezvous(df, epoch_col):
    rendezvous = pd.DataFrame(columns=['id1', 'event_id1', 'id2', 'event_id2', 'distance_m', 'time_diff_secs', 'time'])
    
    # what time stamps occur more than once?
    times = df[epoch_col].value_counts()
    counts = np.unique(times.values)
    
    for count in counts:   
        shared_times = times[times == count]

        # For each time, there are a list of events
        for epoch in shared_times.index:
            # look at the list of events occurring at this epoch time
            events = df[df[epoch_col] == epoch]
            # For each event, look at the events below it in the list and get distance/time diffs
            for index1 in range(0, len(events)):
                for index2 in range(index1, len(events)):
                    if index1 != index2:               
                        distance_time_between(events.iloc[index1], events.iloc[index2], rendezvous)
        
    rendezvous = rendezvous.convert_dtypes()
    return rendezvous


# Read in the cat data that has been previously quality controlled.

df = pd.read_csv("cats_uk_qcd.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Take the simple case of cats that have exact timestamps close to each other

find_rendezvous(df, 'epoch').sort_values(['distance_m']).head()

# Now expand the timestamp search to compare those that are within the same 10 second time slot

# Round timestamps to nearest 10 seconds, then look at distance between
df['epoch_10sec_rounded'] = df['epoch'] // 10 * 10

find_rendezvous(df, 'epoch_10sec_rounded').sort_values(['distance_m']).head()

# Expand the timestamp search again, this time comparing those that are within the same 100 second time slot

# Round timestamps to nearest 100 seconds, then look at distance between
df['epoch_100sec_rounded'] = df['epoch'] // 100 * 100

result = find_rendezvous(df, 'epoch_100sec_rounded').sort_values(['distance_m', 'time_diff_secs'])
result.head()


# We have an exact match on distance, only 15 seconds apart!

# Highligh on a map this meeting
def map_meeting(meeting, df):
    print("When", meeting.id1, "met", meeting.id2, "at", meeting.time, 
          "within", abs(meeting.time_diff_secs), "seconds of each other and",
          meeting.distance_m, "metres")

    cat1 = df[df.animal_id == meeting.id1]
    cat2 = df[df.animal_id == meeting.id2]

    cat1_meeting = df[df.event_id == meeting.event_id1].iloc[0]
    cat2_meeting = df[df.event_id == meeting.event_id2].iloc[0]

    # filter each of the cat datasets down to the meeting day
    cat1_2d = cat1[(cat1['timestamp'].dt.strftime('%Y-%m-%d') == meeting.time.strftime('%Y-%m-%d'))]
    cat2_2d = cat2[(cat2['timestamp'].dt.strftime('%Y-%m-%d') == meeting.time.strftime('%Y-%m-%d'))]

    # extract rusty lat, longs to a list
    list_cat1_locs = list(zip(cat1_2d.location_lat, cat1_2d.location_long))

    # extract indie lat, longs to a list
    list_cat2_locs = list(zip(cat2_2d.location_lat, cat2_2d.location_long))

    # create folium map base
    mapit = folium.Map(location=[cat1_meeting['location_lat'], cat1_meeting['location_long']],
                       zoom_start=18)

    # choose tiles from Carto db
    folium.TileLayer('cartodbpositron').add_to(mapit)

    # plot all rusty locations for those 2 days on low opacity
    for coord in list_cat1_locs:
        folium.CircleMarker(location=[coord[0],coord[1]], 
                            color='red', 
                            opacity = 0.2,
                            fill_opacity = 0.2,
                            fill_color = 'red',
                            radius=2).add_to(mapit)
    
    # plot all indie locations for those 2 days on low opacity
    for coord in list_cat2_locs:
        folium.CircleMarker(location=[coord[0],coord[1]], 
                            color='green', 
                            opacity = 0.2,
                            fill_opacity = 0.2,
                            fill_color = 'green',
                            radius=2).add_to(mapit)
    
    # rusty crossing point on full opacity
    folium.CircleMarker(location=[cat1_meeting['location_lat'], cat1_meeting['location_long']],
                        color='red', 
                        opacity = 1.0,
                        fill_opacity = 1.0,
                        fill_color = 'red',
                        radius=4).add_to(mapit)

    # indie crossing point on full opacity
    folium.CircleMarker(location=[cat2_meeting['location_lat'], cat2_meeting['location_long']], 
                        color='green', 
                        opacity = 1.0,
                        fill_opacity = 1.0,
                        fill_color = 'green',
                        radius=4).add_to(mapit)
    return mapit


meeting = result.iloc[0]
map_meeting(meeting, df)

# And the second close recorded meeting, within 1 metre and 7 seconds

meeting = result.iloc[1]
map_meeting(meeting, df)


