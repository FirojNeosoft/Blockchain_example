from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """
     User Model
    """
    __tablename__ = 'User'

    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(18), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone
        
    def __repr__(self):
        return '%s'.format(self.name)


class Employee(db.Model):
    """
     Employee Model
    """
    __tablename__ = 'Employee'
    id = db.Column('emp_id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'),
                        nullable=False)
    department = db.Column(db.String(120), nullable=False)


class Client(db.Model):
    """
     Client Model
    """
    __tablename__ = 'Client'
    id = db.Column('client_id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'),
                        nullable=False)
    location = db.Column(db.String(120), nullable=False)


class Project(db.Model):
    """
     Project Model
    """
    __tablename__ = 'Project'
    id = db.Column('project_id', db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('Client.client_id'))
    status = db.Column(db.String(1), nullable=False, default='A')
    created_at = db.Column(db.DateTime, default=datetime.now())


class EmployeeProjectMap(db.Model):
    """
     EmployeeProjectMap Model
    """
    __tablename__ = 'EmployeeProjectMap'
    id = db.Column('contract_id', db.Integer, primary_key=True)
    emp_id = db.Column('emp_id', db.Integer, db.ForeignKey('Employee.emp_id')),
    project_id = db.Column('project_id', db.Integer, db.ForeignKey('Project.project_id')),
    role = db.Column(db.String(100), nullable=False),
    start_date = db.Column(db.Date, default=datetime.today()),
    durations = db.Column(db.Integer, nullable=False),
    charges_per_hour = db.Column(db.Float, nullable=False),
    status = db.Column(db.String(1), nullable=False, default='A'),
    remark = db.Column(db.Text),
    created_at=db.Column(db.DateTime, default=datetime.now())
