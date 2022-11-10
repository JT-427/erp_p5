import calendar
import datetime as dt
from sqlalchemy.sql import func, and_, or_

from .. import db
from .database.flask_sqlalchemy_model import (
    Project, ProjectPayment, ProjectDetail, ProjectOutsourced, ProjectLabor, 
    Salary,
    Matarial, MatarialBuyingRecord, MatarialUsingRecord,
    Outsourcer,
    MiscellaneousExpenditure,
    Customer
)

class ReportsC:
    def __init__(self) -> None:
        pass

    def monthly_terminated_projects(self, year, month):
        # customer name, end date, project name, income, cost, net income
        projects = db.session.query(
            Project
        ).filter(
            and_(
                Project.finish_date >= dt.date(year, month, 1),
                Project.finish_date <= dt.date(year, month, calendar.monthrange(year, month)[1])
            )
            
        ).subquery()

        payments = db.session.query(
            ProjectPayment.project_id,
            func.sum(
                ProjectPayment.amount
            ).label("income")
        ).group_by(
            ProjectPayment.project_id
        ).subquery()

        # cost
        labor = db.session.query(
            ProjectLabor.project_id,
            func.sum(
                func.IF(
                    Salary.unit == '日',
                    ProjectLabor.working_days * Salary.salary,
                    ProjectLabor.working_days * Salary.salary/30
                )
            ).label("payment")
        ).join(
            Salary,
            and_(
                ProjectLabor.employee_id == Salary.employee_id,
                or_(
                    Salary.end_date == None,
                    ProjectLabor.date <= Salary.end_date
                ),
                ProjectLabor.date >= Salary.start_date
            )
        ).group_by(
            ProjectLabor.project_id
        ).subquery()
        matarial = db.session.query(
            MatarialUsingRecord.project_id,
            func.sum(
                MatarialUsingRecord.quantity * (MatarialBuyingRecord.price/MatarialBuyingRecord.quantity)
            ).label("cost")
        ).join(
            MatarialBuyingRecord,
            MatarialUsingRecord.matarial_buying_sn == MatarialBuyingRecord.sn
        ).join(
            Matarial,
            MatarialUsingRecord.matarial_id == Matarial.matarial_id
        ).group_by(
            MatarialUsingRecord.project_id
        ).subquery()
        outsourced = db.session.query(
            ProjectOutsourced.project_id,
            func.sum(
                ProjectOutsourced.price
            ).label('payment')
        ).join(
            Outsourcer
        ).group_by(
            ProjectOutsourced.project_id
        ).subquery()
        miscellaneous_expenditure = db.session.query(
            MiscellaneousExpenditure.project_id,
            func.sum(
                MiscellaneousExpenditure.price
            ).label('payment')
        ).group_by(
            MiscellaneousExpenditure.project_id            
        ).subquery()

        query = db.session.query(
            projects.c.project_id,
            projects.c.project_name,
            Customer.customer_name,
            projects.c.finish_date,
            payments.c.income,
            (
                func.IF(
                    labor.c.payment != None,
                    labor.c.payment,
                    0
                ) +
                func.IF(
                    matarial.c.cost != None,
                    matarial.c.cost,
                    0
                ) +
                func.IF(
                    outsourced.c.payment != None,
                    outsourced.c.payment,
                    0
                ) +
                func.IF(
                    miscellaneous_expenditure.c.payment != None,
                    miscellaneous_expenditure.c.payment,
                    0   
                ) +
                func.IF(
                    projects.c.commision != None,
                    projects.c.commision,
                    0   
                )
            ).label('cost')
        ).outerjoin(
            payments,
            projects.c.project_id == payments.c.project_id
        ).outerjoin(
            labor,
            projects.c.project_id == labor.c.project_id
        ).outerjoin(
            matarial,
            projects.c.project_id == matarial.c.project_id
        ).outerjoin(
            outsourced,
            projects.c.project_id == outsourced.c.project_id
        ).outerjoin(
            miscellaneous_expenditure,
            projects.c.project_id == miscellaneous_expenditure.c.project_id
        ).join(
            Customer,
            projects.c.customer_id == Customer.customer_id
        ).all()
        return query