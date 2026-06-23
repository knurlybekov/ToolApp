# ToolApp

A Flask web application for tracking tools and equipment across geographic work sites — who is using which tool, where, and for how long — visualized on an interactive map.

## Overview

ToolApp is a GIS-backed operations dashboard. It plots employees, tools, and work zones on a Folium/Leaflet map centered on Kamloops, BC, and pairs the map with Plotly reports on tool usage and time-per-task. Authentication and per-user sessions are handled with Flask-Login.

## Features

- **Interactive map** (Folium) showing tool/employee markers and color-coded work-area polygons
- **Tool & employee tables** filterable by site, date range, and name
- **Usage reports** with Plotly bar charts (time consumed vs. required time) and box plots
- **Authentication** via Flask-Login with an `employees` user model
- **SQL Server / Azure SQL** backend over `pyodbc`
- Paginated report tables (`flask-paginate`)

## Tech Stack

Python · Flask · Flask-Login · Flask-SQLAlchemy · pyodbc (Azure SQL Server) · pandas · Folium · Plotly · APScheduler

## Project Structure

```
__init__.py     # App factory, DB + login setup
app.py          # Entry point
auth.py         # Login / auth blueprint
views.py        # Map + home views
reports.py      # Plotly reports blueprint
tables.py       # Table data endpoints
models.py       # SQLAlchemy models (employees)
dbConn.py       # DB connection + SQL queries
templates/      # Jinja2 templates
```

## Running Locally

```bash
pip install flask flask-login flask-sqlalchemy pyodbc pandas folium plotly flask-paginate apscheduler
# Requires the Microsoft ODBC Driver 18 for SQL Server
python app.py
```

Configure your database connection in `dbConn.py` before running.

> **Security note:** move database credentials out of `dbConn.py` into environment variables — do not commit connection strings.
