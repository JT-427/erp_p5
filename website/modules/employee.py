import random
import datetime as dt

from sqlalchemy import desc, null, or_, and_
from sqlalchemy.sql import func

from .. import db
from .database.flask_sqlalchemy_model import Employee, EmployeePayment, HiredRecord, RUsersRole, Salary, ProjectLabor, Project, Users

class EmployeeC:
    def __init__(self, employee_id:str=None) -> None:
        if employee_id:
            self.employee_id = employee_id
            self.get_employee_info()
            
    def get_employee_info(self):
        employee_query = db.session.query(Employee).\
            filter(
                Employee.employee_id == self.employee_id
            ).first()
        if employee_query:
            self.name = employee_query.name
            self.sex = employee_query.sex
            self.birthday = employee_query.birthday
            self.telephone = employee_query.telephone
            self.cellphone = employee_query.cellphone
            self.address = employee_query.address
            self.email = employee_query.email 
        # else:
        #     return None

    def create(self, info):
        """
        {
            'name': name,
            'sex': sex,
            'birthday': birthday,
            'telephone': telephone,
            'cellphone': cellphone,
            'address': address,
            'hired_date': hired_date,
            'salary': salary,
            'salary_unit': salary_unit
        }

        """
        name = info['name']
        sex = info['sex']
        birthday = dt.datetime.strptime(info['birthday'], '%Y-%m-%d')
        telephone = info['telephone'] if info['telephone'] else None
        cellphone = info['cellphone'] if info['cellphone'] else None
        address = info['address'] if info['address'] else None
        email = info['email'] if info['email'] else None
        hired_date = dt.datetime.strptime(info['hired_date'], '%Y-%m-%d')
        salary = info['salary']
        salary_unit = info['salary_unit']


        a = hex(random.randint(16**3+1, 16**4))[2:] # 4
        b = oct(random.randint(8**9+1, 8**10))[2:] # 10
        c = str(random.randint(10287, 99874)) # 5

        employee_id = a + info['sex'] + b + birthday.strftime('%m%d') + c + hired_date.strftime('%y%m') + str(random.randint(1022, 9911))
        new_employee = Employee(
            employee_id=employee_id,
            name=name,
            sex=sex,
            birthday=birthday,
            telephone=telephone,
            cellphone=cellphone,
            address=address,
            email=email,
        )
        db.session.add(new_employee)

        new_hire = HiredRecord(
            employee_id=employee_id,
            hired_date=hired_date
        )
        db.session.add(new_hire)

        new_salary = Salary(
            employee_id=employee_id,
            salary=salary,
            unit=salary_unit,
            start_date=hired_date
        )
        db.session.add(new_salary)

        new_user = Users(
            employee_id = employee_id
        )
        db.session.add(new_user)

        user_id = db.session.query(
            Users.user_id
        ).filter(
            Users.employee_id == employee_id
        ).first()[0]
        db.session.add(
            RUsersRole(
                role_id = 1,
                user_id = user_id
            )
        )
        db.session.commit()
    
    def modify(self, name, sex, birthday, telephone, cellphone, address, email):
        empoloyee_id = self.employee_id
        employee = db.session.query(
            Employee
        ).filter(
            Employee.employee_id == empoloyee_id
        ).first()
        employee.name = name
        employee.sex = sex
        employee.birthday = birthday
        employee.telephone = telephone
        employee.cellphone = cellphone
        employee.address = address
        employee.email = email
        db.session.commit()
        return ''

    def get_salary_record(self):
        employee_id = self.employee_id
        query = db.session.query(
            Salary
        ).filter(
            Salary.employee_id == employee_id
        ).order_by(
            desc(Salary.start_date)
        ).all()
        return query
    def modify_salary_record(self, sn, start_date, salary, unit):
        employee_id = self.employee_id

        def edit_previous_record(sn, start_date):
            query = db.session.query(
                Salary
            ).filter(
                Salary.sn != sn,
                Salary.employee_id == employee_id,
                Salary.start_date < start_date
            ).order_by(
                desc(Salary.start_date)
            ).first()
            if query:
                query.end_date = dt.datetime.strptime(start_date, '%Y-%m-%d') - dt.timedelta(days=1)

        if sn:
            record = db.session.query(
                Salary
            ).filter(
                Salary.sn == sn,
                Salary.employee_id == employee_id
            ).first()
            if record.start_date != start_date:
                edit_previous_record(sn, start_date)
                record.start_date = start_date
            record.salary = salary
            record.unit = unit
        else:
            edit_previous_record(sn, start_date)
            new = Salary(
                employee_id = employee_id,
                salary = salary,
                unit = unit,
                start_date = start_date
            )
            db.session.add(new)
        db.session.commit()
        return True
    def delete_salary_record(self, sn):
        employee_id = self.employee_id
        db.session.query(
            Salary
        ).filter(
            Salary.sn == sn,
            Salary.employee_id == employee_id
        ).delete()
        query = db.session.query(
            Salary
        ).filter(
            Salary.employee_id == employee_id
        ).order_by(
            desc(Salary.start_date)
        ).all()
        query[-1].end_date = null()
        db.session.commit()
        return True
    
    def get_dispatches(self, year, month):
        start = dt.date(int(year), int(month), 11)
        end = start + dt.timedelta(days=30)
        end = dt.date(end.year, end.month, 10)

        employee_id = self.employee_id
    
        pl_sub = db.session.query(
            ProjectLabor
        ).filter(
            ProjectLabor.date <= end,
            ProjectLabor.date >= start,
            ProjectLabor.employee_id == employee_id,
            ProjectLabor.assigned == 1
        ).subquery()
        
        query = db.session.query(
            pl_sub.c.date,
            func.group_concat(
                Project.project_name
            ).label('project_name'),
            func.sum(
                pl_sub.c.working_days
            ).label('working_days'),
            func.sum(
                pl_sub.c.working_days * Salary.salary
            ).label("accounts_payable")
        ).join(
            pl_sub,
            pl_sub.c.project_id == Project.project_id
        ).outerjoin(
            Salary,
            and_(
                pl_sub.c.employee_id == Salary.employee_id,
                or_(
                    Salary.end_date == None,
                    pl_sub.c.date <= Salary.end_date
                ),
                pl_sub.c.date >= Salary.start_date
            )
        ).group_by(
            pl_sub.c.date
        ).order_by(
            desc(pl_sub.c.date)
        ).all()
        return query
    
    def get_dispatches_by_date(self, date: str):
        employee_id = self.employee_id
        query = db.session.query(
            ProjectLabor.project_id,
            ProjectLabor.date,
            ProjectLabor.working_days,
            Project.project_name
        ).join(
            Project
        ).filter(
            ProjectLabor.employee_id == employee_id,
            ProjectLabor.date == date,
            ProjectLabor.assigned == 1
        ).all()
        return query

    def modify_dispatches(self, date:str, projects:dict, working_days:float=1.0):
        employee_id = self.employee_id

        count = sum([ 1 if i else 0 for i in projects.values()])
        days = []
        for i in range(count-1):
            days.append(working_days/count)
        days.append(working_days-sum(days))

        query = db.session.query(
            ProjectLabor
        ).filter(
            ProjectLabor.date == date,
            ProjectLabor.employee_id == employee_id
        ).all()

        days_pos = 0
        for i in query:
            if projects[i.project_id] == True:
                i.working_days = days[days_pos]
                days_pos += 1
            else:
                i.working_days = None
        db.session.commit()
        return True
    def delete_dispatches(self, date:str):
        employee_id = self.employee_id

        db.session.query(
            ProjectLabor
        ).filter(
            ProjectLabor.date == date,
            ProjectLabor.employee_id == employee_id
        ).delete()
        db.session.commit()
        return True
    def report_dispatches(self, date: str, projects: dict):
        employee_id = self.employee_id

        count = sum([ 1 if i else 0 for i in projects.values()])
        days = []
        for i in range(count-1):
            days.append(1/count)
        days.append(1-sum(days))

        query = db.session.query(
            ProjectLabor
        ).filter(
            ProjectLabor.employee_id == employee_id,
            ProjectLabor.date == date,
            ProjectLabor.assigned == 1
        ).all()
        days_pos = 0
        for i in query:
            if projects[i.project_id] == True:
                i.working_days = days[days_pos]
                days_pos += 1
            else:
                i.working_days = None
        db.session.commit()

    def get_hired_record(self):
        employee_id = self.employee_id
        query = db.session.query(
            HiredRecord
        ).filter(
            HiredRecord.employee_id == employee_id
        ).order_by(
            desc(HiredRecord.hired_date)
        ).all()
        return query
    
    def modify_hired_record(self, hired_date: str, resigned_date: str=None, sn: str=int):
        employee_id = self.employee_id
        resigned_date = resigned_date if resigned_date != '' else None
        if sn:
            query = db.session.query(
                HiredRecord
            ).filter(
                HiredRecord.sn == sn,
                HiredRecord.employee_id == employee_id
            ).first()

            query.hired_date = hired_date
            query.resigned_date = resigned_date
        else:
            query = db.session.query(
                HiredRecord
            ).filter(
                HiredRecord.employee_id == employee_id,
                HiredRecord.resigned_date != None
            ).all()

            if not query:
                assert False, "Still on the job."
            new = HiredRecord(
                employee_id=employee_id,
                hired_date=hired_date,
                resigned_date=resigned_date
            )
            db.session.add(new)
        db.session.commit()
        return True
    def delete_hired_record(self, sn: int):
        employee_id = self.employee_id
        db.session.query(
            HiredRecord
        ).filter(
            HiredRecord.employee_id == employee_id,
            HiredRecord.sn == sn
        ).delete()
        db.session.commit()
        return True

    def get_payment_record(self):
        try:
            employee_id = self.employee_id
        except:
            employee_id = None
        query = db.session.query(
            EmployeePayment
        ).filter(
            or_(
                employee_id == None,
                EmployeePayment.employee_id == employee_id
            )
        ).all()
        return query
    def modify_payment_record(self, **kwargs):
        kwargs['employee_id'] = self.employee_id
        sn = kwargs['sn']
        del kwargs['sn']
        if sn:
            db.session.query(
                EmployeePayment
            ).filter(
                EmployeePayment.employee_id == self.employee_id,
                EmployeePayment.sn == sn
            ).update(
                kwargs
            )
        else:
            db.session.add(
                EmployeePayment(
                    **kwargs
                )
            )
        db.session.commit()
        return True
    def delete_payment_record(self, sn):
        db.session.query(
            EmployeePayment
        ).filter(
            EmployeePayment.employee_id == self.employee_id,
            EmployeePayment.sn == sn
        ).delete()
        db.session.commit()
        return True

    def get_all_employee(self, date: str=''):
        employees_query = db.session.query(
            Employee
        ).join(
            HiredRecord
        ).filter(
            or_(
                date == '',
                and_(
                    HiredRecord.hired_date <= date,
                    or_(
                        HiredRecord.resigned_date == null(),
                        HiredRecord.resigned_date > date
                    )
                )
            )
        ).order_by(
            desc(HiredRecord.hired_date)
        ).all()
        employees = []
        for employee in employees_query:
            p = {}
            p['employee_id'] = employee.employee_id
            p['name'] = employee.name
            p['sex'] = '男' if employee.sex == 'm' else '女'
            p['birthday'] = employee.birthday.strftime('%Y-%m-%d')
            contact = ""
            if employee.telephone:
                contact += employee.telephone
                if employee.cellphone:
                    contact += ' / ' + employee.cellphone
            elif employee.cellphone:
                contact += employee.cellphone
            p['contact'] = contact
            p['address'] = employee.address
            p['email'] = employee.email
            p['hired_date'] = employee.HiredRecord[-1].hired_date.strftime('%Y-%m-%d')
            p['user_id'] = employee.Users[0].user_id

            if employee.Salary:
                salary = employee.Salary[-1]

                p['salary'] = salary.salary
                p['salary_unit'] = salary.unit
                p['salary_start_date'] = salary.start_date.strftime('%Y-%m-%d')
            employees.append(p)
        return tuple(employees)