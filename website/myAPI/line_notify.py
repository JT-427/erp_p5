import os
import requests
import datetime as dt
from flask_login import login_required
from flask_restful import Resource, reqparse, marshal_with, fields
from sqlalchemy.sql import func

from .. import db
from ..modules.database.flask_sqlalchemy_model import Employee, Project, ProjectLabor

class dispatchNotifyAPI(Resource):
    @login_required
    def get(self, date):
        # date = dt.date.today() + dt.timedelta(1) if dt.datetime.now().hour > 6 else dt.date.today()
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
            ProjectLabor.date == date
        ).subquery()
        query = db.session.query(
            q1.c.project_name,
            q1.c.address,
            func.group_concat(q1.c.name).label('names')
        ).group_by(
            q1.c.project_id
        ).all()
        if query:
            msg = date+'\n\n'
            for project in query:
                msg += f"📬 {project.project_name}\n地址：{project.address}\n派工：{project.names}\n\n"

            headers = {
                "Authorization": "Bearer " + os.environ.get('LINE_NOTIFY_boss_dispatch'),
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
        return '', 200