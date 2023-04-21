import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from PIL import Image
import os
st.set_page_config(layout="wide")


df = pd.read_csv('cleaned.csv')


st.title(":red[Find the Nearest Pub 🍻🍻]")
image = Image.open('nearest.jpg')
st.image(image, use_column_width=True)




user_lat = st.text_input("Enter your Latitude:")
user_lon = st.text_input("Enter your Longitude:")

if st.button("Find nearest pubs"):
    if user_lat and user_lon:
        user_location = (float(user_lat), float(user_lon))
        df['distance'] = df.apply(lambda row: ((row['latitude'] - user_location[0])**2 + (row['longitude'] - user_location[1])**2)**0.5, axis=1)
        nearest_df = df.nsmallest(5, 'distance')

        # create a map centered at the user's location
        pub_map = folium.Map(location=user_location, zoom_start=12)

        # add markers for the nearest pubs
        mc = MarkerCluster()
        for row in nearest_df.iterrows():
            mc.add_child(folium.Marker(location=[row[1]['latitude'], row[1]['longitude']], popup=row[1]['name']))
        pub_map.add_child(mc)

        # display the map
        folium_static(pub_map)
