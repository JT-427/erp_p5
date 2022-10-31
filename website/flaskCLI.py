import os
import requests
import pandas as pd
import numpy as np
import datetime as dt
from flask import Blueprint
from sqlalchemy.sql import func

from website.modules.matraila_suppler import MatarialSupplierC

from . import db
from .modules import CustomerC, CompanyC, MatarialC, StorehouseC, OutsourcerC, EmployeeC
from .modules.database.flask_sqlalchemy_model import Employee, EmployeePayment, Project, ProjectLabor, Users

cli = Blueprint('cli', __name__, cli_group=None)

@cli.cli.command('line_notify_test')
def line_notify_test():
    headers = {
        "Authorization": "Bearer " + os.environ.get('LINE_NOTIFY_p5'),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        "message": '📬測試訊息'
    }
    requests.post(
        "https://notify-api.line.me/api/notify",
        headers=headers, 
        params=params
    )
    return ''
@cli.cli.command('dispatch_notification')
def dispatch_notification():
    q1 = db.session.query(
        ProjectLabor.employee_id,
        ProjectLabor.project_id,
        Project.project_name,
        Project.address,
        Employee.name
    ).join(
        Project
    ).join(
        Employee
    ).filter(
        ProjectLabor.assigned == 1,
        ProjectLabor.date == dt.date.today() + dt.timedelta(1)
    ).subquery()
    query = db.session.query(
        q1.c.project_name,
        q1.c.address,
        func.group_concat(q1.c.name).label('names')
    ).group_by(
        q1.c.project_id
    ).all()
    if query:
        msg = (dt.date.today() + dt.timedelta(1)).strftime("%Y-%m-%d\n\n")
        for project in query:
            msg += f"📬 {project.project_name}\n地址：{project.address}\n派工：{project.names}\n\n"

        headers = {
            "Authorization": "Bearer " + os.environ.get('LINE_NOTIFY_p5'),
            "Content-Type": "application/x-www-form-urlencoded"
        }
        params = {
            "message": msg
        }
        requests.post(
            "https://notify-api.line.me/api/notify",
            headers=headers, 
            params=params
        )

@cli.cli.command('check_matarial')
def check_matarial():
    result = db.session.execute(
        """
        call check_matarial()
        """
    ).fetchall()
    for i in result:
        print(i.remaining_should_be == i.remaining)
