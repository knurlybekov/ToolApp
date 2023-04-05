from flask_login import UserMixin
from __init__ import db


class employees(UserMixin, db.Model):
    __tablename__ = 'employees'
    e_id = db.Column(db.NUMERIC, primary_key=True)
    e_fname = db.Column(db.NVARCHAR(50), nullable=False)
    e_lname = db.Column(db.NVARCHAR(50), nullable=False)
    e_position = db.Column(db.NVARCHAR(60), nullable=False)
    e_department = db.Column(db.NVARCHAR(50), nullable=False)
    e_photo = db.Column(db.VARBINARY(max))
    e_login = db.Column(db.NVARCHAR(100), nullable=False)
    e_password = db.Column(db.NVARCHAR(50), nullable=False)
