from datetime import datetime
import numpy as np
from flask import Blueprint, render_template, request, send_file
from flask_paginate import Pagination, get_page_args
import pandas as pd
from flask_login import login_required
from dbConn import connection, tableEmployees, tableTools, tableWorkinprocess, getemp

tables_bp = Blueprint('tables', __name__)
df = None

# 386ce9d230e54b3bb0f64db8b0da1238


@tables_bp.route('/tables', methods=['GET', 'POST'])
@login_required
def tables():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    menu_items = [
        {'value': 'Employees', 'label': 'Employees'},
        {'value': 'Tools', 'label': 'Tools'},
        {'value': 'Works in process', 'label': 'Works in process'}
    ]
    conn = connection()
    cursor = conn.cursor()
    cursor.execute('SELECT s_id, s_name FROM side')
    wip_items = [{'value': 0, 'label': 'All'}]
    for row in cursor:
        wip_items.append({'value': row[0], 'label': row[1]})
    selected_menu_item = request.args.get('menu')
    selected_wip_item = request.args.get('wip-items')
    nameFind = request.args.get('nameFind')
    startDate = request.args.get('startdate')
    endDate = request.args.get('enddate')
    getDF(selected_menu_item, selected_wip_item, nameFind, startDate, endDate)
    page = request.args.get('page', 1, type=int)
    table_html, pagination = get_table(page=page)
    return render_template("tables.html", menu_items=menu_items,wip_items=wip_items, table_html=table_html, pagination=pagination, current_time=current_time)


def get_table(page=1, per_page=10):
    selected_menu_item, selected_wip_item, nameFind, startDate, endDate = form_submit()
    print(nameFind)
    df = getDF(selected_menu_item, selected_wip_item, nameFind, startDate, endDate)
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


def getDF(selected_menu_item, selected_wip_item, nameFind, startDate, endDate):
    if selected_menu_item == 'Employees':
        return tableEmployees()
    elif selected_menu_item == 'Tools':
        return tableTools(selected_wip_item)
    elif selected_menu_item == 'Works in process':
        return tableWorkinprocess(selected_wip_item, startDate, endDate, nameFind)
    else:
        return pd.DataFrame()


def form_submit():
    if request.method == 'POST':
        selected_menu_item = request.form.get('menu')
        selected_wip_item = request.form.get('wip-items')
        nameFind = request.form.get('nameFind')
        startDate = request.form.get('startdate')
        endDate = request.form.get('enddate')
    elif request.method == 'GET':
        selected_menu_item = request.args.get('menu')
        selected_wip_item = request.args.get('wip-items')
        nameFind = request.args.get('nameFind')
        startDate = request.args.get('startdate')
        endDate = request.args.get('enddate')
    else:
        selected_menu_item, selected_wip_item, nameFind, startDate, endDate = None, None, None, None, None

    if nameFind and startDate and endDate:
        return selected_menu_item, selected_wip_item, nameFind, startDate, endDate
    elif nameFind and startDate:
        return selected_menu_item, selected_wip_item, nameFind, startDate, None
    elif nameFind and endDate:
        return selected_menu_item, selected_wip_item, nameFind, None, endDate
    elif startDate and endDate:
        return selected_menu_item, selected_wip_item, None, startDate, endDate
    elif nameFind:
        return selected_menu_item, selected_wip_item, nameFind, None, None
    elif startDate:
        return selected_menu_item, selected_wip_item, None, startDate, None
    elif endDate:
        return selected_menu_item, selected_wip_item, None, None, endDate
    else:
        return selected_menu_item, selected_wip_item, None, None, None



@tables_bp.route('/tables/download_csv',methods=['GET', 'POST'])
def download_csv():
    df = getemp()
    csv_data = df.to_csv(index=False)
    # convert dataframe to CSV and save to a temporary file
    with open('emplogin.csv', 'w') as f:
        f.write(csv_data)

    # send the file to the client's web browser
    return send_file('emplogin.csv', as_attachment=True)

# @tables_bp.route('/tables', methods=['GET', 'POST'])
# @login_required
# def tables():
#     current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     menu_items = [
#         {'value': 'Employees', 'label': 'Employees'},
#         {'value': 'Tools', 'label': 'Tools'},
#         {'value': 'Works in process', 'label': 'Works in process'}
#     ]
#     conn = connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT s_id, s_name FROM side')
#     wip_items = [{'value': None, 'label': 'All'}]
#     for row in cursor:
#         wip_items.append({'value': row[0], 'label': row[1]})
#     selected_menu_item, selected_wip_item, nameFind, startDate, endDate, page, per_page = form_submit()
#     table_html, pagination = get_table(selected_menu_item, selected_wip_item, nameFind, startDate, endDate, page, per_page)
#     return render_template("tables.html", menu_items=menu_items,wip_items=wip_items,table_html=table_html, pagination=pagination,current_time=current_time)
#
#
# def get_table(selected_menu_item, selected_wip_item, nameFind, startDate, endDate, page, per_page):
#     df = getDF(selected_menu_item, selected_wip_item, nameFind, startDate, endDate)
#     pd.set_option('display.max_colwidth', None)  # display full column width
#     pd.set_option('display.max_columns', None)  # display all columns
#     pd.set_option('display.width', None)  # auto-detect terminal width
#     df.index = range(1, len(df) + 1)
#     offset = (page - 1) * per_page
#     paginated_df = df.iloc[offset: offset + per_page]
#     pagination = Pagination(page=page, per_page=per_page, total=len(df), css_framework='bootstrap4')
#     return paginated_df.to_html(classes='table table-hover table-bordered'), pagination
#
#
# def getDF(selected_menu_item, selected_wip_item, nameFind, startDate, endDate):
#     if selected_menu_item == 'Employees':
#         return tableEmployees()
#     elif selected_menu_item == 'Tools':
#         return tableTools(selected_wip_item)
#     elif selected_menu_item == 'Works in process':
#         return tableWorkinprocess(selected_wip_item, startDate, endDate, nameFind)
#     else:
#         return pd.DataFrame()
#
#
# def form_submit():
#     selected_menu_item = request.args.get('menu', default=None, type=str)
#     selected_wip_item = request.args.get('wip-items', default=None, type=int)
#     nameFind = request.args.get('nameFind', default=None, type=str)
#     startDate = request.args.get('startdate', default=None, type=str)
#     endDate = request.args.get('enddate', default=None, type=str)
#     page = request.args.get('page', default=1, type=int)
#     per_page = request.args.get('per_page', default=10, type=int)
#     return selected_menu_item, selected_wip_item, nameFind, startDate, endDate, page, per_page

