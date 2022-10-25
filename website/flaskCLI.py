import os
import requests
import pandas as pd
import numpy as np
import datetime as dt
from flask import Blueprint
from sqlalchemy.sql import func

from website.modules.company import CompanyC

from . import db
from .modules import CustomerC
from .modules.database.flask_sqlalchemy_model import Employee, Project, ProjectLabor

cli = Blueprint('cli', __name__, cli_group=None)


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
            "Authorization": "Bearer " + os.environ.get('LINE_NOTIFY'),
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

@cli.cli.command('test')
def test():
    from inspect import getmembers, isfunction
    from .modules.database.flask_sqlalchemy_model import Funcs, Roles, RRoleFunc
    from .routes import project, customer, outsourcer, employee, matarial, storehouse, miscellaneous_expenditure, matarial_supplier, employee_report, company
    for g in [project, customer, outsourcer, employee, matarial, storehouse, miscellaneous_expenditure, matarial_supplier, employee_report, company]:
        for i in getmembers(g, isfunction):
            if i[1].__module__.split('.')[0] == 'website' and i[1].__module__.split('.')[1] == 'routes':
                func_module_name = i[1].__module__ + '.' + i[1].__name__
                # func create
                db.session.add(
                    Funcs(
                        func_module_name = func_module_name
                    )
                )
    db.session.commit()
    # role create
    db.session.add(
        Roles(
            role_id = 2,
            role_name = 'admin'
        )
    )
    db.session.add(
        Roles(
            role_id = 1,
            role_name = '一般員工'
        )
    )
    db.session.add(
        Roles(
            role_id = 3,
            role_name = '管理庫存'
        )
    )
    db.session.add(
        Roles(
            role_id = 4,
            role_name = '管理雜支'
        )
    )
    db.session.add(
        Roles(
            role_id = 5,
            role_name = '管理案場'
        )
    )
    db.session.add(
        Roles(
            role_id = 6,
            role_name = '管理業主'
        )
    )
    db.session.add(
        Roles(
            role_id = 7,
            role_name = '管理外包商'
        )
    )
    db.session.commit()
    for func in Funcs.query.all():
        if func.func_module_name != 'website.routes.employee_report.index':
            db.session.add(
                RRoleFunc(
                    role_id = 2,
                    func_id = func.func_id
                )
            )
        else:
            db.session.add(
                RRoleFunc(
                    role_id = 1,
                    func_id = func.func_id
                )
            )
        if func.func_module_name in ("website.routes.matarial.buying", "website.routes.matarial.index", "website.routes.matarial.transfer", "website.routes.matarial.using", "website.routes.storehouse.index"):
            db.session.add(
                RRoleFunc(
                    role_id = 3,
                    func_id = func.func_id
                )
            )
        if func.func_module_name == 'website.routes.miscellaneous_expenditure.index':
            db.session.add(
                RRoleFunc(
                    role_id = 4,
                    func_id = func.func_id
                )
            )
        if func.func_module_name in (
            'website.routes.project.index', 
            'website.routes.project.details', 
            'website.routes.project.outsourced'):
            db.session.add(
                RRoleFunc(
                    role_id = 5,
                    func_id = func.func_id
                )
            )
        if func.func_module_name == 'website.routes.customer.index':
            db.session.add(
                RRoleFunc(
                    role_id = 6,
                    func_id = func.func_id
                )
            )
        if func.func_module_name == 'website.routes.outsourcer.index':
            db.session.add(
                RRoleFunc(
                    role_id = 7,
                    func_id = func.func_id
                )
            )
    db.session.commit()
    sqls = [
        "INSERT INTO `employee` VALUES ('9c85m724564740005247865622088847','最高權限','m','1990-01-01','','','','');",
        "INSERT INTO `hired_record` VALUES (1,'9c85m724564740005247865622088847','2022-08-01',NULL);",
        "INSERT INTO `users` VALUES (1,'9c85m724564740005247865622088847','sha256$X5QXG5FzqowBmLNZ$cb1a59380d73c84fb01498a20a1a0b61f7a1d9a9d0fed9adf397da5fd96c7c68');",
        "INSERT INTO `r_users_role` VALUES (1, 2)"
    ]
    for sql in sqls:
        db.session.execute(sql)
        db.session.commit()

    return ''

@cli.cli.command('import_data')
def import_data():
    customers = pd.read_excel('../import_data/customer.xlsx')
    customers.replace(np.nan, None, inplace=True)
    for record in customers.to_dict('index').values():
        CustomerC().create(**record)

    companies = pd.read_excel('../import_data/company.xlsx')
    companies.replace(np.nan, None, inplace=True)
    for record in companies.to_dict('index').values():
        CompanyC().create(**record)
        
