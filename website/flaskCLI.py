from flask import Blueprint

from . import db
from .modules.database.flask_sqlalchemy_model import Customer, Employee, Funcs, HiredRecord, Project, ProjectDetail, RRoleFunc, Roles, Salary, Users

cli = Blueprint('cli', __name__, cli_group=None)

@cli.cli.command('check_matarial')
def check_matarial():
    result = db.session.execute(
        """
        call check_matarial()
        """
    ).fetchall()
    for i in result:
        print(i.remaining_should_be == i.remaining)
