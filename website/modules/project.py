import random
import datetime as dt
from sqlalchemy import desc, null, or_, and_
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from flask_login import current_user

from .. import db
from ..modules.database.flask_sqlalchemy_model import Company, Customer, Matarial, MatarialUsingRecord, MatarialBuyingRecord, MiscellaneousExpenditure, Outsourcer, Project, ProjectDetail, ProjectLabor, ProjectOutsourced, Employee, HiredRecord, ProjectPayment, Salary
class ProjectC:
    def __init__(self, project_id:str=None) -> None:
        if project_id:
            self.project_id = project_id

    def check_id(callback):
        def inner(self, *args, **kwargs):
            assert self.project_id, 'Please set the project_id first.'
            return callback(self, *args, **kwargs)
        return inner

    @check_id
    def get_info(self):
        project_query = db.session.query(
            Project.project_id,
            Project.project_name,
            Project.address,
            Project.invoice,
            Project.singing_date,
            Project.start_date,
            Project.finish_date,
            Project.customer_id,
            Project.account_receivable,
            Project.company_id,
            Project.referrer,
            Project.commision,
            Customer.customer_name,
            Company.company_name
        ).join(
            Customer
        ).join(
            Company
        ).filter(
            Project.project_id == self.project_id
        ).first()

        return project_query
    
    @check_id
    def get_details(self) -> list:
        query = db.session.query(
            ProjectDetail
        ).filter(
            ProjectDetail.project_id == self.project_id
        ).all()
        return query

    @check_id
    def modify_details(self, description, unit, quantity, unit_price, price, date=dt.date.today(), sn=None):
        project_id = self.project_id
        delta = 0
        if sn:
            query = db.session.query(
                ProjectDetail
            ).filter(
                ProjectDetail.sn == sn
            ).first()

            delta = price - query.price

            query.date = date
            query.unit = unit
            query.quantity = quantity
            query.unit_price = unit_price
            query.price = price

        else:
            new_details = ProjectDetail(
                project_id = project_id,
                description = description,
                unit = unit,
                quantity = quantity,
                unit_price = unit_price,
                price = price,
                date = date
            )
            db.session.add(new_details)
            delta = price

        project_query = db.session.query(
            Project
        ).filter(
            Project.project_id == project_id
        ).first()

        project_query.account_receivable += delta*1.05 if project_query.invoice else delta
        if project_query.account_receivable < 0:
            project_query.account_receivable = 0

        db.session.commit()
    @check_id
    def delete_detail(self, sn):
        project_id = self.project_id

        sql = db.session.query(
            ProjectDetail
        ).filter(
            ProjectDetail.sn == sn
        )

        query = sql.first()

        project_query = db.session.query(
            Project
        ).filter(
            Project.project_id == project_id
        ).first()
        project_query.account_receivable -= query.price*1.05 if project_query.invoice else query.price
        if project_query.account_receivable < 0:
            project_query.account_receivable = 0

        sql.delete()
        db.session.commit()

    @check_id
    def get_dispatches_by_date(self, date: str):
        project_id = self.project_id
        date = dt.datetime.strptime(date, '%Y-%m-%d')

        pl = db.session.query(
            ProjectLabor
        ).filter(
            ProjectLabor.project_id == project_id,
            ProjectLabor.date == date
        ).subquery()

        query = db.session.query(
            Employee.employee_id,
            Employee.name,
            pl.c.assigned
        ).join(
            HiredRecord
        ).outerjoin(
            pl
        ).filter(
            HiredRecord.hired_date <= date,
            or_(
                HiredRecord.resigned_date == null(),
                HiredRecord.resigned_date >= date,
            )
        ).all()
        return query
    @check_id
    def get_all_dispatches(self):
        project_id = self.project_id
        query = db.session.query(
            ProjectLabor.date,
            ProjectLabor.employee_id,
            Employee.name,
            ProjectLabor.assigned,
            ProjectLabor.working_days
        ).filter(
            ProjectLabor.project_id == project_id
        ).join(
            Employee
        ).order_by(
            desc(ProjectLabor.date)
        ).all()
        return query

    @check_id
    def dispatch(self, employee_id, date, assigned):
        project_id = self.project_id
        
        query = db.session.query(
            ProjectLabor
        ).filter(
            ProjectLabor.project_id == project_id,
            ProjectLabor.employee_id == employee_id,
            ProjectLabor.date == date
        )
        if query.first():
            if assigned:
                query.first().assigned=assigned
            else:
                query.delete()
            db.session.commit()
        else:
            if assigned:
                assignment = ProjectLabor(project_id=project_id, employee_id=employee_id, date=date, assigned=True)
                db.session.add(assignment)
                db.session.commit()
    @check_id
    def get_outsourced(self):
        project_id = self.project_id
        query = db.session.query(
            ProjectOutsourced.sn,
            ProjectOutsourced.project_id,
            ProjectOutsourced.outsourcer_id,
            ProjectOutsourced.description,
            ProjectOutsourced.price,
            ProjectOutsourced.date,
            ProjectOutsourced.notes,
            func.concat(Outsourcer.outsourcer_name, ' (', Outsourcer.notes, ')').label('outsourcer_name')
        ).join(
            Outsourcer
        ).filter(
            ProjectOutsourced.project_id == project_id
        ).all()
        return query
    @check_id
    def modify_outsourced(self, outsourcer_id: str, description: str, price: float, date: str, notes: str=None, sn: int=None):
        project_id = self.project_id

        if sn:
            db.session.query(
                ProjectOutsourced
            ).filter(
                ProjectOutsourced.sn == sn,
                ProjectOutsourced.project_id == project_id
            ).update(
                {
                    'outsourcer_id': outsourcer_id,
                    'description': description,
                    'price': price,
                    'date': date,
                    'notes': notes
                }
            )
        else:
            new = ProjectOutsourced(
                project_id=project_id,
                outsourcer_id=outsourcer_id,
                description=description,
                price=price,
                date=date,
                notes=notes
            )
            db.session.add(new)
        db.session.commit()
        return True
    @check_id
    def delete_outsourced(self, sn: int):
        project_id = self.project_id
        db.session.query(
            ProjectOutsourced
        ).filter(
            ProjectOutsourced.sn == sn,
            ProjectOutsourced.project_id == project_id
        ).delete()
        db.session.commit()
        return True

    @check_id
    def get_cost(self):
        project_id = self.project_id
        labor = db.session.query(
            ProjectLabor.project_id,
            ProjectLabor.employee_id,
            Employee.name,
            func.sum(
                ProjectLabor.working_days
            ).label("working_days"),
            func.sum(
                func.IF(
                    Salary.unit == '日',
                    ProjectLabor.working_days * Salary.salary,
                    ProjectLabor.working_days * Salary.salary/30
                )
            ).label("payment")
        ).filter(
            ProjectLabor.project_id == project_id
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
        ).join(
            Employee,
            ProjectLabor.employee_id == Employee.employee_id
        ).group_by(
            ProjectLabor.employee_id
        ).all()

        matarial = db.session.query(
            MatarialUsingRecord.matarial_id,
            Matarial.matarial_name,
            func.sum(
                MatarialUsingRecord.quantity
            ).label("quantity"),
            func.sum(
                MatarialUsingRecord.quantity * (MatarialBuyingRecord.price/MatarialBuyingRecord.quantity)
            ).label("cost")
        ).filter(
            MatarialUsingRecord.project_id == project_id
        ).join(
            MatarialBuyingRecord,
            MatarialUsingRecord.matarial_buying_sn == MatarialBuyingRecord.sn
        ).join(
            Matarial,
            MatarialUsingRecord.matarial_id == Matarial.matarial_id
        ).group_by(
            MatarialUsingRecord.matarial_id
        ).all()

        outsourced = db.session.query(
            ProjectOutsourced.outsourcer_id,
            Outsourcer.outsourcer_name,
            func.count(

            ).label('count'),
            func.sum(
                ProjectOutsourced.price
            ).label('payment')
        ).join(
            Outsourcer
        ).filter(
            ProjectOutsourced.project_id == project_id
        ).group_by(
            ProjectOutsourced.outsourcer_id
        ).all()

        miscellaneous_expenditure = db.session.query(
            func.sum(
                MiscellaneousExpenditure.price
            ).label('total')
        ).filter(
            MiscellaneousExpenditure.project_id == project_id
        ).group_by(
            MiscellaneousExpenditure.project_id            
        ).first()

        commision = db.session.query(
            Project.referrer,
            Project.commision
        ).filter(
            Project.project_id == project_id
        ).first()
        return {
            'labor': labor,
            'matarial': matarial,
            'outsourced': outsourced,
            'miscellaneous_expenditure': miscellaneous_expenditure,
            'commision': commision
        }

    def get_payment(self):
        query = db.session.query(
            ProjectPayment
        ).filter(
            ProjectPayment.project_id == self.project_id
        ).all()
        return query
    def modify_payment(self, **kwargs):
        kwargs['project_id'] = self.project_id
        if 'sn' in kwargs and bool(kwargs['sn']) == True:
            sn = kwargs['sn']
            del kwargs['sn']
            db.session.query(
                ProjectPayment
            ).filter(
                ProjectPayment.project_id == self.project_id,
                ProjectPayment.sn == sn
            ).update(kwargs)
        else:
            new = ProjectPayment(**kwargs)
            db.session.add(new)
        db.session.commit()
        return ''
    def delete_payment(self, sn):
        db.session.query(
            ProjectPayment
        ).filter(
            ProjectPayment.project_id == self.project_id,
            ProjectPayment.sn == sn
        ).delete()
        db.session.commit()
        return ''

    def create(self, **kwargs):
        new = Project(**kwargs)

        def id_gen():
            a = new.customer_id[-10:] # 10
            b = hex(random.randint(16**6+1, 16**7))[2:] # 7
            d = oct(int(dt.date.today().strftime('%Y%m%d')))[2:]
            lef = a + b + d
            e = hex(random.randint(16**(32-len(lef)-1)+1, 16**(32 - len(lef))))[2:]
            return lef + e
        new.project_id = id_gen()

        db.session.add(new)
        try:
            db.session.commit()
        except IntegrityError:
            new.project_id = id_gen()
            db.session.add(new)
            db.session.commit()
    def modify(self, **kwargs):
        project_id = self.project_id
        query = db.session.query(
            Project
        ).filter(
            Project.project_id == project_id
        ).first()
        if 'invoice' in kwargs and query.invoice != kwargs['invoice']:
            sum_ = sum([d.price for d in query.ProjectDetail])
            kwargs['account_receivable'] = sum_*1.05 if kwargs['invoice'] else sum_

        db.session.query(
            Project
        ).filter(
            Project.project_id == project_id
        ).update(kwargs)
        db.session.commit()

    def delete(self):
        project_id = self.project_id
        db.session.query(
            Project
        ).filter(
            Project.project_id == project_id
        ).delete()
        db.session.commit()

    def get_all_project(self, date:str='') -> tuple:
        # db.session.close_all()
        # with db.session.begin():
        #     db.session.execute(
        #         f'SET @user_id = {current_user.user_id}'
        #     )
        #     db.session.execute(
        #         'select @user_id'
        #     ).one()
        projects_query = db.session.query(
            Project.project_id,
            Project.project_name,
            Project.address,
            Project.invoice,
            Project.singing_date,
            Project.start_date,
            Project.finish_date,
            Project.customer_id,
            Project.company_id,
            Project.referrer,
            Project.commision,
            Customer.customer_name,
            Company.company_name
        ).join(
            Customer
        ).join(
            Company
        ).filter(
            or_(date=='', Project.singing_date <= date),
            or_(date=='', Project.finish_date==null(), Project.finish_date >= date)
        ).order_by(
            desc(Project.start_date)
        ).all()
        return projects_query