from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
load_dotenv()

db = SQLAlchemy()

def create_app(config_file="config.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    api = Api(app)
    db.init_app(app)



    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .modules.database.flask_sqlalchemy_model import Users
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(user_id)
    
    db.drop_all(app=app)
    db.create_all(app=app)

    from .myAPI import (
        ProjectAPI, ProjectListAPI,
        ProjectDetailsAPI,
        ProjectDispatchAPI,
        ProjectCostAPI,
        PrejectOutsourcedAPI,
        ProjectPaymentAPI,
        OutsourcerAPI, OutsourcerListAPI,
        EmployeeAPI, EmployeeListAPI,
        EmployeeSalaryAPI,
        EmployeeDispatchByDateAPI, EmployeeDispatchByMonthAPI,
        EmployeeDispatchReportAPI,
        EmployeeHiredAPI,
        EmployeePaymentAPI,
        CustomerAPI, CustomerListAPI,
        StorehouseAPI, StorehouseListAPI,
        MatarialAPI, MatarialListAPI,
        MatarialBuyingAPI,
        MatarialUsingAPI,
        MatarialTransferAPI,
        MatarialSupplierAPI, MatarialSupplierListAPI,
        MiscellaneousExpenditureAPI,
        CompanyAPI, CompanyListAPI
    )
    api.add_resource(ProjectListAPI, "/api/project/", endpoint="project_api")
    api.add_resource(ProjectAPI, "/api/project/<string:project_id>")
    api.add_resource(ProjectDetailsAPI, "/api/projectDetails/<string:project_id>")
    api.add_resource(ProjectDispatchAPI, "/api/projectDispatch/<string:project_id>")
    api.add_resource(ProjectCostAPI, "/api/projectCost/<string:project_id>")
    api.add_resource(PrejectOutsourcedAPI, "/api/projectOutsourced/<string:project_id>")
    api.add_resource(ProjectPaymentAPI, "/api/projectPayment/<string:project_id>")

    api.add_resource(OutsourcerListAPI, "/api/outsourcer/")
    api.add_resource(OutsourcerAPI, "/api/outsourcer/<string:outsourcer_id>")

    api.add_resource(EmployeeListAPI, "/api/employee/")
    api.add_resource(EmployeeAPI, "/api/employee/<string:employee_id>")
    api.add_resource(EmployeeSalaryAPI, "/api/employeeSalary/<string:employee_id>")
    api.add_resource(EmployeeDispatchByDateAPI, "/api/employeeDispatch/<string:employee_id>/<string:date>")
    api.add_resource(EmployeeDispatchByMonthAPI, "/api/employeeDispatch/<string:employee_id>/<string:year>/<string:month>")
    api.add_resource(EmployeeDispatchReportAPI, "/api/employeeDispatchReport/")
    api.add_resource(EmployeeHiredAPI, "/api/employeeHired/<string:employee_id>")
    api.add_resource(EmployeePaymentAPI, "/api/employeePayment/<string:employee_id>")

    api.add_resource(CustomerListAPI, "/api/customer/")
    api.add_resource(CustomerAPI, "/api/customer/<string:customer_id>")

    api.add_resource(StorehouseListAPI, "/api/storehouse/")
    api.add_resource(StorehouseAPI, "/api/storehouse/<string:storehouse_id>")

    api.add_resource(MatarialListAPI, "/api/matarial/")
    api.add_resource(MatarialAPI, "/api/matarial/<string:matarial_id>")
    api.add_resource(MatarialBuyingAPI, "/api/matarial/buying/<string:matarial_id>")
    api.add_resource(MatarialUsingAPI, "/api/matarial/using/<string:matarial_id>")
    api.add_resource(MatarialTransferAPI, "/api/matarial/transfer/<string:matarial_id>")

    api.add_resource(MatarialSupplierListAPI, "/api/matarialSupplier/")
    api.add_resource(MatarialSupplierAPI, "/api/matarialSupplier/<string:matarial_supplier_id>")

    api.add_resource(MiscellaneousExpenditureAPI, "/api/miscellaneousExpenditure/")

    api.add_resource(CompanyListAPI, "/api/company/")
    api.add_resource(CompanyAPI, "/api/company/<string:company_id>")


    from .routes import auth_, project_, customer_, outsourcer_, employee_, employeeReport_, matarial_, storehouse_, miscellaneousExpenditure_, matarial_supplier_, company_
    app.register_blueprint(auth_, url_prefix='/')
    app.register_blueprint(project_, url_prefix='/project')
    app.register_blueprint(customer_, url_prefix='/customer')
    app.register_blueprint(outsourcer_, url_prefix='/outsourcer')
    app.register_blueprint(employee_, url_prefix='/employee')
    app.register_blueprint(employeeReport_, url_prefix='/employeeReport')
    app.register_blueprint(storehouse_, url_prefix='/storehouse')
    app.register_blueprint(matarial_, url_prefix='/matarial')
    app.register_blueprint(matarial_supplier_, url_prefix='/matarialSupplier')
    app.register_blueprint(miscellaneousExpenditure_, url_prefix='/miscellaneousExpenditure')
    app.register_blueprint(company_, url_prefix='/company')


    from .flaskCLI import cli
    app.register_blueprint(cli, cli_group=None)

    return app