import os
from datetime import datetime

import pyodbc
import pandas as pd


def connection():
    conn = pyodbc.connect(
        f"Driver={os.environ.get('TOOLAPP_DB_DRIVER', '{ODBC Driver 18 for SQL Server}')};"
        f"Server=tcp:{os.environ['TOOLAPP_DB_SERVER']},1433;Database={os.environ['TOOLAPP_DB_NAME']};"
        f"Uid={os.environ['TOOLAPP_DB_USER']};Pwd={os.environ['TOOLAPP_DB_PASSWORD']};"
        "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    cursor = conn.cursor()
    return conn


def tableEmployees():
    conn = connection()
    sql_query = "SELECT e_id as 'Employee ID', concat(e_fname,' ', e_lname) as 'Employee Name', e_position AS 'Position', e_department AS 'Department' FROM employees"
    df = pd.read_sql_query(sql_query, conn)
    df = df.drop(df.columns[0], axis=1)
    return df


def tableTools(side):
    side = int(side)
    conn = connection()
    print(side)
    if side == 0:
        sql_query = "SELECT t_inv as 'Toool Inventory Number', t_type AS 'Tool Type', t_name AS 'Tool Name', t_status AS 'Tool Satus' FROM tools"
        df = pd.read_sql_query(sql_query, conn)
        df = df.drop(df.columns[0], axis=1)
        return df
    elif 1<=side<=3:
        sql_query = "SELECT t_inv as 'Toool Inventory Number', t_type AS 'Tool Type', t_name AS 'Tool Name', t_status AS 'Tool Satus' FROM tools where t_s_id like ?"
        df = pd.read_sql_query(sql_query, conn, params=[side])
        df = df.drop(df.columns[0], axis=1)
        return df


def tableWorkinprocess(side, startdate, enddate, name_filter):
    conn = connection()
    side = int(side)
    if side == 0:
        sql_query = "select e.e_id as 'Employee ID', concat(e.e_fname,' ', e.e_lname) as 'Employee Name', e.e_position as 'Employee Job Title', e.e_department as 'Employees` Department', t.t_name as 'Tool Name', t.t_type as 'Tool Type', wp_start_time as 'Start time', wp_end_time as 'End time' from work_process join employees e on e.e_id = work_process.wp_employee_id join tools t on t.t_inv = work_process.wp_tool_inv join side s on s.s_id = t.t_s_id"
        params = []
        if startdate is None and enddate is None:
            pass
        elif startdate and enddate:
            sql_query += " and wp_start_time >= ? and wp_end_time <= ?"
            params.extend([startdate, enddate])
        elif startdate:
            today = datetime.now().strftime('%Y-%m-%d')
            sql_query += " and wp_start_time >= ? and wp_end_time <= ?"
            params.extend([startdate, today])
        elif enddate:
            sql_query += " and wp_start_time >= '0000-00-00' and wp_end_time <= ?"
            params.append(enddate)
        if name_filter:
            sql_query += " and concat(e.e_fname,' ', e.e_lname) LIKE ?"
            params.append(f"%{name_filter}%")
        df = pd.read_sql_query(sql_query, conn, params=params)
        df = df.drop(df.columns[0], axis=1)
        return df
    elif 1 <=side<=3:
        sql_query = "select e.e_id as 'Employee ID', concat(e.e_fname,' ', e.e_lname) as 'Employee Name', e.e_position as 'Employee Job Title', e.e_department as 'Employees` Department', t.t_name as 'Tool Name', t.t_type as 'Tool Type', wp_start_time as 'Start time', wp_end_time as 'End time' from work_process join employees e on e.e_id = work_process.wp_employee_id join tools t on t.t_inv = work_process.wp_tool_inv join side s on s.s_id = t.t_s_id where wp_side_id like ?"
        params = [side]
        if startdate is None and enddate is None:
            pass
        elif startdate and enddate:
            sql_query += " and wp_start_time >= ? and wp_end_time <= ?"
            params.extend([startdate, enddate])
        elif startdate:
            today = datetime.now().strftime('%Y-%m-%d')
            sql_query += " and wp_start_time >= ? and wp_end_time <= ?"
            params.extend([startdate, today])
        elif enddate:
            sql_query += " and wp_start_time >= '0000-00-00' and wp_end_time <= ?"
            params.append(enddate)
        if name_filter:
            sql_query += " and concat(e.e_fname,' ', e.e_lname) LIKE ?"
            params.append(f"%{name_filter}%")
        df = pd.read_sql_query(sql_query, conn, params=params)
        df = df.drop(df.columns[0], axis=1)
        return df




def getUser(e_login):
    conn = connection()
    sql_query = "SELECT e_login, e_password, e_id, e_fname, e_lname,e_position FROM employees WHERE e_login = ?"
    params = (e_login)
    # execute the query with the parameter values
    cursor = conn.cursor()
    cursor.execute(sql_query, params)
    # fetch the results
    result = cursor.fetchone()
    if result:
        # assign the values to separate variables
        e_login_result, e_password_result, e_id_result, e_fname_result, e_lname_result, e_position_result = result
        print(e_login_result, e_password_result,  e_id_result, e_fname_result, e_lname_result, e_position_result)
        return e_login_result, e_password_result, e_id_result, e_fname_result, e_lname_result, e_position_result
    else:
        return None, None, None, None, None, None


def getToolsOnSides(side):
    conn = connection()
    cursor = conn.cursor()
    sql_query = "select t_name, t_status, t_position_lat, t_position_lon, t_s_id from tools where t_s_id = ?"
    params = (side)
    cursor.execute(sql_query, params)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=['Tool Name', 'Tool Status', 'Latitude', 'Longitude', 'On side'])
    return df


