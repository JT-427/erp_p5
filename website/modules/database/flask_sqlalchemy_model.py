from ... import db
from flask_login import UserMixin
from sqlalchemy import CheckConstraint, or_, null, func, text
import datetime as dt

class Users(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(32), db.ForeignKey('employee.employee_id'))
    password = db.Column(db.String(100))

    RUsersRole = db.relationship('RUsersRole', backref='users', lazy='select')
    MiscellaneousExpenditure = db.relationship(
        'MiscellaneousExpenditure',
        backref='Users', 
        lazy='select'
    )

    def get_id(self):
           return (self.user_id)
    @property
    def user_funcs(self):
        return Funcs.query.join(
            RRoleFunc
        ).join(
            Roles
        ).join(
            RUsersRole
        ).join(
            Users
        ).filter(
            Users.user_id == self.user_id
        )
    @property
    def user_roles(self):
        return Roles.query.join(
            RUsersRole
        ).join(
            Users
        ).filter(
            Users.user_id == self.user_id
        )
    def check_authority(self, func_module, func_name):
        """
        檢查使用者是否有權限進入該View Function
        :param
            func_module: View Function的module
            func_name: View Function的name
        :return:
            result: 有無權限 boolean
        """
        #  取得個人的權限表
        func_list = self.user_funcs
        #  func的table中記錄是module+.+func_name
        view_function = func_module + '.' + func_name
        result = func_list.filter(text("func_module_name=:view_function")) \
            .params(view_function=view_function).first()
        if result:
            return True
        else:
            return False

class RUsersRole(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), primary_key=True)
    

class Roles(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20), unique=True, nullable=False)
    role_description = db.Column(db.String(100))
    
    RRoleFunc = db.relationship('RRoleFunc', backref='roles', lazy='select')
    RUsersRole = db.relationship('RUsersRole', backref='roles', lazy='select')

class RRoleFunc(db.Model):
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), primary_key=True)
    func_id = db.Column(db.Integer, db.ForeignKey('funcs.func_id'), primary_key=True)

class Funcs(db.Model):
    func_id = db.Column(db.Integer, primary_key=True)
    func_module_name = db.Column(db.String(100), unique=True, nullable=False)
    func_description = db.Column(db.String(100))

    RRoleFunc = db.relationship('RRoleFunc', backref='funcs', lazy='select')

class Employee(db.Model):
    # 員工
    employee_id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    sex = db.Column(db.String(1), nullable=False)
    birthday = db.Column(db.Date)
    telephone = db.Column(db.String(10))
    cellphone = db.Column(db.String(10))
    address = db.Column(db.String(50))
    email = db.Column(db.String(50))

    Users = db.relationship('Users', backref='Employee', lazy='select')
    HiredRecord = db.relationship('HiredRecord', backref='Employee', lazy='select')
    Salary = db.relationship('Salary', backref='Employee', lazy='select')
    EmployeePayment = db.relationship('EmployeePayment', backref='Employee', lazy='select')
    ProjectLabor = db.relationship('ProjectLabor', backref='Employee', lazy='select')
    MatarialUsingRecord = db.relationship('MatarialUsingRecord', backref='Employee', lazy='select')
    MiscellaneousExpenditure = db.relationship('MiscellaneousExpenditure', backref='Employee', lazy='select')
    
class HiredRecord(db.Model):
    # 員工雇用紀錄
    sn = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(32), db.ForeignKey('employee.employee_id'))
    hired_date = db.Column(db.Date)
    resigned_date = db.Column(db.Date)

    __table_args__ = (
        CheckConstraint(
            or_(
                resigned_date == null(),
                func.date(hired_date) < resigned_date
            )
        ), 
    )

class Salary(db.Model):
    # 員工薪資紀錄
    sn = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(32), db.ForeignKey('employee.employee_id'))
    salary = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(5), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    __table_args__ = (
        CheckConstraint(salary > 0), 
        CheckConstraint(
            or_(
                end_date == null(),
                func.date(start_date) <= end_date
            )
        ), 
    )

class EmployeePayment(db.Model):
    # 員工薪水支付紀錄
    sn = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(32), db.ForeignKey('employee.employee_id'), nullable=False)
    date = db.Column(db.Date)
    type = db.Column(db.String(10)) # 可能是獎金或薪資
    amount = db.Column(db.Float, nullable=False)
    notes = db.Column(db.String(50))

class Matarial(db.Model):
    # 材料
    matarial_id = db.Column(db.String(32), primary_key=True)
    matarial_name = db.Column(db.String(30), nullable=False)
    unit = db.Column(db.String(10), nullable=False)
    notes = db.Column(db.String(50))

    MatarialInStorehouse = db.relationship('MatarialInStorehouse', backref='Matarial', lazy='select')
    MatarialBuyingRecord = db.relationship('MatarialBuyingRecord', backref='Matarial', lazy='select')
    MatarialUsingRecord = db.relationship('MatarialUsingRecord', backref='Matarial', lazy='select')
    MatarialTransferRecord = db.relationship('MatarialTransferRecord', backref='Matarial', lazy='select')
    MatarialRemainingAdjustmentRecord = db.relationship('MatarialRemainingAdjustmentRecord', backref='Matarial', lazy='select')

