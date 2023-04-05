import base64
import io
import json
from datetime import datetime

import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objs as go
from flask_paginate import get_page_args, Pagination

from __init__ import db
from flask import Blueprint, render_template, request, flash, send_file
import matplotlib.pyplot as plt
from flask_login import login_required, current_user
from dbConn import connection, getWorks, getAreas, work_processBar
from models import employees

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():

    selected_menu_item = request.args.get('menu')
    print(selected_menu_item)
    conn = connection()
    cursor = conn.cursor()
    cursor.execute('SELECT s_id, s_name FROM side')
    menu_items = [{'value': 0, 'label': 'All sides'}]
    for row in cursor:
        menu_items.append({'value': row[0], 'label': row[1]})

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    page = request.args.get('page', 1, type=int)
    table_html, pagination = get_table(page=page)
    df = work_processBar(selected_menu_item)
    num_rows = df.shape[0]

    x_values = list(range(num_rows))
    fig = px.bar(df, x=x_values, y='Time Consumed (Minutes)', color='Employee ID', barmode='group')
    fig.update_layout(xaxis_title='№ of works', title='Works on a side')
    fig.add_trace(
        go.Scatter(x=x_values, y=df['Required Time'], mode='markers',
                   marker=dict(size=0, color='#FF0000', symbol='square'), name='Required Time')
    )
    fig.update_traces(
        customdata=df[['Employee ID', 'Name', 'Start Date Time', 'End Date Time', 'Time Consumed (Minutes)',
                       'Name of Work', 'Required Time']].values,
        hovertemplate='Employee ID: %{customdata[0]}<br>Name: %{customdata[1]}<br>Start Time: %{customdata[2]}<br>End Time: %{customdata[3]}<br>Time Consumed: %{customdata[4]}<br>Name of Work: %{customdata[5]}<br>Required Time: %{customdata[6]}'
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSONbox = boxPlot()
    return render_template('reports.html', graphJSON=graphJSON, current_time=current_time, menu_items=menu_items,
                           graphJSONbox=graphJSONbox, table_html=table_html, pagination=pagination)


def boxPlot():
    selected_menu_item = request.args.get('menu')
    df = work_processBar(selected_menu_item)
    trace = go.Box(y=df['Time Consumed (Minutes)'], x=df['Name of Work'], boxpoints='all', jitter=0.3, pointpos=-1.8)
    layout = go.Layout(title='Time consuming on a side by Type of work (Minutes)')
    fig = go.Figure(data=[trace], layout=layout)
    graphJSONbox = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSONbox


def get_table(page=1):
    # selected_menu_item, selected_wip_item = form_submit()
    selected_menu_item = request.args.get('menu')
    df = work_processBar(selected_menu_item)
    pd.set_option('display.max_colwidth', None)  # display full column width
    pd.set_option('display.max_columns', None)  # display all columns
    pd.set_option('display.width', None)  # auto-detect terminal width
    df.index = np.arange(1, len(df) + 1)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    per_page = 10
    offset = (page - 1) * per_page
    paginated_df = df.iloc[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=len(df), css_framework='bootstrap4')
    return paginated_df.to_html(classes='table table-hover table-bordered'), pagination