def getWorksOnSides(side):
    conn = connection()
    cursor = conn.cursor()
    sql_query = "select e.e_fname, e.e_lname, e.e_position, t.t_name, t.t_type, wp_start_time, wp_end_time, wp_side_id from work_process join employees e on e.e_id = work_process.wp_employee_id join tools t on t.t_inv = work_process.wp_tool_inv where wp_side_id = ?"
    params = (side)
    cursor.execute(sql_query, params)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=['Employee First Name', 'Employee Last Name', 'Employee job Title', 'Tool Name', 'Tool Type', 'Start Time', 'End Time'])
    return df


def getWorks():
    conn = connection()
    sql_query = "select e.e_id as 'Employee ID', e.e_fname as 'Employee First Name', e.e_lname as 'Employee Last Name', e.e_position as 'Employee Job Title', e.e_department as 'Employees` Department', t.t_name as 'Tool Name', t.t_type as 'Tool Type', t.t_position_lat as 'Latitude', t.t_position_lon as 'Longitude', wp_start_time as 'Start time', wp_end_time as 'End time', s.s_color as 'Color', wp_worklist_id as 'Work' from work_process join employees e on e.e_id = work_process.wp_employee_id join tools t on t.t_inv = work_process.wp_tool_inv join side s on s.s_id = t.t_s_id where wp_end_time is null "
    df = pd.read_sql_query(sql_query, conn, index_col='Employee ID')
    return df


def getAreas():
    conn = connection()
    sql_query = "select s_id, s_name, s_lat as 'Latitude', s_lon as 'Longitude', s_color as 'Color' from side"
    df = pd.read_sql_query(sql_query, conn)
    return df


def work_processBar(side):
    global df
    conn = connection()
    if side is not None:
        side=int(side)
    if side is None:
        sql_query = "SELECT wp_id AS 'Number of Completed Work', wp_employee_id AS 'Employee ID', concat(e_fname, ' ', e_lname) as 'Name', SUM(DATEDIFF(second, wp_start_time, wp_end_time))/60 AS 'Time Consumed (Minutes)', wp_start_time as 'Start Date Time', wp_end_time as 'End Date Time',wp_worklist_id, wl_name as 'Name of Work',wl_id, wl_time_required AS 'Required Time', wp_side_id as 'Work' FROM work_process JOIN employees on work_process.wp_employee_id = employees.e_id JOIN work_list wl ON work_process.wp_worklist_id = wl.wl_id WHERE wp_end_time IS NOT NULL GROUP BY wp_employee_id, wp_id, wp_worklist_id, wl_id, wl_time_required, wp_side_id, wp_end_time, wp_start_time, e_lname, e_fname, wl_name"
        df = pd.read_sql_query(sql_query, conn)
        return df
    elif 1 <= side <= 3:
        sql_query = "SELECT wp_id AS 'Number of Completed Work', wp_employee_id AS 'Employee ID', concat(e_fname, ' ', e_lname) as 'Name', SUM(DATEDIFF(second, wp_start_time, wp_end_time))/60 AS 'Time Consumed (Minutes)', wp_start_time as 'Start Date Time', wp_end_time as 'End Date Time',wp_worklist_id, wl_name as 'Name of Work',wl_id, wl_time_required AS 'Required Time', wp_side_id as 'Work' FROM work_process JOIN employees on work_process.wp_employee_id = employees.e_id JOIN work_list wl ON work_process.wp_worklist_id = wl.wl_id WHERE wp_end_time IS NOT NULL and wp_side_id like ? GROUP BY wp_employee_id, wp_id, wp_worklist_id, wl_id, wl_time_required, wp_side_id, wp_end_time, wp_start_time, e_lname, e_fname, wl_name"
        params = [side]
        df = pd.read_sql_query(sql_query, conn, params=params)
        return df



def boxPlot():
    conn = connection()
    sql_query = "SELECT wp_id AS 'Number of Completed Work', wp_employee_id AS 'Employee ID', SUM(DATEDIFF(second, wp_start_time, wp_end_time))/60 AS 'Time Consumed (Minutes)', wp_worklist_id, wl_id, wl_time_required AS 'Required Time' FROM work_process JOIN work_list wl ON work_process.wp_worklist_id = wl.wl_id WHERE wp_end_time IS NOT NULL GROUP BY wp_employee_id, wp_id, wp_worklist_id, wl_id, wl_time_required"
    df = pd.read_sql_query(sql_query, conn)
    return df


def getemp():
    conn = connection()
    sql_query = "select * from employees"
    df = pd.read_sql_query(sql_query, conn)
    return df