class MatarialInStorehouse(db.Model):
    sn = db.Column(db.Integer, primary_key=True)
    matarial_id = db.Column(db.String(32), db.ForeignKey('matarial.matarial_id'))
    storehouse_id = db.Column(db.String(32), db.ForeignKey('storehouse.storehouse_id'))
    date = db.Column(db.Date, default=dt.date.today(), nullable=False)
    remaining = db.Column(db.Float, nullable=False)
    notes = db.Column(db.String(50))

    __table_args__ = (
        CheckConstraint(remaining >= 0), 
    )

class MatarialBuyingRecord(db.Model):
    # 材料購買紀錄
    sn = db.Column(db.Integer, primary_key=True)
    matarial_id = db.Column(db.String(32), db.ForeignKey('matarial.matarial_id'), nullable=False)
    matarial_supplier_id = db.Column(db.String(32), db.ForeignKey('matarial_supplier.matarial_supplier_id'), nullable=False)
    storehouse_id = db.Column(db.String(32), db.ForeignKey('storehouse.storehouse_id'), nullable=False)
    buying_date = db.Column(db.Date, default=dt.date.today(), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    remaining = db.Column(db.Float, nullable=False) # 此購買紀錄的餘額，在「使用材料」時可以記錄

    MatarialUsingRecord = db.relationship('MatarialUsingRecord', backref='MatarialBuyingRecord', lazy='select')

class MatarialUsingRecord(db.Model):
    # 材料使用紀錄
    sn = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(32), db.ForeignKey('employee.employee_id'), nullable=False)
    matarial_id = db.Column(db.String(32), db.ForeignKey('matarial.matarial_id'), nullable=False)
    storehouse_id = db.Column(db.String(32), db.ForeignKey('storehouse.storehouse_id'), nullable=False)
    matarial_buying_sn = db.Column(db.Integer, db.ForeignKey('matarial_buying_record.sn'), nullable=False)
    date = db.Column(db.Date, default=dt.date.today(), nullable=False)
    project_id = db.Column(db.String(32), db.ForeignKey('project.project_id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)

class MatarialTransferRecord(db.Model):
    # 材料轉移
    sn = db.Column(db.Integer, primary_key=True)
    matarial_id = db.Column(db.String(32), db.ForeignKey('matarial.matarial_id'), nullable=False)
    storehouse_id_from = db.Column(db.String(32), db.ForeignKey('storehouse.storehouse_id'), nullable=False)
    storehouse_id_to = db.Column(db.String(32), db.ForeignKey('storehouse.storehouse_id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False) # 應大於0
    date = db.Column(db.Date, default=dt.date.today(), nullable=False)
    
    storehouse_from = db.relationship("Storehouse", foreign_keys=[storehouse_id_from])
    storehouse_to = db.relationship("Storehouse", foreign_keys=[storehouse_id_to])

    __table_args__ = (CheckConstraint(quantity > 0), )

class MatarialRemainingAdjustmentRecord(db.Model):
    #
    sn = db.Column(db.Integer, primary_key=True)
    storehouse_id = db.Column(db.String(32), db.ForeignKey('storehouse.storehouse_id'), nullable=False)
    matarial_id = db.Column(db.String(32), db.ForeignKey('matarial.matarial_id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=dt.date.today(), nullable=False)


class MatarialSupplier(db.Model):
    matarial_supplier_id = db.Column(db.String(32), primary_key=True)
    matarial_supplier_name = db.Column(db.String(50), nullable=False) 
    contact_person = db.Column(db.String(30))
    contact_number = db.Column(db.String(30))
    email = db.Column(db.String(50))
    notes = db.Column(db.String(50))
    cooperating = db.Column(db.Boolean, default=True, nullable=False)

class Storehouse(db.Model):
    storehouse_id = db.Column(db.String(32), primary_key=True)
    storehouse_name = db.Column(db.String(30), nullable=False)
    create_date = db.Column(db.Date, nullable=False)
    quit_date = db.Column(db.Date)
    address = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.String(50))

    __table_args__ = (
        CheckConstraint(
            or_(
                quit_date == null(),
                func.date(create_date) < quit_date
            )
        ), 
    )

    MatarialInStorehouse = db.relationship('MatarialInStorehouse', backref='Storehouse', lazy='select')
    MatarialBuyingRecord = db.relationship('MatarialBuyingRecord', backref='Storehouse', lazy='select')
    MatarialUsingRecord = db.relationship('MatarialUsingRecord', backref='Storehouse', lazy='select')
    MatarialRemainingAdjustmentRecord = db.relationship('MatarialRemainingAdjustmentRecord', backref='Storehouse', lazy='select')

class Outsourcer(db.Model):
    # 外包商
    outsourcer_id = db.Column(db.String(32), primary_key=True)
    outsourcer_name = db.Column(db.String(50), nullable=False)
    outsourcer_title = db.Column(db.String(50))
    address = db.Column(db.String(50))
    tax_id_num = db.Column(db.Integer)
    contact_person = db.Column(db.String(30))
    contact_number = db.Column(db.String(30))
    fax = db.Column(db.String(30))
    email = db.Column(db.String(50))
    invoice_date = db.Column(db.String(20)) # 請款日
    drawdown_date = db.Column(db.String(20)) # 放款日
    payment_method = db.Column(db.String(10)) # 付款方式
    notes = db.Column(db.String(100))

    ProjectOutsourced = db.relationship('ProjectOutsourced', backref='Outsourcer', lazy='select')
    

class Customer(db.Model):
    # 業主
    customer_id = db.Column(db.String(32), primary_key=True)
    customer_name = db.Column(db.String(50), nullable=False)
    customer_title = db.Column(db.String(50))
    address = db.Column(db.String(50))
    tax_id_num = db.Column(db.Integer)
    contact_person = db.Column(db.String(30))
    contact_number = db.Column(db.String(30))
    fax = db.Column(db.String(30)) # 傳真
    email = db.Column(db.String(50))
    invoice_date = db.Column(db.String(20)) # 請款日
    drawdown_date = db.Column(db.String(20)) # 放款日
    payment_method = db.Column(db.String(10)) # 付款方式
    notes = db.Column(db.String(100))

    Project = db.relationship('Project', backref='Customer', lazy='select')


class Project(db.Model):
    project_id = db.Column(db.String(100), primary_key=True)
    project_name = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    invoice = db.Column(db.Boolean, default=True, nullable=False)
    singing_date = db.Column(db.Date)
    start_date = db.Column(db.Date)
    finish_date = db.Column(db.Date)
    customer_id = db.Column(db.String(32), db.ForeignKey('customer.customer_id'), nullable=False)
    account_receivable = db.Column(db.Float, default=0, nullable=False)
    company_id = db.Column(db.String(32), db.ForeignKey('company.company_id'), nullable=False)
    referrer = db.Column(db.String(10))
    commision = db.Column(db.Float)

    __table_args__ = (
        CheckConstraint(account_receivable >= 0),
        CheckConstraint(
            or_(
                finish_date == null(),
                func.date(start_date) < finish_date
            )
        )
    )

    ProjectDetail = db.relationship('ProjectDetail', backref='Project', lazy='select')
    ProjectLabor = db.relationship('ProjectLabor', backref='Project', lazy='select')
    ProjectOutsourced = db.relationship('ProjectOutsourced', backref='Project', lazy='select')
    MatarialUsingRecord = db.relationship('MatarialUsingRecord', backref='Project', lazy='select')
    MiscellaneousExpenditure = db.relationship('MiscellaneousExpenditure', backref='Project', lazy='select')

class ProjectDetail(db.Model):
    sn = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.String(32), db.ForeignKey('project.project_id'), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(5), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

class ProjectLabor(db.Model):
    project_id = db.Column(db.String(32), db.ForeignKey('project.project_id'), primary_key=True)
    employee_id = db.Column(db.String(32), db.ForeignKey('employee.employee_id'), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    assigned = db.Column(db.Boolean, nullable=False)
    working_days = db.Column(db.Float)

class ProjectOutsourced(db.Model):
    sn = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.String(32), db.ForeignKey('project.project_id'))
    outsourcer_id = db.Column(db.String(32), db.ForeignKey('outsourcer.outsourcer_id'))
    description = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.String(100))

    __table_args__ = (
        CheckConstraint(price >= 0),
    )

class ProjectPayment(db.Model):
    # 收款紀錄
    sn = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.String(32), db.ForeignKey('project.project_id'), nullable=False)
    date = db.Column(db.Date)
    amount = db.Column(db.Float, nullable=False)
    notes = db.Column(db.String(50))

    __table_args__ = (
        CheckConstraint(amount != 0),
    )

class MiscellaneousExpenditure(db.Model):
    # 雜支
    sn = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    employee_id = db.Column(db.String(32), db.ForeignKey('employee.employee_id'))
    project_id = db.Column(db.String(32), db.ForeignKey('project.project_id'))
    description = db.Column(db.String(50))
    classification = db.Column(db.String(15), nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    __table_args__ = (
        CheckConstraint(price >= 0),
    )

class Company(db.Model):
    # 自己的公司
    company_id = db.Column(db.String(32), primary_key=True)
    company_name = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(50))
    postal_address = db.Column(db.String(50))
    tax_id_num = db.Column(db.Integer)
    responsible_person = db.Column(db.String(10))
    contact_person = db.Column(db.String(30))
    contact_number = db.Column(db.String(30))
    fax = db.Column(db.String(30))
    create_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    notes = db.Column(db.String(100))

    Project = db.relationship('Project', backref='Company', lazy='select')