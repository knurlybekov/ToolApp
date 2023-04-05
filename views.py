import json
from datetime import datetime

from __init__ import db
from flask import Blueprint, render_template, request, flash, jsonify, session, send_file
import folium
import pandas as pd
from flask_login import login_required, current_user
from dbConn import connection, getWorks, getAreas
from models import employees
from apscheduler.schedulers.background import BackgroundScheduler

# scheduler = BackgroundScheduler()

views = Blueprint('views', __name__)


# 386ce9d230e54b3bb0f64db8b0da1238


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    map_obj = map_create()
    map_html = map_obj._repr_html_()
    return render_template("home.html", map_html=map_html, user=current_user, current_time=current_time)


def map_create():
    lat = 50.676109
    lon = -120.340836
    zoom = 11

    dfAreas = getAreas()

    map = folium.Map(location=[lat, lon],
                     zoom_start=zoom, control_scale=True)

    markers = get_markers()
    for marker in markers:
        marker.add_to(map)

    # for i, row in df.iterrows():
    #     popup_text = f'Employee: {row["Employee First Name"]} {row["Employee Last Name"]}<br>'
    #     popup_text += f'Tool: {row["Tool Name"]}<br>'
    #     popup_text += f'Start Time: {row["Start time"]}<br>'
    #     popup_text += f'End Time: {row["End time"]}'
    #     popup = folium.Popup(popup_text, max_width=300)
    #     folium.Marker(location=[row['Latitude'], row['Longitude']], popup=popup,
    #                   icon=folium.Icon(color='#' + row['Color'], icon_color='#' + row['Color'])).add_to(map)

    for i, row in dfAreas.iterrows():
        Latitude = row["Latitude"].split(',')
        Longitude = row["Longitude"].split(',')
        coordinates = []
        for lat, lon in zip(Latitude, Longitude):
            coordinates.append([float(lat), float(lon)])
        folium.PolyLine(coordinates, color='#' + row['Color'], weight=2.5, opacity=1).add_to(map)
        folium.Polygon(coordinates, color='#' + row['Color'], fill=True, fill_color='#' + row['Color'],
                       fill_opacity=0.2).add_to(map)

    map.get_root().width = "100%"
    map.get_root().height = "800px"

    return map


def get_markers():
    df = getWorks()
    markers = []
    for i, row in df.iterrows():
        popup_text = f'Employee: {row["Employee First Name"]} {row["Employee Last Name"]}<br>'
        popup_text += f'Tool: {row["Tool Name"]}<br>'
        popup_text += f'Start Time: {row["Start time"]}<br>'
        popup_text += f'End Time: {row["End time"]}'
        popup = folium.Popup(popup_text, max_width=300)
        marker = folium.Marker(location=[row['Latitude'], row['Longitude']], popup=popup,
                               icon=folium.Icon(color='#' + row['Color'], icon_color='#' + row['Color']))
        markers.append(marker)
    return markers



# scheduler.add_job(get_markers, 'interval', seconds=10)
#
# # start the scheduler
# scheduler.start()
