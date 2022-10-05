import datetime as dt
from sqlalchemy import desc, null, or_, and_
from sqlalchemy.sql import func
from flask_login import current_user

from .. import db
from ..modules.database.flask_sqlalchemy_model import Employee, MiscellaneousExpenditure, Project, Users

class MiscellaneousExpenditureC:
    def __init__(self) -> None:
        pass
    def get_records(self, sn: int=None):
        sub_users = db.session.query(
            Users.user_id,
            Employee.name
        ).join(
            Employee
        ).subquery()
        query = db.session.query(
            MiscellaneousExpenditure.sn, 
            MiscellaneousExpenditure.date, 
            MiscellaneousExpenditure.employee_id, 
            Employee.name,
            MiscellaneousExpenditure.project_id, 
            Project.project_name,
            MiscellaneousExpenditure.description, 
            MiscellaneousExpenditure.classification, 
            MiscellaneousExpenditure.price, 
            MiscellaneousExpenditure.user_id,
            sub_users.c.name.label('register')
        ).outerjoin(
            Project
        ).outerjoin(
            Employee
        ).join(
            sub_users,
            MiscellaneousExpenditure.user_id == sub_users.c.user_id
        ).filter(
            or_(
                sum([ 1 if i.role_name == 'admin' else 0 for i in current_user.user_roles]) != 0,
                MiscellaneousExpenditure.user_id == current_user.user_id
            ),
            or_(
                sn == None,
                MiscellaneousExpenditure.sn == sn
            )
        ).order_by(
            desc(MiscellaneousExpenditure.sn)
        ).all()
        return query
    def modify(self, **kwargs):
        kwargs['user_id'] = current_user.user_id
        if 'sn' in kwargs and kwargs['sn'] != None:
            sn = kwargs['sn']
            del kwargs['sn']
            db.session.query(
                MiscellaneousExpenditure
            ).filter(
                MiscellaneousExpenditure.sn == sn
            ).update(
                kwargs
            )
            db.session.commit()
        else:
            db.session.add(
                MiscellaneousExpenditure(**kwargs)
            )
            db.session.commit()
        return True
    def delete(self, sn):
        db.session.query(
            MiscellaneousExpenditure
        ).filter(
            MiscellaneousExpenditure.sn == sn
        ).delete()
        db.session.commit()
        return True